# analyzer/analyzer.py
import subprocess
from datetime import datetime
from db.db import get_supabase_client

def get_latest_commit_info():
    """Fetch the latest commit's author, message, and diff."""
    author = subprocess.check_output(
        ["git", "log", "-1", "--pretty=format:%an"], text=True
    ).strip()

    message = subprocess.check_output(
        ["git", "log", "-1", "--pretty=format:%s"], text=True
    ).strip()

    diff = subprocess.check_output(
        ["git", "diff", "HEAD~1", "HEAD"], text=True
    ).strip()

    return author, message, diff

def insert_commit(author, message, diff):
    """Insert commit info into Supabase table gitcommits."""
    supabase = get_supabase_client()
    data = {
        "created_at": datetime.now().isoformat(),
        "author": author,
        "message": message,
        "diff": diff,
        "ai_summary": None  # placeholder for AI summary
    }
    response = supabase.table("gitcommits").insert(data).execute()
    print("Inserted:", response)

if __name__ == "__main__":
    author, message, diff = get_latest_commit_info()
    insert_commit(author, message, diff)
