# lets 'uvicorn main:app' still work if some platform ignores the Procfile
from app.main import app
