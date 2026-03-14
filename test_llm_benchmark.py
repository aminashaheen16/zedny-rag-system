"""
📊 ZEDNY LLM PERFORMANCE BENCHMARK
Compares different models via OpenRouter on Latency, Quality, and Arabic Fluency.
"""

import sys
import os
import time
import requests
from typing import List, Dict

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from backend.app.services.ai_service import AIService

# Models to compare
MODELS_TO_TEST = [
    "anthropic/claude-3.5-sonnet",
    "google/gemini-2.0-flash-exp:free",
    "deepseek/deepseek-chat",
    "meta-llama/llama-3.3-70b-instruct",
    "llama-3.3-70b-versatile" # Groq fallback
]

# Test cases (Targeting Info, Issue, and Arabic nuances)
TEST_CASES = [
    {
        "name": "Identity/Intro",
        "msg": "مين زدني؟",
        "prompt": "You are Zedny Assistant. Answer briefly in Arabic."
    },
    {
        "name": "Complex Sales",
        "msg": "إيه الفرق بين باقة الأفراد والشركات في زدني؟",
        "prompt": "You are a professional Sales Agent. Answer in Arabic."
    },
    {
        "name": "Vague Issue (Guard Test)",
        "msg": "مش عارف أدخل",
        "prompt": "You are a Tech Support bot. Analyze why the user can't login."
    }
]

def benchmark_model(model_path: str):
    print(f"\n--- 🚀 Testing Model: {model_path} ---")
    results = []
    
    for case in TEST_CASES:
        start_time = time.time()
        try:
            # Force this specific model by passing it as the 'model' parameter
            response = AIService.run_llm(case["prompt"], case["msg"], model=model_path, timeout=40)
            end_time = time.time()
            
            latency = end_time - start_time
            
            # Basic analysis of response
            is_fallback = "عذراً، نواجه ضغطاً تقنياً" in response
            status = "✅ SUCCESS" if not is_fallback else "⚠️ FALLBACK"
            
            print(f"   [{case['name']}] -> {status} ({latency:.2f}s)")
            
            results.append({
                "case": case["name"],
                "latency": latency,
                "status": status,
                "response": response[:100] + "..." if len(response) > 100 else response
            })
            
        except Exception as e:
            print(f"   [{case['name']}] -> ❌ ERROR: {e}")
            results.append({
                "case": case["name"],
                "latency": 0,
                "status": "ERROR",
                "response": str(e)
            })
            
    return results

def run_benchmark():
    print("="*80)
    print("📊 ZEDNY LLM PERFORMANCE & QUALITY BENCHMARK")
    print("="*80)
    
    summary = {}
    
    for model in MODELS_TO_TEST:
        summary[model] = benchmark_model(model)
        # Small sleep to be polite to APIs
        time.sleep(1)
        
    print("\n" + "="*80)
    print("📈 FINAL SUMMARY REPORT")
    print("="*80)
    
    header = f"{'Model':<40} | {'Avg Latency':<12} | {'Success Rate'}"
    print(header)
    print("-" * len(header))
    
    for model, results in summary.items():
        success_count = sum(1 for r in results if r["status"] == "✅ SUCCESS")
        avg_latency = sum(r["latency"] for r in results) / len(results) if results else 0
        rate = f"{success_count}/{len(results)}"
        print(f"{model:<40} | {avg_latency:<12.2f}s | {rate}")

if __name__ == "__main__":
    run_benchmark()
