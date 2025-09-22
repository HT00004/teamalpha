# 🎖️ Mission Alpha - Azure AI Foundry Integration

**Operation Synthetic Shield: Advanced AI-Powered Pension Data Generation**

Generate realistic synthetic UK pension member data using Azure AI Foundry for testing and development purposes, with **zero PII exposure**.

## 🚀 Quick Start

### Option 1: Demo Mode (Immediate Start)
```bash
python launch_enhanced.py
# Select option 1 for instant demo
```

### Option 2: Azure AI Mode (Full AI Power)
```bash
python launch_enhanced.py
# Select option 3 to configure Azure AI
# Then select option 2 to launch with AI
```

## 🔧 Azure AI Foundry Setup

### Prerequisites
1. **Azure subscription** with access to Azure AI Foundry
2. **Deployed model** in Azure AI Foundry (recommended: GPT-4o)
3. **API endpoint and key** from your deployment

### Step-by-Step Configuration

1. **Deploy a Model in Azure AI Foundry**
   - Go to [Azure AI Foundry](https://ai.azure.com)
   - Create or select a project
   - Deploy a model (GPT-4o recommended for best results)
   - Note the endpoint URL and API key

2. **Configure Mission Alpha**
   ```bash
   python launch_enhanced.py
   # Select option 3: Setup Azure AI Configuration
   ```
   
3. **Edit the generated .env file**
   ```env
   # Replace these with your actual Azure AI Foundry details
   AZURE_AI_ENDPOINT=https://your-foundry-endpoint.region.inference.ml.azure.com
   AZURE_AI_KEY=your-actual-api-key-here
   AZURE_AI_MODEL=your-model-deployment-name
   
   # Optional settings
   ENABLE_AZURE_AI=true
   FALLBACK_TO_DEMO=true  # Falls back to demo if AI fails
   ```

4. **Launch with Azure AI**
   ```bash
   python launch_enhanced.py
   # Select option 2: Azure AI Version
   ```

## 📊 Features Comparison

| Feature | Demo Mode | Azure AI Mode |
|---------|-----------|---------------|
| **Data Generation** | Built-in algorithms | AI-powered realistic generation |
| **Setup Time** | Instant | 5-10 minutes |
| **Dependencies** | Streamlit only | + Azure AI SDK |
| **Realism** | Good | Excellent |
| **Customization** | Limited | High (AI prompts) |
| **Cost** | Free | Azure AI costs |
| **Edge Cases** | Predefined | AI-generated |

## 🎯 Generated Data Types

### Member Profiles
- **Demographics**: Age, gender, location (UK postcodes)
- **Employment**: Sector, job grade, salary
- **Pension Details**: Years of service, status
- **Compliance**: UK auto-enrollment regulations

### Contribution History
- **Monthly Records**: Employee and employer contributions
- **Realistic Patterns**: Career progression, salary changes
- **Edge Cases**: Career breaks, rate changes

### Fund Allocations
- **Investment Preferences**: Risk-appropriate allocations
- **Age-Based Strategies**: Conservative → Aggressive
- **Compliance**: 100% total allocation validation

## 📈 CSV Export Options

### Individual Files
- `pension_members_YYYYMMDD_HHMMSS.csv` - Member profiles
- `pension_contributions_YYYYMMDD_HHMMSS.csv` - Contribution history
- `pension_allocations_YYYYMMDD_HHMMSS.csv` - Fund allocations
- `pension_analytics_YYYYMMDD_HHMMSS.csv` - Statistical analysis
- `mission_summary_YYYYMMDD_HHMMSS.csv` - Executive summary

### Complete Package
- **ZIP file** with all data + documentation
- **Mission manifest** with metadata
- **Validation report** (JSON)
- **README** with usage instructions

## 🔒 Security & Compliance

### Zero PII Guarantee
- ✅ **No real personal data** used or generated
- ✅ **Synthetic identities** only
- ✅ **Safe for testing** environments
- ✅ **GDPR compliant** (no personal data)

### UK Pension Compliance
- ✅ **Auto-enrollment** minimum contributions (3%)
- ✅ **Realistic salary** distributions by sector
- ✅ **Age-appropriate** contribution patterns
- ✅ **Valid UK postcodes** with regional clustering

## 🛠️ Technical Architecture

### Azure AI Integration
```python
# Azure AI Foundry Client
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key)
)
```

### Fallback Strategy
1. **Primary**: Azure AI Foundry generation
2. **Secondary**: Built-in demo algorithms (if AI fails)
3. **Configuration**: Controlled via `FALLBACK_TO_DEMO` setting

### Performance Optimization
- **Batch Processing**: Generate data in configurable batches
- **Caching**: Smart pattern caching for large datasets
- **Progressive Loading**: Real-time progress updates

## 🎖️ Mission Scenarios

### Testing Pension Systems
- **System Integration**: Realistic data for API testing
- **Load Testing**: Generate 1,000-5,000 member records
- **Edge Case Testing**: Career gaps, high earners, transfers

### Business Analysis
- **Statistical Validation**: Distribution analysis
- **Compliance Testing**: Regulatory requirement validation
- **Performance Benchmarking**: System capacity testing

### Development
- **Database Population**: Realistic test data
- **UI Testing**: Representative member scenarios
- **Algorithm Validation**: Business rule testing

## 📚 API Reference

### Environment Variables
```env
# Required for Azure AI mode
AZURE_AI_ENDPOINT=<your-foundry-endpoint>
AZURE_AI_KEY=<your-api-key>
AZURE_AI_MODEL=<your-model-name>

# Optional configuration
ENABLE_AZURE_AI=true|false
FALLBACK_TO_DEMO=true|false
DEFAULT_MEMBER_COUNT=1000
MAX_MEMBER_COUNT=5000
```

### Launch Options
```bash
python launch_enhanced.py
# 1. Demo Version - Immediate start
# 2. Azure AI Version - Full AI power
# 3. Setup Configuration - Initial setup
# 4. System Information - Status check
```

## 🔧 Troubleshooting

### Common Issues

#### "Azure AI dependencies not installed"
```bash
pip install azure-ai-inference python-dotenv
```

#### "Azure AI configuration issue"
- Check `.env` file exists and has correct values
- Verify endpoint URL format: `https://your-endpoint.../`
- Confirm API key is valid and not expired

#### "Connection failed"
- Verify internet connectivity
- Check Azure AI Foundry service status
- Validate endpoint URL and API key

#### "Generation failed"
- Enable fallback mode: `FALLBACK_TO_DEMO=true`
- Check Azure AI service limits/quotas
- Try smaller batch sizes

### Debug Mode
Enable verbose logging by setting:
```env
STREAMLIT_LOGGER_LEVEL=debug
```

## 📞 Support

### Mission Command
- **Technical Issues**: Check troubleshooting section
- **Configuration Help**: Use setup assistant (option 3)
- **Azure AI Issues**: Verify Azure AI Foundry deployment

### Resources
- [Azure AI Foundry Documentation](https://docs.microsoft.com/azure/ai-services/)
- [Mission Alpha Demo](http://localhost:8501) (when running)
- [UK Pension Regulations](https://www.gov.uk/workplace-pensions)

---

## 📋 Mission Status

**Classification**: OPERATION SYNTHETIC SHIELD  
**Security Level**: ZERO PII RISK  
**Compliance**: UK PENSION REGULATIONS  
**Status**: READY FOR DEPLOYMENT  

🎖️ **Mission Alpha Command**: *"Generate synthetic intelligence that serves our testing purposes while maintaining complete operational security."*
