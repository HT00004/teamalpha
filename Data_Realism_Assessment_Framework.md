# 🎯 Data Realism Assessment Framework
## Mission Alpha - Synthetic vs Real UK Pension Data Comparison

---

## 📋 **Overview**

This framework provides a comprehensive methodology for assessing the realism of synthetic UK pension data by comparing it against real industry benchmarks and statistics. The assessment uses a weighted scoring system across multiple categories to generate an overall realism score.

---

## 🏗️ **Assessment Categories & Weights**

### **1. Age Distribution Analysis** 
**Weight: 20%**

#### Age Bins & UK Benchmarks:
- **22-29 years**: 20% of workforce
- **30-39 years**: 28% of workforce
- **40-49 years**: 26% of workforce
- **50-59 years**: 20% of workforce
- **60-67 years**: 6% of workforce

#### Methodology:
- Creates age bins using pandas cut function
- Compares synthetic distribution percentages against real UK workforce data
- Calculates accuracy using: `max(0, 1 - (total_difference / 2))`

#### Pass Criteria:
- **Pass Threshold**: 80% accuracy
- **Data Source**: ONS workforce demographics

---

### **2. Gender Distribution Analysis**
**Weight: 15%**

#### Categories & UK Benchmarks:
- **Male (M)**: 52% workforce participation
- **Female (F)**: 47% workforce participation  
- **Other/Non-binary (O)**: 1%

#### Methodology:
- Direct percentage comparison of gender distribution
- Handles flexible column naming (Gender, gender, Gender_Code, sex)
- Statistical difference calculation with error percentages

#### Pass Criteria:
- **Pass Threshold**: 90% accuracy
- **Data Source**: ONS gender workforce statistics

---

### **3. Sector Distribution Analysis**
**Weight: 20%**

#### Sectors & UK Benchmarks:
- **Finance**: 14%
- **Manufacturing**: 10%
- **Public Service**: 19%
- **Healthcare**: 13%
- **Education**: 9%
- **Retail**: 11%
- **Other**: 24%

#### Methodology:
- Compares employment sector distribution across industries
- Flexible column detection for sector/industry fields
- Percentage difference analysis for each sector

#### Pass Criteria:
- **Pass Threshold**: 70% accuracy
- **Data Source**: UK employment sector statistics

---

### **4. Salary Pattern Analysis**
**Weight: 25% (Highest Importance)**

#### Sector-Specific Salary Ranges & Medians:

| Sector | Min Salary | Max Salary | Median Salary |
|--------|------------|------------|---------------|
| **Finance** | £25,000 | £150,000 | £45,000 |
| **Manufacturing** | £20,000 | £80,000 | £32,000 |
| **Public Service** | £18,000 | £85,000 | £35,000 |
| **Healthcare** | £22,000 | £90,000 | £38,000 |
| **Education** | £24,000 | £70,000 | £35,000 |
| **Retail** | £18,000 | £55,000 | £26,000 |
| **Other** | £20,000 | £100,000 | £35,000 |

#### Methodology:
- **Median Accuracy**: `1 - abs(synthetic_median - real_median) / real_median`
- **Range Accuracy**: Compares min/max salary ranges for each sector
- **Overall Score**: Average of median and range accuracy per sector
- Handles currency symbol cleaning and numeric conversion

#### Pass Criteria:
- **Pass Threshold**: 70% accuracy per sector
- **Data Source**: UK salary surveys and government statistics

---

### **5. Geographic Distribution Analysis**
**Weight: 10%**

#### UK Regions & Distribution:
- **London**: 22%
- **South East**: 18%
- **North West**: 12%
- **West Midlands**: 9%
- **Yorkshire**: 8%
- **Scotland**: 8%
- **East**: 7%
- **South West**: 6%
- **East Midlands**: 5%
- **Wales**: 3%
- **North East**: 2%

#### Postcode to Region Mapping:
```
'EC1', 'SW1', 'W1A', 'E1', 'N1' → London
'M1', 'M2', 'M3', 'L1', 'L2' → North West
'B1', 'B2', 'B3' → West Midlands
'G1', 'G2', 'EH1', 'EH2' → Scotland
'LS1', 'LS2' → Yorkshire
'BS1', 'BS2' → South West
'CF10', 'CF11' → Wales
```

#### Methodology:
- Extracts postcode area from full postcodes
- Maps postcode areas to UK regions
- Compares regional distribution percentages
- Only analyzes regions with available data

