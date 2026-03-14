
import os
import sys
from app.core.config import supabase

# Mock Company Clients (The "Data Provided by Company")
MOCK_CLIENTS = [
    {
        "email": "sarah@partner-company.com",
        "name": "Sarah Connor",
        "role": "Lead",
        "department": "External",
        "metadata": {
             "company": "Cyberdyne Systems",
             "position": "Operations Manager",
             "vip_status": True
        }
    },
    {
        "email": "john@tech-corp.com",
        "name": "John Wick",
        "role": "Lead",
        "department": "External", 
        "metadata": {
             "company": "Continental Services",
             "position": "Security Consultant", 
             "vip_status": True
        }
    },
    {
        "email": "amira@startups-inc.eg",
        "name": "Amira Ali",
        "role": "Lead",
        "department": "External",
        "metadata": {
             "company": "Cairo Startups",
             "position": "HR Director",
             "vip_status": False
        }
    }
]

def seed_users():
    print("--- SEEDING USERS ---")
    for client in MOCK_CLIENTS:
        try:
            # Check if exists
            res = supabase.table("users").select("id").eq("email", client["email"]).execute()
            if not res.data:
                print(f"Creating user: {client['email']}")
                user_data = {
                    "email": client["email"],
                    "name": client["name"],
                    "metadata": client["metadata"]
                }
                supabase.table("users").insert(user_data).execute()
            else:
                print(f"User exists: {client['email']}")
        except Exception as e:
            print(f"Error seeding {client['email']}: {e}")
    print("--- SEEDING COMPLETE ---")

if __name__ == "__main__":
    seed_users()
