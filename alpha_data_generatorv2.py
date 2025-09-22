import os
import sys
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder
import pandas as pd

# Constants for data generation
CHUNK_SIZE = 50  # Generate data in chunks of 50 records
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
    print(f"Generating chunk of {chunk_size} records starting from ID {start_id}")
    
    generation_prompt = f"""Generate exactly {chunk_size} rows of synthetic pension member data as CSV. Follow these specifications PRECISELY:

Start with header row:
MemberID,Age,Gender,Postcode,Sector,JobGrade,AnnualSalary,YearsService,Status

Requirements:
1. MemberID: Start from MB{start_id:08d} and increment by 1 for each row

2. Age Distribution:
   - 22-35: 40% of records
   - 36-45: 25% of records
   - 46-55: 25% of records
   - 56-75: 10% of records

3. Gender: Exact proportions:
   - M: 49%
   - F: 50%
   - O: 1%

4. Postcode: Use ONLY these formats:
   London: EC1A 1BB, SW1A 1AA, W1A 1AA, E1 6AN, N1 9GU
   Manchester: M1 1AA, M2 5BQ, M3 3EB
   Birmingham: B1 1HQ, B2 4QA, B3 3DH
   Glasgow: G1 1XW, G2 8DL
   Edinburgh: EH1 1BB, EH2 2ER
   Cardiff: CF10 1DD, CF11 9LJ
   Liverpool: L1 8JQ, L2 2PP
   Leeds: LS1 1UR, LS2 8JS
   Bristol: BS1 4TR, BS2 0FZ

5. Sector Distribution:
   Finance(15%), Manufacturing(12%), Public Service(18%), 
   Healthcare(13%), Education(10%), Retail(8%), Other(24%)

6. JobGrade by sector:
   Finance: [Analyst, Senior Analyst, Associate, Manager, Senior Manager, Director]
   Public Service: [Grade 7, Grade 6, Senior Officer, Principal Officer]
   Manufacturing: [Technician, Senior Technician, Supervisor, Production Manager]
   Healthcare: [Band 5, Band 6, Band 7, Senior Practitioner]
   Education: [Teacher, Senior Teacher, Head of Department, Deputy Head]
   Retail: [Sales Assistant, Supervisor, Store Manager, Area Manager]
   Other: [Associate, Consultant, Senior Consultant, Manager]

7. AnnualSalary ranges:
   Finance: 25000-120000 (40% between 35000-55000)
   Public Service: 20000-80000 (50% between 30000-45000)
   Manufacturing: 18000-75000 (60% between 28000-38000)
   Healthcare: 22000-85000 (45% between 32000-48000)
   Education: 24000-65000 (55% between 30000-45000)
   Retail: 18000-55000 (70% between 22000-35000)
   Other: 20000-90000 (45% between 35000-55000)

8. YearsService rules:
   - Cannot exceed (Age - 21)
   - Typically 20-40% of working age
   - More years in public sector

9. Status Distribution:
   Active(70%), Deferred(20%), Pensioner(10%, age 55+)

CRITICAL:
- Provide ONLY CSV data, no explanations
- Start with header row
- Generate EXACTLY {chunk_size} records
- Each record MUST follow ALL rules above
- No markdown formatting or code blocks"""

    try:
        # Create a thread for this chunk
        thread = project_client.agents.threads.create()
        
        # Send the generation request
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=generation_prompt
        )
        
        # Process the request
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )
        
        if run.status == "failed":
            print(f"❌ Chunk generation failed: {run.last_error}")
            return None
            
        # Get the response
        messages = project_client.agents.messages.list(
            thread_id=thread.id,
            order=ListSortOrder.ASCENDING
        )
        
        # Get the last message
        agent_messages = [msg for msg in messages if msg.role == "assistant" and msg.text_messages]
        if not agent_messages:
            print("❌ No response received from agent")
            return None
            
        response = agent_messages[-1].text_messages[-1].text.value
        
        # Clean up any markdown or code formatting
        clean_data = response.replace('```', '').strip()
        if clean_data.startswith('csv\n'):
            clean_data = clean_data[4:]
        
        return clean_data

    except Exception as e:
        print(f"❌ Error generating chunk: {str(e)}")
        return None

def generate_pension_data(num_records=REQUIRED_RECORDS):
    """Generate the complete pension dataset in chunks"""
    print(f"🎯 Alpha Data Generator: Generating {num_records} pension records")
    print("=======================================================")
    
    chunks = []
    current_id = 1
    
    # Generate data in chunks
    while current_id < num_records:
        chunk_size = min(CHUNK_SIZE, num_records - current_id + 1)
        chunk_data = generate_chunk(current_id, chunk_size)
        
        if chunk_data is None:
            print(f"❌ Failed to generate chunk starting at {current_id}")
            return False
        
        chunks.append(chunk_data)
        current_id += chunk_size
        print(f"✅ Generated {chunk_size} records ({current_id-1}/{num_records})")
    
    try:
        # Combine all chunks
        all_data = []
        header = None
        
        for chunk in chunks:
            lines = chunk.strip().split('\n')
            if header is None:
                header = lines[0]
                all_data.append(header)
            all_data.extend(lines[1:])
        
        # Save the combined data
        output_file = "generated_pension_data.csv"
        with open(output_file, "w") as f:
            f.write('\n'.join(all_data))
        
        print(f"\n✅ Successfully generated {num_records} pension records")
        print(f"📁 Data saved to: {output_file}")
        return True

    except Exception as e:
        print(f"❌ Error saving combined data: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Check Azure CLI authentication scope:")
        print("   az login --scope https://ai.azure.com/.default")
        print("2. Verify virtual environment is activated (.venv)")
        print("3. Confirm access to Azure AI Foundry project")
        return False

if __name__ == "__main__":
    generate_pension_data()