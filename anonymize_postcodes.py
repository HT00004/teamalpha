import pandas as pd
import re
import glob

def anonymize_postcode(postcode):
    """
    Anonymize UK postcode by replacing the second part with XXX
    Examples: 
    - M1 1AA -> M1 XXX
    - EC1A 1BB -> EC1A XXX
    - B2 4QA -> B2 XXX
    """
    if pd.isna(postcode) or not isinstance(postcode, str):
        return postcode
    
    # UK postcode pattern: first part (1-4 chars) + space + second part (3 chars)
    match = re.match(r'^([A-Z]{1,2}[0-9]{1,2}[A-Z]?)\s+([0-9][A-Z]{2})$', postcode.upper().strip())
    
    if match:
        first_part = match.group(1)
        return f"{first_part} XXX"
    else:
        # If it doesn't match standard format, try to extract first part and add XXX
        parts = postcode.strip().split()
        if len(parts) >= 1:
            return f"{parts[0]} XXX"
        else:
            return postcode  # Return as-is if can't parse

def anonymize_csv_file(input_file, output_file=None):
    """
    Anonymize postcodes in a CSV file
    """
    if output_file is None:
        output_file = input_file.replace('.csv', '_anonymized.csv')
    
    try:
        # Read CSV file
        df = pd.read_csv(input_file)
        
        # Find postcode column (case insensitive)
        postcode_col = None
        for col in df.columns:
            if col.lower() in ['postcode', 'post_code', 'zipcode', 'zip_code']:
                postcode_col = col
                break
        
        if postcode_col is None:
            print(f"❌ No postcode column found in {input_file}")
            return False
        
        # Count original postcodes
        original_count = len(df[postcode_col].dropna())
        
        # Anonymize postcodes
        df[postcode_col] = df[postcode_col].apply(anonymize_postcode)
        
        # Count anonymized postcodes
        anonymized_count = len(df[df[postcode_col].str.contains('XXX', na=False)])
        
        # Save anonymized file
        df.to_csv(output_file, index=False)
        
        print(f"✅ {input_file} -> {output_file}")
        print(f"   Original postcodes: {original_count}")
        print(f"   Anonymized: {anonymized_count}")
        print(f"   Success rate: {anonymized_count/original_count*100:.1f}%" if original_count > 0 else "   No postcodes to anonymize")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing {input_file}: {str(e)}")
        return False

def main():
    """
    Main function to anonymize all CSV files in the current directory
    """
    print("🔒 POSTCODE ANONYMIZATION TOOL")
    print("=" * 50)
    
    # Find all CSV files
    csv_files = glob.glob("*.csv")
    csv_files = [f for f in csv_files if not f.endswith('_anonymized.csv')]  # Skip already anonymized files
    
    if not csv_files:
        print("❌ No CSV files found in current directory")
        return
    
    print(f"📁 Found {len(csv_files)} CSV files to process:")
    for file in csv_files:
        print(f"   • {file}")
    
    print("\n🔄 Processing files...")
    
    success_count = 0
    for file in csv_files:
        if anonymize_csv_file(file):
            success_count += 1
        print()  # Empty line for readability
    
    print(f"✅ Successfully processed {success_count}/{len(csv_files)} files")
    print("\n💡 Anonymized files have '_anonymized' suffix")

if __name__ == "__main__":
    main()
