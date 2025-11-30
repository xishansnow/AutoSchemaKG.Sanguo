"""
Test UMLS API Connection
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file)
    print(f"✓ Loaded .env from {env_file}")
else:
    print(f"⚠ No .env file found")

from pipeline.umls_loader import UMLSLoader

print("\n" + "=" * 80)
print("UMLS API VALIDATION TEST")
print("=" * 80 + "\n")

# Check if UMLS_API_KEY is set
api_key = os.getenv("UMLS_API_KEY", "").strip()
print(f"1. Checking UMLS_API_KEY environment variable...")
if api_key:
    print(f"   ✓ UMLS_API_KEY found: {api_key[:10]}...{api_key[-5:]}")
else:
    print(f"   ✗ UMLS_API_KEY not set in .env file")
    print(f"\n   To fix this:")
    print(f"   1. Go to https://www.nlm.nih.gov/research/umls/")
    print(f"   2. Create free account")
    print(f"   3. Generate API key")
    print(f"   4. Add to .env: UMLS_API_KEY=your_key_here")
    exit(1)

# Initialize UMLS loader
print(f"\n2. Initializing UMLS loader...")
try:
    umls = UMLSLoader(api_key=api_key)
    
    if umls.is_available():
        print(f"   ✓ UMLS API is authenticated and ready!")
    else:
        print(f"   ✗ UMLS API authentication failed")
        print(f"   This usually means:")
        print(f"   - API key is invalid or expired")
        print(f"   - Network connection issue")
        exit(1)
        
except Exception as e:
    print(f"   ✗ Error initializing UMLS: {e}")
    exit(1)

# Test search
print(f"\n3. Testing UMLS search functionality...")
test_terms = ["Metformin", "Type 2 Diabetes", "Hypertension", "Aspirin"]

for term in test_terms:
    try:
        results = umls.search_concept(term)
        if results:
            best = results[0]
            print(f"   ✓ '{term}'")
            print(f"      → UMLS ID: {best['umls_id']}")
            print(f"      → Name: {best['name']}")
            print(f"      → Source: {best['source']}")
            print(f"      → Score: {best['score']:.2f}")
        else:
            print(f"   ⚠ '{term}' - No results found")
    except Exception as e:
        print(f"   ✗ '{term}' - Error: {str(e)[:50]}")

print(f"\n" + "=" * 80)
print("✓ UMLS API validation complete!")
print("=" * 80 + "\n")