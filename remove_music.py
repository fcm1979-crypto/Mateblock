import re, glob

for fname in glob.glob('*.html'):
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    # Eliminar bloque de música completo
    content = re.sub(r'\n<!-- MUSICA MATEBLOCKS -->.*?</script>', '', content, flags=re.DOTALL)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"OK: {fname}")
