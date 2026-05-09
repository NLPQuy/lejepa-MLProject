#!/usr/bin/env python3
"""Quick check of imagenet-hf parquet format."""
import pyarrow.parquet as pq

f = '/workspace/imagenet-hf/data/train-00000-of-00294.parquet'
t = pq.read_table(f)
print('Schema:', t.schema)
print('Rows in shard 0:', len(t))

row0 = t.slice(0, 1).to_pydict()
img = row0['image'][0]
print('Image type:', type(img))
if isinstance(img, dict):
    print('Image keys:', list(img.keys()))
    b = img.get('bytes')
    if b:
        print('Bytes len:', len(b))
        # Try to open as PIL
        from PIL import Image
        import io
        pil = Image.open(io.BytesIO(b))
        print('PIL image:', pil.size, pil.mode)
print('Label:', row0['label'][0])
