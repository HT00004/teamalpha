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

def generate_chunk(start_id, chunk_size):
    """Generate a chunk of pension data"""
    generation_prompt = f"""Generate {chunk_size} rows of synthetic pension member data as a CSV table. 
    Member IDs should start from MB{start_id:08d} and increment by 1 for each record. Start immediately with the header row followed by data rows. Follow these EXACT specifications carefully:

Header row must be exactly:
MemberID,Age,Gender,Postcode,Sector,JobGrade,AnnualSalary,YearsService,Status

Data requirements:
1. MemberID: STRICT format "MB" followed by exactly 8 digits (e.g., MB12345678). Each ID must be unique.

2. Age Distribution (MUST match these percentages exactly):
   - 22-35: 40% of records
   - 36-45: 25% of records
   - 46-55: 25% of records
   - 56-75: 10% of records

3. Gender: EXACTLY these proportions:
   - M: 49% of records
   - F: 50% of records
   - O: 1% of records

4. Postcode: Valid UK format only. Use these EXACT formats for major cities:
   London: EC1A 1BB, SW1A 1AA, W1A 1AA, E1 6AN, N1 9GU
   Manchester: M1 1AA, M2 5BQ, M3 3EB
   Birmingham: B1 1HQ, B2 4QA, B3 3DH
   Glasgow: G1 1XW, G2 8DL
   Edinburgh: EH1 1BB, EH2 2ER
   Cardiff: CF10 1DD, CF11 9LJ
   Liverpool: L1 8JQ, L2 2PP
   Leeds: LS1 1UR, LS2 8JS
   Bristol: BS1 4TR, BS2 0FZ

5. Sector Distribution (MUST match exactly):
   - Finance: 15%
   - Manufacturing: 12%
   - Public Service: 18%
   - Healthcare: 13%
   - Education: 10%
   - Retail: 8%
   - Other: 24%

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

9. Status Distribution:
   - Active: 70%
   - Deferred: 20%
   - Pensioner: 10% (must be age 55+)

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
- Include {num_records} data rows
- Maintain data integrity and realistic correlations
- Use only realistic UK postcodes
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
        
        # Save the generated data
        output_file = "generated_pension_data.csv"
        
        # Clean up the response to remove any markdown or code formatting
        clean_data = last_message.replace('```plaintext\n', '').replace('```', '').strip()
        
        with open(output_file, "w") as f:
            f.write(clean_data)
        
        print(f"✅ Successfully generated {num_records} pension records")
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

if __name__ == "__main__":
    generate_pension_data()