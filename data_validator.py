import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import re

class PensionDataValidator:
    def __init__(self, csv_file):
        """Initialize validator with path to CSV file"""
        try:
            self.data = pd.read_csv(csv_file, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                self.data = pd.read_csv(csv_file, encoding='latin-1')
            except:
                self.data = pd.read_csv(csv_file, encoding='cp1252')
        
        # Print column names for debugging
        print(f"Available columns: {list(self.data.columns)}")
        
        # Clean up numeric fields
        numeric_fields = ['Age', 'AnnualSalary', 'YearsService']
        for field in numeric_fields:
            if field in self.data.columns:
                # Convert to string and clean
                self.data[field] = self.data[field].astype(str)
                # Remove currency symbols and special characters
                self.data[field] = (self.data[field]
                                  .str.replace('£', '', regex=False)
                                  .str.replace('�', '', regex=False)  # Handle encoding issues
                                  .str.replace(',', '', regex=False)
                                  .str.strip())
                
                # Convert to numeric, handling any remaining non-numeric values
                self.data[field] = pd.to_numeric(self.data[field], errors='coerce')
        
        print(f"\nLoaded {len(self.data)} records for validation")
        self.validation_results = {}
        
    def validate_all(self):
        """Run all validation checks"""
        print("🔍 Running comprehensive data validation...")
        print("===========================================")
        
        # Run all validation checks
        self.check_distributions()
        self.validate_business_rules()
        self.check_data_integrity()
        self.validate_geographic_distribution()
        self.validate_sector_patterns()
        
        # Print summary
        self.print_summary()
        
    def check_distributions(self):
        """Validate statistical distributions"""
        print("\n📊 Checking Statistical Distributions...")
        
        # Gender Distribution (Expected: M=49%, F=50%, O=1%)
        gender_dist = self.data['Gender'].value_counts(normalize=True)
        gender_valid = (
            abs(gender_dist.get('M', 0) - 0.49) < 0.05 and
            abs(gender_dist.get('F', 0) - 0.50) < 0.05 and
            abs(gender_dist.get('O', 0) - 0.01) < 0.01
        )
        
        # Age Distribution (22-75 years, peaks at 25-35 and 45-55)
        age_valid = (
            self.data['Age'].between(22, 75).all() and
            self.data['Age'].value_counts(bins=[22,35,45,55,75]).index.size == 4
        )
        
        # Sector Distribution
        expected_sector_dist = {
            'Finance': 0.15,
            'Manufacturing': 0.12,
            'Public Service': 0.18,
            'Healthcare': 0.13,
            'Education': 0.10,
            'Retail': 0.08,
            'Other': 0.24
        }
        
        sector_dist = self.data['Sector'].value_counts(normalize=True)
        sector_valid = all(
            abs(sector_dist.get(sector, 0) - expected) < 0.05
            for sector, expected in expected_sector_dist.items()
        )
        
        self.validation_results['distributions'] = {
            'gender_distribution': gender_valid,
            'age_distribution': age_valid,
            'sector_distribution': sector_valid
        }
        
        print(f"✓ Gender Distribution: {'✅' if gender_valid else '❌'}")
        print(f"✓ Age Distribution: {'✅' if age_valid else '❌'}")
        print(f"✓ Sector Distribution: {'✅' if sector_valid else '❌'}")
        
    def validate_business_rules(self):
        """Validate business rules and relationships"""
        print("\n📋 Validating Business Rules...")
        
        # Salary ranges by sector
        salary_rules = {
            'Finance': (25000, 120000),
            'Public Service': (20000, 80000),
            'Manufacturing': (18000, 75000),
            'Healthcare': (22000, 85000)
        }
        
        salary_valid = all(
            self.data[self.data['Sector'] == sector]['AnnualSalary'].between(
                min_sal, max_sal
            ).all()
            for sector, (min_sal, max_sal) in salary_rules.items()
        )
        
        # Years service validation (must be less than age - 18)
        service_valid = (
            self.data['YearsService'] <= (self.data['Age'] - 18)
        ).all()
        
        # Status validation
        valid_statuses = {'Active', 'Deferred', 'Pensioner'}
        status_valid = self.data['Status'].isin(valid_statuses).all()
        
        self.validation_results['business_rules'] = {
            'salary_ranges': salary_valid,
            'service_years': service_valid,
            'status_values': status_valid
        }
        
        print(f"✓ Salary Ranges: {'✅' if salary_valid else '❌'}")
        print(f"✓ Service Years: {'✅' if service_valid else '❌'}")
        print(f"✓ Status Values: {'✅' if status_valid else '❌'}")
        
    def check_data_integrity(self):
        """Check data integrity and format"""
        print("\n🔐 Checking Data Integrity...")
        
        # Member ID format (MB + 8 digits)
        member_id_valid = self.data['MemberID'].str.match(r'^MB\d{8}$').all()
        
        # UK Postcode format
        postcode_pattern = r'^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$'
        postcode_valid = self.data['Postcode'].str.match(postcode_pattern).all()
        
        # No duplicate Member IDs
        no_duplicates = not self.data['MemberID'].duplicated().any()
        
        self.validation_results['integrity'] = {
            'member_id_format': member_id_valid,
            'postcode_format': postcode_valid,
            'no_duplicates': no_duplicates
        }
        
        print(f"✓ Member ID Format: {'✅' if member_id_valid else '❌'}")
        print(f"✓ Postcode Format: {'✅' if postcode_valid else '❌'}")
        print(f"✓ No Duplicates: {'✅' if no_duplicates else '❌'}")
        
    def validate_geographic_distribution(self):
        """Validate geographic distribution of members"""
        print("\n🗺️ Checking Geographic Distribution...")
        
        # Check postcode areas distribution
        postcode_areas = self.data['Postcode'].str[:2].value_counts()
        
        # Ensure major UK cities are represented
        major_cities = {'L', 'M', 'B', 'S', 'N', 'E', 'W', 'G'}
        cities_covered = all(
            any(area.startswith(city) for area in postcode_areas.index)
            for city in major_cities
        )
        
        self.validation_results['geographic'] = {
            'major_cities_covered': cities_covered
        }
        
        print(f"✓ Major Cities Coverage: {'✅' if cities_covered else '❌'}")
        
    def validate_sector_patterns(self):
        """Validate sector-specific patterns"""
        print("\n🏢 Checking Sector Patterns...")
        
        # Check job grades are appropriate for sectors
        finance_grades = {'Analyst', 'Senior', 'Manager', 'Director', 'Consultant'}
        public_grades = {'Grade', 'Officer', 'Principal', 'Senior'}
        
        finance_valid = any(
            any(grade.lower() in job.lower() 
                for grade in finance_grades)
            for job in self.data[self.data['Sector'] == 'Finance']['JobGrade']
        )
        
        public_valid = any(
            any(grade.lower() in job.lower() 
                for grade in public_grades)
            for job in self.data[self.data['Sector'] == 'Public Service']['JobGrade']
        )
        
        self.validation_results['sector_patterns'] = {
            'finance_grades': finance_valid,
            'public_service_grades': public_valid
        }
        
        print(f"✓ Finance Job Grades: {'✅' if finance_valid else '❌'}")
        print(f"✓ Public Service Grades: {'✅' if public_valid else '❌'}")
        
    def print_summary(self):
        """Print overall validation summary"""
        print("\n📑 VALIDATION SUMMARY")
        print("===================")
        
        all_checks = []
        for category, checks in self.validation_results.items():
            all_checks.extend(checks.values())
        
        total_checks = len(all_checks)
        passed_checks = sum(all_checks)
        
        print(f"Total Checks: {total_checks}")
        print(f"Passed: {passed_checks}")
        print(f"Failed: {total_checks - passed_checks}")
        print(f"Success Rate: {(passed_checks/total_checks)*100:.1f}%")
        
        if passed_checks == total_checks:
            print("\n✅ All validation checks passed!")
        else:
            print("\n⚠️ Some validation checks failed. Review the details above.")
            
    def generate_visualization(self):
        """Generate visualizations of key distributions"""
        print("\n📈 Generating Data Visualizations...")
        
        # Create a figure with multiple subplots
        fig = plt.figure(figsize=(15, 10))
        
        # 1. Age Distribution
        plt.subplot(2, 2, 1)
        self.data['Age'].hist(bins=20)
        plt.title('Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Count')
        
        # 2. Sector Distribution
        plt.subplot(2, 2, 2)
        self.data['Sector'].value_counts().plot(kind='bar')
        plt.title('Sector Distribution')
        plt.xticks(rotation=45)
        
        # 3. Salary Distribution
        plt.subplot(2, 2, 3)
        self.data['AnnualSalary'].hist(bins=20)
        plt.title('Salary Distribution')
        plt.xlabel('Annual Salary')
        plt.ylabel('Count')
        
        # 4. Years of Service Distribution
        plt.subplot(2, 2, 4)
        self.data['YearsService'].hist(bins=20)
        plt.title('Years of Service Distribution')
        plt.xlabel('Years')
        plt.ylabel('Count')
        
        plt.tight_layout()
        plt.savefig('data_distributions.png')
        print("✅ Visualizations saved as 'data_distributions.png'")

if __name__ == "__main__":
    # Create validator instance
    validator = PensionDataValidator('generated_pension_data_fixed.csv')
    
    # Run all validations
    validator.validate_all()
    
    # Generate visualizations
    validator.generate_visualization()