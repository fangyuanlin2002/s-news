from mangum import Mangum
from backend.main import app  # Adjust path based on your structure

handler = Mangum(app)