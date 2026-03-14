import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(name, path, method="GET", payload=None):
    print(f"\n--- Testing {name} [{method} {path}] ---")
    try:
        url = f"{BASE_URL}{path}"
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Success (200)")
            data = response.json()
            if isinstance(data, list):
                print(f"Items count: {len(data)}")
                if len(data) > 0:
                    print(f"First item keys: {list(data[0].keys())}")
            elif isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
                if 'kpis' in data:
                    print(f"KPIs: {[k['label'] + ': ' + str(k['value']) for k in data['kpis']]}")
            return data
        else:
            print(f"❌ Failed (Status: {response.status_code})")
            print(response.text)
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    # 1. Test Stats
    stats = test_endpoint("Stats API", "/stats")
    
    # 2. Test Reports list
    reports = test_endpoint("Reports List", "/reports")
    
    # 3. Test Ratings list
    ratings = test_endpoint("Ratings List", "/ratings")
    
    # 4. Try fetching a specific report if available
    if reports and len(reports) > 0:
        report_id = reports[0]['id']
        test_endpoint(f"Report Details ({report_id})", f"/reports/{report_id}?role=admin")

    print("\n--- Test Finished ---")
