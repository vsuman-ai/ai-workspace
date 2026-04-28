import uvicorn
from ai.sentiment.src.app.server import app

def run_app_parser():
    # Start Uvicorn
    # Since we've already modified the 'container' object in this process,
    # we pass the actual 'app' object or the string path.
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3000,
        timeout_keep_alive=60,
        log_level="debug",
    )