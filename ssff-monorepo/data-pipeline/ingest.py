import json
import os

# Placeholder for Phase 1: Data Pipeline
# This script will:
# 1. Read raw_data.json
# 2. Generate Embeddings (pgvector)
# 3. Call LLM to extract {Origin, Destination, Time, Urgency}
# 4. Insert into DB

def ingest_data(file_path="raw_data.json"):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Run crawler first.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Ingesting {len(data)} items...")
    
    for item in data:
        print(f"Processing: {item['content'][:50]}...")
        
        # --- PROMPT LOGIC ---
        # matches the user's feedback about Route Extraction
        prompt = f"""
        Analyze the following logistics social media post:
        "{item['content']}"

        Extract:
        1. **Origin** (City/Province). If strictly From A to B, this is A.
        2. **Destination** (City/Province). If strictly From A to B, this is B.
        3. **Commodity** (e.g., Rice, Fruit).
        4. **Urgency Score** (0-100). 100 = Desperate/Emergency. 0 = Normal/Ad.
        
        Return JSON: {{ "origin": "...", "destination": "...", "commodity": "...", "urgency": int }}
        """
        
        # print(f"DEBUG Prompt: {prompt}")

        # TODO: 
        # 1. embedding = get_embedding(item['content'])
        # 2. extraction = call_llm(prompt) -> returns JSON
        # 3. db.execute("INSERT INTO vectors ...")
        # 4. db.execute("INSERT INTO signals (location_id=origin_id, ...)") 
        #    # Note: We map the 'Signal' to the Origin because that's where the truck is needed.
        # 5. db.execute("INSERT INTO flows (origin, dest, ...) ...")
        pass

    print("Ingestion Complete.")

if __name__ == "__main__":
    ingest_data()
