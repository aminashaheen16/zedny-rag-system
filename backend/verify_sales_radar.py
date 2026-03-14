import sys
import os
import asyncio

# Fix Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_service import AIService

async def test_sales_radar():
    print("\n[TEST] TEST 2: Passive Sales Radar (B2B Intent)")
    
    scenarios = [
        "عايز ادرب الموظفين عندي في الشركة",
        "I have a team of 50 people needing soft skills",
        "My password is not working",
        "How much is the subscription for individuals?",
        "عرض سعر للمؤسسات"
    ]
    
    for i, msg in enumerate(scenarios):
        is_b2b = AIService.detect_b2b_intent(msg)
        status = "[B2B]" if is_b2b else "[Individual]"
        print(f"   Scenario #{i+1}: {status}")

if __name__ == "__main__":
    asyncio.run(test_sales_radar())
