from imp import reload
import uvicorn
host = "127.0.0.1"
port = 8000

if __name__ == "__main__":
    uvicorn.run("api.app:app", host=host, port=port, reload=True)
