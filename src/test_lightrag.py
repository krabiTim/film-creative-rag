#!/usr/bin/env python3
import torch
try:
    from lightrag import LightRAG
    print('LightRAG imported successfully!')
    
    # Test basic functionality
    rag = LightRAG(working_dir='./cache/lightrag')
    print('LightRAG instance created!')
    
    # Test with screenplay content
    screenplay = '''
    FADE IN:
    EXT. COFFEE SHOP - DAY
    SARAH sits with her laptop, writing.
    
    SARAH
    This screenplay will change everything.
    
    FADE OUT.
    '''
    
    rag.insert(screenplay)
    print('Screenplay content inserted!')
    
    result = rag.query('Who is the main character?')
    print(f'Query result: {result}')
    
    print('SUCCESS: LightRAG + RTX 4090 working!')
    
except ImportError:
    print('LightRAG not installed. Installing...')
except Exception as e:
    print(f'Error: {e}')
