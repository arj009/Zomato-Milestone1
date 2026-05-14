import logging
from phase1.ingest import build_catalog_from_hf_dataset
from phase1.catalog import save_catalog_jsonl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Dataset ID from problem statement
    DATASET_ID = "ManikaSaini/zomato-restaurant-recommendation"
    OUTPUT_PATH = "data/catalog.jsonl"
    
    print("Starting Phase 1: Data Ingestion...")
    
    try:
        # 1. Build catalog from Hugging Face
        catalog = build_catalog_from_hf_dataset(DATASET_ID)
        
        # 2. Save to local JSONL for Phase 2/3
        save_catalog_jsonl(catalog, OUTPUT_PATH)
        
        print(f"Success! Catalog saved to {OUTPUT_PATH}")
        print(f"Total unique restaurants processed: {catalog.size}")
        
    except Exception as e:
        logging.error(f"Phase 1 failed: {e}")

if __name__ == "__main__":
    main()
