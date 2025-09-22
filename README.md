# 🎖️ MISSION ALPHA - PENSION PHANTOM GENERATOR
## Operation Synthetic Shield - Data Generation Division

**AI-driven synthetic pension data generation using Azure AI Foundry**

> Generate 1,000-5,000 realistic UK pension member records that pass operational "Turing Tests" while maintaining complete civilian identity protection.

---

## 🚀 QUICK START

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Configure AI Service
Copy `.env.example` to `.env` and configure:

**Option A: Azure AI Foundry (Recommended)**
```env
AZURE_ENDPOINT=https://your-foundry-endpoint.openai.azure.com/
AZURE_API_KEY=your_azure_api_key
MODEL_DEPLOYMENT_NAME=gpt-4o
```

**Option B: GitHub Models (Alternative)**
```env
GITHUB_TOKEN=your_github_token
```

### 3. Run Setup Check
```powershell
python setup.py
```

### 4. Run Quick Demo
```powershell
python quick_demo.py
```

### 5. Execute Full Mission
```powershell
python pension_phantom_generator.py
```

---

## 🎯 MISSION OBJECTIVES

✅ **Scale Achievement**: Generate 1,000-5,000 synthetic member records  
✅ **Security Clearance**: Zero PII exposure - complete civilian identity protection  
✅ **Statistical Accuracy**: Generated data matches real population distributions  
✅ **Business Rule Compliance**: All operational rules validate correctly  
✅ **Edge Case Coverage**: Include realistic boundary conditions and anomalies  
✅ **Scalability Proof**: Algorithm design that could handle production volumes  

---

## 🛠️ SYSTEM ARCHITECTURE

### AI-First Approach
- **Primary Weapon**: GPT-4o via Azure AI Foundry for realistic persona generation
- **Secondary System**: GitHub Models for fallback capability
- **Orchestration**: Semantic Kernel patterns for multi-step data generation
- **Validation**: AI-driven quality checks and business rule compliance

### Data Generation Pipeline
1. **Member Profiles**: AI generates realistic demographics with UK population patterns
2. **Contribution History**: AI creates contribution patterns following UK pension regulations
3. **Fund Allocations**: AI determines age-appropriate risk allocations totaling 100%
4. **Quality Validation**: Statistical analysis and business rule compliance checking
5. **Export**: CSV files and JSON validation reports

---

## 📊 GENERATED DATA SCHEMA

### Member Profiles (`pension_members_TIMESTAMP.csv`)
```
member_id      | Unique identifier (MB12345678)
age           | 22-67 (UK workforce distribution)
gender        | M/F/Other (realistic proportions)
postcode      | Valid UK format with regional clustering
sector        | Finance, Healthcare, Public Service, etc.
job_grade     | Age and sector appropriate titles
annual_salary | £18,000-£120,000 (sector specific ranges)
years_service | Realistic career progression patterns
status        | Active/Deferred/Pensioner/Deceased
start_date    | Calculated from service years
```

### Contribution History (`pension_contributions_TIMESTAMP.csv`)
```
member_id         | Reference to member profile
contribution_date | Monthly contribution dates
employee_amount   | 3-8% of salary (auto-enrollment compliance)
employer_amount   | 3-12% of salary (matching schemes)
salary_at_date    | Salary when contribution was made
contribution_type | Monthly/Annual/Irregular patterns
```

### Fund Allocations (`pension_fund_allocations_TIMESTAMP.csv`)
```
member_id         | Reference to member profile
fund_name         | Available pension fund options
allocation_percent| Percentage allocation (totals 100%)
selection_date    | When allocation was chosen
risk_level        | High/Medium/Low risk classification
```

---

## 🤖 AI MODEL CONFIGURATION

### Azure AI Foundry Setup
1. Create Azure AI Foundry resource
2. Deploy GPT-4o model
3. Copy endpoint and API key to `.env`
4. Test connection with `python setup.py`

### GitHub Models Setup
1. Get GitHub token with model access
2. Add token to `.env` file
3. System automatically uses `openai/gpt-4.1` model

### Model Selection Priority
1. **Azure AI Foundry** (if configured) - Production grade
2. **GitHub Models** (fallback) - Development/testing

---

## 📈 BUSINESS RULES IMPLEMENTED

### UK Pension Regulations
- Auto-enrollment minimum 3% employee contribution
- Employer matching schemes (3-12% typical range)
- Annual allowance compliance (£60,000 limit)
- Age-appropriate salary progression

### Statistical Accuracy
- UK population age distribution patterns
- Employment sector clustering by region
- Realistic career progression and salary bands
- Life event impacts on contribution patterns

