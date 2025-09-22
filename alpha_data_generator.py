import os
import sys
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder

# Constants for data generation
REQUIRED_RECORDS = 1000
PROJECT_ENDPOINT = "https://ais-hack-u5nxuil7gjgjq.services.ai.azure.com/api/projects/lgir-team-alpha"
AGENT_ID = "asst_YRz6huPVHYlT3Dwvm5cVlVi0"

# Initialize Azure AI connection
project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)
agent = project_client.agents.get_agent(AGENT_ID)

def generate_chunk(start_id, chunk_size, output_file="generated_pension_data.csv"):
    """Generate a chunk of pension data
    
    Args:
        start_id (int): Starting member ID number
        chunk_size (int): Number of records to generate
        output_file (str): Output CSV filename
        
    Returns:
        bool: Success status
    """
    generation_prompt = f"""Generate {chunk_size} rows of synthetic pension member data as a CSV table. 
    Member IDs should start from MB{start_id:08d} and increment by 1 for each record. Start immediately with the header row followed by data rows. Follow these EXACT specifications carefully:

Header row must be exactly:
MemberID,Age,Gender,Postcode,Sector,JobGrade,AnnualSalary,YearsService,Status

Data requirements:
1. MemberID: STRICT format "MB" followed by exactly 8 digits (e.g., MB12345678). Each ID must be unique.

2. Age Distribution (MUST match these percentages exactly for {chunk_size} records):
   DETAILED AGE BRACKETS:
   - 22-27: 15% of records ({int(chunk_size * 0.15)} records)
   - 28-32: 15% of records ({int(chunk_size * 0.15)} records)  
   - 33-35: 10% of records ({int(chunk_size * 0.10)} records)
   - 36-40: 15% of records ({int(chunk_size * 0.15)} records)
   - 41-45: 10% of records ({int(chunk_size * 0.10)} records)
   - 46-50: 15% of records ({int(chunk_size * 0.15)} records)
   - 51-55: 10% of records ({int(chunk_size * 0.10)} records)
   - 56-65: 7% of records ({int(chunk_size * 0.07)} records)
   - 66-75: 3% of records ({int(chunk_size * 0.03)} records)
   
   SUMMARY: Young Adults (22-35): 40%, Mid-Career (36-45): 25%, Experienced (46-55): 25%, Senior (56-75): 10%

3. Gender: EXACTLY these proportions for {chunk_size} records:
   - M: 49% of records ({int(chunk_size * 0.49)} records)
   - F: 50% of records ({int(chunk_size * 0.50)} records)
   - O: 1% of records ({int(chunk_size * 0.01)} records)

4. Postcode: Valid UK format with ANONYMIZED second half. Use these EXACT formats for major cities (second half anonymized with XXX):
   London: EC1A XXX, SW1A XXX, W1A XXX, E1 XXX, N1 XXX
   Manchester: M1 XXX, M2 XXX, M3 XXX
   Birmingham: B1 XXX, B2 XXX, B3 XXX
   Glasgow: G1 XXX, G2 XXX
   Edinburgh: EH1 XXX, EH2 XXX
   Cardiff: CF10 XXX, CF11 XXX
   Liverpool: L1 XXX, L2 XXX
   Leeds: LS1 XXX, LS2 XXX
   Bristol: BS1 XXX, BS2 XXX

5. Sector Distribution (MUST match exactly for {chunk_size} records):
   - Finance: 15% ({int(chunk_size * 0.15)} records)
   - Manufacturing: 12% ({int(chunk_size * 0.12)} records)
   - Public Service: 18% ({int(chunk_size * 0.18)} records)
   - Healthcare: 13% ({int(chunk_size * 0.13)} records)
   - Education: 10% ({int(chunk_size * 0.10)} records)
   - Retail: 8% ({int(chunk_size * 0.08)} records)
   - Other: 24% ({int(chunk_size * 0.24)} records)

6. JobGrade: Use these EXACT titles by sector:
   Finance: [Analyst, Senior Analyst, Associate, Manager, Senior Manager, Director]
   Public Service: [Grade 7, Grade 6, Senior Officer, Principal Officer]
   Manufacturing: [Technician, Senior Technician, Supervisor, Production Manager]
   Healthcare: [Band 5, Band 6, Band 7, Senior Practitioner]
   Education: [Teacher, Senior Teacher, Head of Department, Deputy Head]
   Retail: [Sales Assistant, Supervisor, Store Manager, Area Manager]
   Other: [Associate, Consultant, Senior Consultant, Manager]

7. AnnualSalary: EXACTLY these ranges (use whole numbers without commas):
   - Finance: 25000-120000 (40% between 35000-55000)
   - Public Service: 20000-80000 (50% between 30000-45000)
   - Manufacturing: 18000-75000 (60% between 28000-38000)
   - Healthcare: 22000-85000 (45% between 32000-48000)
   - Education: 24000-65000 (55% between 30000-45000)
   - Retail: 18000-55000 (70% between 22000-35000)
   - Other: 20000-90000 (45% between 35000-55000)

8. YearsService: Must correlate with age:
   - Cannot exceed (Age - 21)
   - Typically 20-40% of working age
   - More years of service in public sector roles

9. Status Distribution for {chunk_size} records:
   - Active: 70% ({int(chunk_size * 0.70)} records)
   - Deferred: 20% ({int(chunk_size * 0.20)} records)
   - Pensioner: 10% ({int(chunk_size * 0.10)} records - must be age 55+)

Important:
- Provide ONLY the CSV data with no explanations or markdown
- Start with the header row immediately
- Use exact distributions specified above
- Maintain logical relationships between fields
- Each row must pass ALL validation rules

Important:
- Provide ONLY the CSV data with no explanations or markdown
- Start with the header row immediately
- Ensure exact column names and proper CSV formatting
- Include {chunk_size} data rows
- Maintain data integrity and realistic correlations
- Use only realistic UK postcodes with anonymized second half (XXX format)
- Ensure no real PII is included"""

    try:
        # Create a thread for our conversation
        thread = project_client.agents.threads.create()
        print(f"✅ Thread created: {thread.id}")
        
        # Send the generation request
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=generation_prompt
        )
        print("✅ Generation request sent to agent")
        
        # Process the request
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )
        
        if run.status == "failed":
            print(f"❌ Generation failed: {run.last_error}")
            return False
            
        # Get the response
        messages = project_client.agents.messages.list(
            thread_id=thread.id,
            order=ListSortOrder.ASCENDING
        )
        
        # Get the last message from the agent
        agent_messages = [msg for msg in messages if msg.role == "assistant" and msg.text_messages]
        if not agent_messages:
            print("❌ No response received from agent")
            return False
            
        last_message = agent_messages[-1].text_messages[-1].text.value
        
        # Clean up the response to remove any markdown or code formatting
        clean_data = last_message.replace('```plaintext\n', '').replace('```', '').strip()
        
        with open(output_file, "w") as f:
            f.write(clean_data)
        
        print(f"✅ Successfully generated {chunk_size} pension records")
        print(f"📁 Data saved to: {output_file}")
        return True

    except Exception as e:
        print(f"❌ Error generating data: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Make sure you're signed in to Azure CLI with correct scope:")
        print("   az login --scope https://ai.azure.com/.default")
        print("2. Check that your virtual environment is activated (.venv)")
        print("3. Ensure you have access to the Azure AI Foundry project")
        return False

