import os, glob

files = glob.glob('*.html')
for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    # Bajar volumen de melodía de 0.08 a 0.03 y bajo de 0.06 a 0.02
    content = content.replace("'square',0.08,a)", "'square',0.03,a)")
    content = content.replace("'triangle',0.06,a)", "'triangle',0.02,a)")
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"OK: {fname}")

