from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production on Render
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log the current directory and its contents for debugging
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Directory contents: {os.listdir('.')}")

# Check if static directory exists
static_dir = "/app/static"
if os.path.exists(static_dir):
    logger.info(f"Static directory exists at {static_dir}")
    logger.info(f"Static directory contents: {os.listdir(static_dir)}")
else:
    logger.warning(f"Static directory does not exist at {static_dir}")
    # Try to create it if it doesn't exist
    try:
        os.makedirs(static_dir, exist_ok=True)
        logger.info(f"Created static directory at {static_dir}")
    except Exception as e:
        logger.error(f"Failed to create static directory: {e}")

# Root path handler - serve the React frontend instead of API
@app.get("/")
async def root(request: Request):
    logger.info("Root path requested, serving frontend index.html")
    index_path = os.path.join(static_dir, "index.html")
    
    if os.path.exists(index_path):
        logger.info(f"Serving index.html from {index_path}")
        return FileResponse(index_path)
    else:
        logger.error(f"index.html not found at {index_path}")
        return {"error": "Frontend not found. Please check deployment."}

# API endpoints - moved under /api prefix
@app.get("/api")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/api/items")
def read_items():
    return [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
        {"id": 3, "name": "Item 3"}
    ]

# Health check endpoint for Render
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Mount static files
try:
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info("Successfully mounted static files directory")
except Exception as e:
    logger.error(f"Failed to mount static files directory: {e}")

# Catch-all route for serving the React app
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    logger.info(f"Requested path: {full_path}")
    
    # Don't handle API routes here
    if full_path.startswith("api/"):
        logger.warning(f"API route not found: {full_path}")
        raise HTTPException(status_code=404, detail="API route not found")
    
    # Try to serve the specific file if it exists
    file_path = os.path.join(static_dir, full_path)
    logger.info(f"Looking for file at: {file_path}")
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        logger.info(f"Serving file: {file_path}")
        return FileResponse(file_path)
    
    # Default to serving index.html for client-side routing
    index_path = os.path.join(static_dir, "index.html")
    logger.info(f"Looking for index.html at: {index_path}")
    
    if os.path.exists(index_path):
        logger.info("Serving index.html for client-side routing")
        return FileResponse(index_path)
    
    # If index.html doesn't exist, return detailed error
    logger.error(f"index.html not found at {index_path}")
    raise HTTPException(
        status_code=404, 
        detail=f"Frontend files not found. Make sure React build is in {static_dir}"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))