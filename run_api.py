import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    print(f"Starting Zomato AI Backend on port {port}...")
    print(f"URL: http://localhost:{port}")
    print(f"Documentation: http://localhost:{port}/docs")
    
    uvicorn.run(
        "phase4.app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
