import re

def normalize_arabic(text: str) -> str:
    """
    Standardizes Arabic text for robust keyword matching.
    - Normalizes various forms of Alef (أ، إ، آ) to plain Alef (ا)
    - Normalizes Teh Marbuta (ة) to Heh (ه)
    - Normalizes Alef Maqsura (ى) to Yeh (ي)
    - Removes Tashkeel (diacritics)
    - Removes punctuation and extra whitespace
    """
    if not text:
        return ""
    
    # Convert to string and lower (for English parts)
    text = str(text).lower()
    
    # 1. Remove Tashkeel (Diacritics)
    tashkeel_pattern = re.compile(r'[\u064B-\u0652]')
    text = re.sub(tashkeel_pattern, '', text)
    
    # 2. Normalize Alef forms
    text = re.sub(r'[أإآ]', 'ا', text)
    
    # 3. Normalize Teh Marbuta
    text = re.sub(r'ة', 'ه', text)
    
    # 4. Normalize Alef Maqsura
    text = re.sub(r'ى', 'ي', text)
    
    # 5. Remove punctuation and special characters (keep spaces and alphanumeric)
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # 6. Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def contains_arabic(text: str) -> bool:
    """Returns True if the text contains any Arabic characters."""
    return bool(re.search(r'[\u0600-\u06FF]', text))
