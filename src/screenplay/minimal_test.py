#!/usr/bin/env python3
"""
Minimal LightRAG Test - Film Creative RAG
"""
print("=== MINIMAL SYSTEM TEST ===")

# Test 1: Basic imports
try:
    from lightrag import LightRAG
    print("âœ“ LightRAG import: SUCCESS")
except Exception as e:
    print(f"âœ— LightRAG import: FAILED - {e}")

try:
    import torch
    gpu_available = torch.cuda.is_available()
    print(f"âœ“ GPU status: {'AVAILABLE' if gpu_available else 'NOT AVAILABLE'}")
except Exception as e:
    print(f"âœ— GPU test: FAILED - {e}")

# Test 2: Check our screenplay engine
try:
    from screenplay_engine import ScreenplayIntelligence
    engine = ScreenplayIntelligence()
    print("âœ“ Screenplay engine: SUCCESS")
except Exception as e:
    print(f"âœ— Screenplay engine: FAILED - {e}")

# Test 3: Simple analysis
test_script = """
FADE IN:

INT. TEST ROOM - DAY

ALICE works at computer.

ALICE
This is a test.

FADE OUT.
"""

try:
    if 'engine' in locals():
        result = engine.analyze_screenplay(test_script, "Simple Test")
        chars = result.get('characters', {}).get('character_list', [])
        print(f"âœ“ Analysis test: SUCCESS - Found characters: {chars}")
    else:
        print("âœ— Analysis test: SKIPPED - No engine")
except Exception as e:
    print(f"âœ— Analysis test: FAILED - {e}")

print("\n=== TEST COMPLETE ===")
print("If you see âœ“ marks above, those components are working!")
print("Any âœ— marks show what needs attention.")