#### Pass Criteria:
- **Pass Threshold**: 60% accuracy
- **Data Source**: ONS regional employment data

---

### **6. Member Status Distribution**
**Weight: 10%**

#### Status Categories & Benchmarks:
- **Active**: 75% (actively contributing members)
- **Deferred**: 20% (non-contributing but not yet receiving benefits)
- **Pensioner**: 5% (receiving pension benefits)

#### Methodology:
- Direct comparison of member status percentages
- Flexible column naming support
- Standard distribution difference calculation

#### Pass Criteria:
- **Pass Threshold**: 80% accuracy
- **Data Source**: TPR (The Pensions Regulator) member statistics

---

### **7. Years of Service Patterns**
**Weight: Included in analysis**

#### Service Bins & Patterns:
- **0-5 years**: 40%
- **6-15 years**: 35%
- **16-25 years**: 15%
- **26-35 years**: 8%
- **36+ years**: 2%

#### Methodology:
- Creates service year bins using pandas cut
- Compares distribution across career length categories
- Reflects typical UK employment tenure patterns

#### Pass Criteria:
- **Pass Threshold**: 70% accuracy
- **Data Source**: UK employment tenure statistics

---

## 📊 **Overall Scoring Methodology**

### **Weighted Score Calculation:**
```python
overall_score = Σ(category_accuracy × category_weight)

weights = {
    "age": 0.20,
    "gender": 0.15, 
    "sector": 0.20,
    "salary": 0.25,  # Highest weight
    "geographic": 0.10,
    "status": 0.10
}
```

### **Individual Category Scoring:**
```python
accuracy_score = max(0, 1 - (total_difference / normalization_factor))
```

### **Grade Classifications:**

| Score Range | Grade | Description |
|-------------|-------|-------------|
| **80-100%** | 🏆 **Excellent** | Synthetic data closely matches UK pension patterns |
| **60-79%** | ⚠️ **Good** | Some areas need improvement |
| **0-59%** | ❌ **Poor** | Significant improvements needed |

---

## 🔍 **Data Sources & Validation**

### **Primary Sources:**
- **ONS (Office for National Statistics)**: Workforce demographics, regional data
- **TPR (The Pensions Regulator)**: Pension industry statistics  
- **UK Government**: Employment sector data, salary surveys
- **Industry Reports**: Pension scheme benchmarking studies

### **Quality Assurance:**
- Multiple encoding support for CSV files
- Currency symbol cleaning and normalization
- Missing data handling and validation
- Flexible column name detection
- Error handling and fallback mechanisms

---

## 📈 **Output & Reporting**

### **Analysis Results Include:**
1. **Overall Realism Score** (0-100%)
2. **Category-by-Category Breakdown** with pass/fail status
3. **Detailed Distribution Comparisons** (synthetic vs real percentages)
4. **Interactive Visualizations** (gauges, bar charts, comparisons)
5. **Improvement Recommendations** based on weak areas
6. **Statistical Error Analysis** for each category

### **Visualization Components:**
- **Realism Gauge**: Overall score with color-coded thresholds
- **Distribution Charts**: Side-by-side comparison bars
- **Salary Analysis**: Sector-specific median and range comparisons
- **Geographic Mapping**: Regional distribution analysis

---

## 🎯 **Implementation Notes**

### **Technical Requirements:**
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualizations
- **streamlit**: Web interface integration
- **numpy**: Statistical calculations

### **File Format Support:**
- UTF-8, Latin1, CP1252, ISO-8859-1 encoding detection
- CSV format with flexible column naming
- Currency symbol cleaning (£, $, commas)
- Automatic data type conversion

### **Error Handling:**
- Graceful degradation for missing columns
- Encoding fallback mechanisms  
- Data validation and cleaning
- Comprehensive error reporting

---

## 📋 **Usage Guidelines**

### **Best Practices:**
1. **Data Preparation**: Ensure CSV files have clear column headers
2. **File Naming**: Use descriptive names for synthetic data files
3. **Sample Size**: Minimum 100 records for meaningful analysis
4. **Column Standards**: Follow standard naming conventions when possible

### **Interpretation:**
- **Focus on weighted categories**: Salary patterns have highest impact
- **Regional limitations**: Geographic analysis limited to mapped postcodes  
- **Sector coverage**: Ensure all major employment sectors represented
- **Continuous monitoring**: Regular realism assessment during data generation

---

*Framework developed for Mission Alpha hackathon challenge - Synthetic UK Pension Data Generation and Validation.*
