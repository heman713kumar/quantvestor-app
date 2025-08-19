# shim so 'uvicorn main:app' still works if Railway ignores Procfile
from app.main import app