### Fund Allocation Logic
- **Age 22-35**: Growth strategy (60-80% equity)
- **Age 36-50**: Balanced approach (40-60% equity)
- **Age 51-67**: Conservative shift (20-40% equity)
- Total allocations always equal 100%

---

## 🧪 VALIDATION & QUALITY ASSURANCE

### Automated Checks
- **PII Scanning**: Zero real personal information
- **Statistical Validation**: Distribution analysis against baselines
- **Business Rules**: Contribution limits and fund allocation compliance
- **Data Integrity**: Referential integrity and format validation

### Output Validation Report
```json
{
  "total_members": 2500,
  "age_distribution": {"min": 22, "max": 67, "mean": 44.2},
  "salary_stats": {"min": 18000, "max": 120000, "mean": 42500},
  "fund_allocation_checks": {
    "allocation_compliance_rate": 0.98
  }
}
```

---

## 🎪 USAGE EXAMPLES

### Quick Demo (5 sample members)
```powershell
python quick_demo.py
```

### Small Scale Test (100 members)
```powershell
# Edit .env: MEMBER_COUNT=100
python pension_phantom_generator.py
```

### Full Mission (2,500 members)
```powershell
# Edit .env: MEMBER_COUNT=2500
python pension_phantom_generator.py
```

### Large Scale (5,000 members)
```powershell
# Edit .env: MEMBER_COUNT=5000
python pension_phantom_generator.py
```

---

## 📁 OUTPUT FILES

All files are timestamped for version control:

- `pension_members_20241222_143052.csv` - Member profiles
- `pension_contributions_20241222_143052.csv` - Contribution history
- `pension_fund_allocations_20241222_143052.csv` - Fund selections
- `validation_report_20241222_143052.json` - Quality metrics

---

## 🔧 CONFIGURATION OPTIONS

### Environment Variables (`.env`)
```env
# AI Service Configuration
AZURE_ENDPOINT=your_azure_foundry_endpoint
AZURE_API_KEY=your_azure_api_key
MODEL_DEPLOYMENT_NAME=gpt-4o
GITHUB_TOKEN=your_github_token

# Generation Settings
MEMBER_COUNT=2500                    # Number of members to generate
OUTPUT_FORMAT=csv                    # Export format
INCLUDE_EDGE_CASES=true             # Include boundary conditions
```

### Advanced Configuration
- **Batch Size**: Adjust batch processing (default: 50 members)
- **Temperature**: AI creativity level (default: 0.7)
- **Sample Size**: Contribution/allocation sample percentage
- **Validation Tolerance**: Business rule compliance thresholds

---

## 🚨 TROUBLESHOOTING

### Common Issues

**❌ "No AI credentials found"**
- Solution: Configure `.env` with Azure or GitHub credentials

**❌ "AI API Error"**
- Solution: Check API key validity and endpoint configuration
- Verify model deployment in Azure AI Foundry

**❌ "JSON Parse Error"**
- Solution: AI response formatting issue - retry with different temperature
- Check AI service status and rate limits

**❌ "Dependencies missing"**
- Solution: Run `pip install -r requirements.txt`

### Debug Mode
```powershell
# Enable verbose logging
python pension_phantom_generator.py --debug
```

---

## 🏆 SUCCESS METRICS

### Mission Accomplished When:
- [x] Generated 1,000+ realistic pension member records
- [x] Zero PII exposure (all synthetic data)
- [x] 95%+ business rule compliance rate
- [x] Statistical distributions match UK patterns
- [x] Fund allocations total exactly 100%
- [x] Edge cases and anomalies included
- [x] Scalable architecture demonstrated

### Bonus Achievements:
🎖️ **Innovation Medal**: Novel AI prompt engineering techniques  
🎖️ **Efficiency Citation**: Sub-10 minute generation for 1,000 records  
🎖️ **Realism Award**: Indistinguishable from real pension data  

---

## 📞 SUPPORT

### Technical Support
- GitHub Issues for bug reports
- Check Azure AI Foundry service status
- Verify GitHub Models token permissions

### Documentation
- [Azure AI Foundry Documentation](https://docs.microsoft.com/azure/ai/)
- [GitHub Models Documentation](https://docs.github.com/models)
- [UK Pension Regulations](https://www.gov.uk/workplace-pensions)

---

## 🎖️ MISSION COMMAND

**CLASSIFICATION**: Hackathon Participants Only  
**AUTHORIZATION**: Operation Synthetic Shield Command  
**STATUS**: Ready for Deployment

---

*"At Bletchley Park, we didn't just decode messages - we created entirely new forms of communication. Your mission continues this tradition: create data that serves our testing purposes while appearing completely authentic to business systems."*

**GOOD LUCK, SQUADRON! THE DIGITAL FRONT DEPENDS ON YOUR SUCCESS.** 🎖️
