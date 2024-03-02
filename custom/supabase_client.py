import os
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()

def get_supabase_client():
    """Initialize and return a Supabase client."""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and key must be provided via environment variables.")

    return create_client(supabase_url, supabase_key)
