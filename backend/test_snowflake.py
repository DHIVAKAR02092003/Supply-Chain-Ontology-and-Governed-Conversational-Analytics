import sys
import os

# Add the backend directory to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.snowflake_service import execute_scalar
from app.core.config import get_settings
from dotenv import load_dotenv

load_dotenv()

def test_query():
    query = "SELECT COUNT(DISTINCT PO_NUMBER) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA"
    try:
        val = execute_scalar(query)
        print(f"Result: {val}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(f"Account: {get_settings().snowflake_account}")
    test_query()
