# La música debe estar en index.html directamente, ya está.
# El problema es que la consola apunta al iframe, no al index.
# Verificamos que index.html tiene el script
with open('index.html', 'r') as f:
    content = f.read()
if 'MUSICA MATEBLOCKS' in content:
    print("OK - index.html tiene la música")
else:
    print("FALTA - index.html no tiene la música")
