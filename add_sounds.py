import os, re

SOUND_JS = """
<!-- SONIDOS MATEBLOCKS -->
<script>
(function(){
  window.MB = window.MB || {};
  var ctx = null;
  function getCtx(){
    if(!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    return ctx;
  }
  function playTone(freq, type, start, duration, gainVal, ac){
    var o = ac.createOscillator();
    var g = ac.createGain();
    o.connect(g); g.connect(ac.destination);
    o.type = type; o.frequency.setValueAtTime(freq, start);
    g.gain.setValueAtTime(gainVal, start);
    g.gain.exponentialRampToValueAtTime(0.001, start + duration);
    o.start(start); o.stop(start + duration);
  }
  window.MB.soundOk = function(){
    try {
      var ac = getCtx();
      var t = ac.currentTime;
      // Acorde alegre ascendente: do-mi-sol
      playTone(523, 'sine', t,      0.18, 0.4, ac);
      playTone(659, 'sine', t+0.1,  0.18, 0.35, ac);
      playTone(784, 'sine', t+0.2,  0.28, 0.35, ac);
      // Brillo encima
      playTone(1047,'sine', t+0.22, 0.22, 0.18, ac);
    } catch(e){}
  };
  window.MB.soundErr = function(){
    try {
      var ac = getCtx();
      var t = ac.currentTime;
      // Dos notas graves descendentes
      playTone(220, 'sawtooth', t,      0.18, 0.3, ac);
      playTone(180, 'sawtooth', t+0.15, 0.25, 0.25, ac);
    } catch(e){}
  };
})();
</script>
"""

# Archivos a procesar
targets = [
    'decimales-mateblocks.html',
    'division-mateblocks.html',
    'fracciones-mateblocks.html',
    'monedas-mateblocks.html',
    'reloj-mateblocks.html',
    'restas-llevadas-mateblocks.html',
    'romanos-mateblocks.html',
    'sumas-llevadas-mateblocks.html',
    'tablas-mateblocks.html',
    'valor-posicional-mateblocks.html',
]

# Patrones de celebrate() en cada archivo → añadir MB.soundOk()
# Patrones de feedback wrong/error → añadir MB.soundErr()

def inject_sounds(content):
    # 1. Inyectar el bloque de sonido antes de </body>
    if 'window.MB.soundOk' in content:
        print("  → Sonidos ya presentes, omitiendo inyección de script")
    else:
        content = content.replace('</body>', SOUND_JS + '</body>', 1)

    # 2. Añadir MB.soundOk() justo después de cada llamada a celebrate()
    #    pero solo si no está ya
    content = re.sub(
        r'celebrate\(\);(?!\s*window\.MB\.soundOk)',
        'celebrate(); window.MB.soundOk();',
        content
    )

    # 3. Patrones de error/wrong feedback → añadir soundErr
    # Buscamos asignaciones de clase 'wrong' o 'err' seguidas de punto y coma
    # Patrón: fb.className = 'feedback wrong'; o className='feedback err';
    content = re.sub(
        r"(fb\.className\s*=\s*['\"]feedback (?:wrong|err)['\"];)(?!\s*window\.MB\.soundErr)",
        r'\1 window.MB.soundErr();',
        content
    )
    # También: classList.add('wrong') seguido de ;
    content = re.sub(
        r"(\.classList\.add\(['\"]wrong['\"]\);)(?!\s*window\.MB\.soundErr)",
        r'\1 window.MB.soundErr();',
        content
    )

    return content

# Procesar cada archivo
for fname in targets:
    if not os.path.exists(fname):
        print(f"NO ENCONTRADO: {fname}")
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = inject_sounds(content)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"OK: {fname}")

print("\nListo. Ahora ejecuta:")
print("  git add .")
print('  git commit -m "Añadir sonidos acierto/error a todos los módulos"')
print("  git push")