def generate_pension_data(num_records=REQUIRED_RECORDS, output_file="generated_pension_data.csv", start_id=1):
    """Generate pension data with specified parameters
    
    Args:
        num_records (int): Number of records to generate
        output_file (str): Output CSV filename
        start_id (int): Starting ID for member records
        
    Returns:
        bool: Success status
    """
    try:
        print(f"🚀 Starting pension data generation...")
        print(f"📊 Records to generate: {num_records}")
        print(f"📁 Output file: {output_file}")
        print(f"🆔 Starting ID: MB{start_id:08d}")
        
        # For large datasets, generate in chunks to avoid Azure AI token limits
        MAX_CHUNK_SIZE = 1000  # Azure AI works well with up to 1000 records per request
        
        if num_records <= MAX_CHUNK_SIZE:
            # Small dataset - generate in one go
            success = generate_chunk(start_id, num_records, output_file)
        else:
            # Large dataset - generate in chunks and combine
            print(f"📦 Large dataset detected - generating in chunks of {MAX_CHUNK_SIZE}")
            success = generate_large_dataset(num_records, output_file, start_id, MAX_CHUNK_SIZE)
        
        if success:
            print(f"✅ Generation completed successfully!")
            return True
        else:
            print(f"❌ Generation failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error in main generation function: {str(e)}")
        return False

