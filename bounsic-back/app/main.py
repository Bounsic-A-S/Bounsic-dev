import asyncio
import sys
import uvicorn
from app import app, env_host, app_port, debug_mode

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    uvicorn.run(
        "app:app",
        host=env_host,
        port=app_port,
        reload=debug_mode,
        loop="asyncio",
        workers=1
    )