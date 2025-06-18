import torch
print('Testing RTX 4090...')
print(f'GPU: {torch.cuda.get_device_name(0)}')
print(f'CUDA Available: {torch.cuda.is_available()}')

print('Testing LightRAG import...')
try:
    from lightrag import LightRAG
    print('SUCCESS: LightRAG imported!')
    
    rag = LightRAG(working_dir='./cache')
    print('SUCCESS: LightRAG instance created!')
    
    rag.insert('SARAH is a filmmaker working on a screenplay.')
    result = rag.query('Who is Sarah?')
    print(f'Query result: {result}')
    
    print('EVERYTHING WORKING!')
except Exception as e:
    print(f'Error: {e}')