def generate_large_dataset(total_records, output_file, start_id, chunk_size):
    """Generate large datasets by breaking into chunks and combining
    
    Args:
        total_records (int): Total number of records to generate
        output_file (str): Final output CSV filename
        start_id (int): Starting ID for member records
        chunk_size (int): Size of each chunk
        
    Returns:
        bool: Success status
    """
    import pandas as pd
    import tempfile
    import os
    
    try:
        # Calculate number of chunks needed
        num_chunks = (total_records + chunk_size - 1) // chunk_size  # Ceiling division
        
        print(f"📊 Generating {total_records} records in {num_chunks} chunks of {chunk_size}")
        
        temp_files = []
        current_id = start_id
        
        # Generate each chunk
        for chunk_num in range(num_chunks):
            remaining_records = total_records - (chunk_num * chunk_size)
            current_chunk_size = min(chunk_size, remaining_records)
            
            print(f"🔄 Generating chunk {chunk_num + 1}/{num_chunks} ({current_chunk_size} records)")
            
            # Create temporary file for this chunk
            temp_file = f"temp_chunk_{chunk_num}.csv"
            temp_files.append(temp_file)
            
            # Generate chunk
            success = generate_chunk(current_id, current_chunk_size, temp_file)
            
            if not success:
                print(f"❌ Failed to generate chunk {chunk_num + 1}")
                # Clean up temp files
                for tf in temp_files:
                    if os.path.exists(tf):
                        os.remove(tf)
                return False
            
            current_id += current_chunk_size
            print(f"✅ Chunk {chunk_num + 1} completed")
        
        # Combine all chunks into final file
        print(f"🔗 Combining {len(temp_files)} chunks into final file...")
        combined_df = None
        
        for i, temp_file in enumerate(temp_files):
            if os.path.exists(temp_file):
                chunk_df = pd.read_csv(temp_file)
                
                if combined_df is None:
                    combined_df = chunk_df
                else:
                    combined_df = pd.concat([combined_df, chunk_df], ignore_index=True)
                
                # Clean up temp file
                os.remove(temp_file)
                print(f"✅ Merged chunk {i + 1}")
        
        # Save final combined file
        if combined_df is not None:
            combined_df.to_csv(output_file, index=False)
            print(f"💾 Final dataset saved with {len(combined_df)} records")
            return True
        else:
            print("❌ No data to save")
            return False
            
    except Exception as e:
        print(f"❌ Error in large dataset generation: {str(e)}")
        # Clean up any remaining temp files
        for tf in temp_files:
            if os.path.exists(tf):
                os.remove(tf)
        return False

def validate_age_brackets(chunk_size):
    """Validate that age bracket calculations sum to 100% for given chunk size"""
    
    brackets = {
        "22-27": 0.15,
        "28-32": 0.15, 
        "33-35": 0.10,
        "36-40": 0.15,
        "41-45": 0.10,
        "46-50": 0.15,
        "51-55": 0.10,
        "56-65": 0.07,
        "66-75": 0.03
    }
    
    total_percentage = sum(brackets.values())
    total_records = sum(int(chunk_size * percentage) for percentage in brackets.values())
    
    print(f"📊 Age Bracket Validation for {chunk_size} records:")
    print(f"   Total percentage: {total_percentage:.2%}")
    print(f"   Calculated records: {total_records}/{chunk_size}")
    print(f"   Difference: {chunk_size - total_records} records")
    
    if abs(total_percentage - 1.0) > 0.01:
        print(f"⚠️  Warning: Percentages don't sum to 100% ({total_percentage:.2%})")
    
    return brackets

if __name__ == "__main__":
    generate_pension_data()