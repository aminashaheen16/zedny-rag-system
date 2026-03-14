import requests
import uuid

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("🧪 TECHNICAL AI EXPERT VALIDATION TEST SUITE")
print("Testing Llama 3.3 70B Technical Diagnostic Capabilities")
print("=" * 60)

def test_video_playback_black_screen():
    print("\n--- [TEST 1] Video Black Screen (No Controls) ---")
    payload = {
        "message": "الفيديو أسود خالص ومش ظاهر أي حاجة، حتى الكونترولز مش شغالة",
        "user_email": "tech_test@zedny.ai",
        "incident_state": {
            "session_id": str(uuid.uuid4()),
            "status": "diagnosing",
            "step": 1,
            "problem_description": "شاشة سوداء بدون كونترولز",
            "solutions_tried": [],
            "diagnostic_turns": 1
        }
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", "")
        
        # Check for advanced diagnostics
        has_drm_solution = any(k in answer.lower() for k in ["drm", "widevine", "chrome://components"])
        has_cache_solution = any(k in answer.lower() for k in ["ctrl+shift+r", "hard refresh", "كاش"])
        
        if has_drm_solution or has_cache_solution:
            print("✅ PASS: AI provided advanced DRM/Cache diagnostics")
            print(f"   Answer: {answer[:200]}...")
        else:
            print("⚠️  WARNING: AI solution may be too generic")
            print(f"   Answer: {answer[:200]}...")
    else:
        print(f"❌ FAILED: {response.text}")

def test_buffering_stable_internet():
    print("\n--- [TEST 2] Buffering on Stable Internet ---")
    payload = {
        "message": "الفيديو بيعمل buffering كتير بالرغم إن النت عندي سريع",
        "user_email": "tech_test2@zedny.ai",
        "incident_state": {
            "session_id": str(uuid.uuid4()),
            "status": "diagnosing",
            "step": 1,
            "problem_description": "buffering مع نت سريع",
            "solutions_tried": [],
            "diagnostic_turns": 1
        }
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", "")
        
        # Check for CDN/adaptive bitrate diagnostics
        has_cdn_awareness = any(k in answer.lower() for k in ["cdn", "bitrate", "adaptive", "quality"])
        has_speedtest = "speedtest" in answer.lower()
        
        if has_cdn_awareness or has_speedtest:
            print("✅ PASS: AI diagnosed CDN/adaptive bitrate issue")
            print(f"   Answer: {answer[:200]}...")
        else:
            print("⚠️  WARNING: Missing CDN diagnosis")
            print(f"   Answer: {answer[:200]}...")
    else:
        print(f"❌ FAILED: {response.text}")

def test_no_sound_all_browsers():
    print("\n--- [TEST 3] No Sound Across All Browsers ---")
    payload = {
        "message": "الصوت مش شغال خالص في كل المتصفحات، جربت Chrome و Firefox نفس المشكلة",
        "user_email": "tech_test3@zedny.ai",
        "incident_state": {
            "session_id": str(uuid.uuid4()),
            "status": "diagnosing",
            "step": 1,
            "problem_description": "صوت لا يعمل في جميع المتصفحات",
            "solutions_tried": [],
            "diagnostic_turns": 1
        }
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", "")
        
        # Should recognize this is hardware/driver issue, not browser
        has_hardware_diagnosis = any(k in answer.lower() for k in ["hardware", "driver", "audio driver", "youtube", "test"])
        
        if has_hardware_diagnosis:
            print("✅ PASS: AI correctly identified hardware/driver issue")
            print(f"   Answer: {answer[:200]}...")
        else:
            print("⚠️  WARNING: May not have identified root cause")
            print(f"   Answer: {answer[:200]}...")
    else:
        print(f"❌ FAILED: {response.text}")

def test_login_keeps_failing():
    print("\n--- [TEST 4] Login Keeps Failing (Cookies Issue) ---")
    payload = {
        "message": "مش قادر أدخل الحساب، كل مرة يقولي wrong password بالرغم إني متأكد منها",
        "user_email": "tech_test4@zedny.ai",
        "incident_state": {
            "session_id": str(uuid.uuid4()),
            "status": "diagnosing",
            "step": 1,
            "problem_description": "فشل تسجيل الدخول المتكرر",
            "solutions_tried": [],
            "diagnostic_turns": 1
        }
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", "")
        
        # Should suggest cookies/cache/caps lock checks
        has_cookie_solution = any(k in answer.lower() for k in ["cookie", "كوكيز", "cache", "كاش"])
        has_caps_check = any(k in answer.lower() for k in ["caps lock", "shift"])
        
        if has_cookie_solution or has_caps_check:
            print("✅ PASS: AI provided systematic login diagnostics")
            print(f"   Answer: {answer[:200]}...")
        else:
            print("⚠️  WARNING: Missing standard login checks")
            print(f"   Answer: {answer[:200]}...")
    else:
        print(f"❌ FAILED: {response.text}")

def test_connection_timeout():
    print("\n--- [TEST 5] Connection Timeout Error ---")
    payload = {
        "message": "بيجيلي ERR_TIMED_OUT وأنا بفتح المنصة",
        "user_email": "tech_test5@zedny.ai",
        "incident_state": {
            "session_id": str(uuid.uuid4()),
            "status": "diagnosing",
            "step": 1,
            "problem_description": "ERR_TIMED_OUT عند الوصول للمنصة",
            "solutions_tried": [],
            "diagnostic_turns": 1
        }
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", "")
        
        # Should suggest DNS/firewall checks
        has_dns_solution = any(k in answer.lower() for k in ["dns", "8.8.8.8", "1.1.1.1"])
        has_firewall_check = any(k in answer.lower() for k in ["firewall", "antivirus", "vpn"])
        
        if has_dns_solution or has_firewall_check:
            print("✅ PASS: AI diagnosed network/DNS issue correctly")
            print(f"   Answer: {answer[:200]}...")
        else:
            print("⚠️  WARNING: Missing network diagnostics")
            print(f"   Answer: {answer[:200]}...")
    else:
        print(f"❌ FAILED: {response.text}")

if __name__ == "__main__":
    print("\n🔬 Starting Technical Diagnostic Tests...\n")
    
    try:
        test_video_playback_black_screen()
        test_buffering_stable_internet()
        test_no_sound_all_browsers()
        test_login_keeps_failing()
        test_connection_timeout()
        
        print("\n" + "=" * 60)
        print("✨ Technical AI Expert Test Suite Complete!")
        print("=" * 60)
    except Exception as e:
        print(f"💥 Error running tests: {e}")
