#!/usr/bin/env python3
"""
🔬 Test Data Realism Comparison
Quick test to verify the data realism comparison functionality
"""

import pandas as pd
from data_realism_comparator import DataRealismComparator

def test_realism_comparison():
    """Test the data realism comparison functionality"""
    
    print("🔬 Testing Data Realism Comparison...")
    
    try:
        # Initialize comparator
        comparator = DataRealismComparator()
        print("✅ DataRealismComparator initialized successfully")
        
        # Test with the generated pension data
        file_path = "generated_pension_data_fixed.csv"
        
        print(f"🔍 Loading data from: {file_path}")
        
        # Load and inspect the data first
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        print(f"✅ Loaded {len(df)} records")
        print(f"📊 Columns: {list(df.columns)}")
        print(f"🔍 Sample data:")
        print(df.head())
        
        # Run the comparison
        print("\n🚀 Running realism comparison...")
        results = comparator.compare_synthetic_vs_real(file_path)
        
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            return False
        
        # Display results
        print("\n🏆 REALISM ANALYSIS RESULTS")
        print("=" * 50)
        
        overall_score = results.get('overall_realism_score', 0)
        print(f"📊 Overall Realism Score: {overall_score:.2%}")
        
        if overall_score >= 0.8:
            print("🏆 EXCELLENT - Synthetic data closely matches UK pension patterns")
        elif overall_score >= 0.6:
            print("⚠️ GOOD - Some areas need improvement")
        else:
            print("❌ POOR - Significant improvements needed")
        
        # Category breakdown
        print(f"\n📊 Category Breakdown:")
        detailed = results.get('detailed_comparisons', {})
        
        for category, data in detailed.items():
            score = data.get('accuracy_score', 0)
            passes = data.get('passes_test', False)
            status = "✅" if passes else "❌"
            print(f"{status} {category.title()}: {score:.2%}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        recommendations = results.get('recommendations', [])
        for rec in recommendations:
            print(f"  • {rec}")
        
        print("\n🎖️ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_realism_comparison()
