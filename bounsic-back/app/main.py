import uvicorn
from app import app, env_host, app_port, debug_mode  


if __name__ == "__main__":
    uvicorn.run("app:app", host=env_host, port=app_port, reload=debug_mode)
