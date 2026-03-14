
import re

def clean_ai_response(text: str) -> str:
    if not text:
        return ""
    
    # 1. Remove Markdown JSON blocks
    text = re.sub(r'```json\s*[\s\S]*?```', '', text)
    text = re.sub(r'```[\s\S]*?```', '', text) 
    
    # 2. Remove internal logic markers
    forbidden_patterns = [
        r'\{"INTENT":.*\}', 
        r'\{"worked":.*\}',
        r'INTENT:.*',
        r'LENGTH_RULE:.*',
        r'### 🌍 LANGUAGE RULE:.*'
    ]
    for pattern in forbidden_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
    return text.strip()

# Test Cases
test_leak_1 = """```json
{
  "INTENT": "FEATURE",
  "LENGTH_RULE": "3 bullets MAX"
}
```
Welcome to Zedny! We offer training."""

test_leak_2 = """INTENT: SALES
### 🌍 LANGUAGE RULE: Respond ONLY in Arabic.
أهلاً بك في زدني، نحن نقدم أفضل الدورات."""

print(f"Test 1 Results:\n'{clean_ai_response(test_leak_1)}'")
print(f"\nTest 2 Results:\n'{clean_ai_response(test_leak_2)}'")
