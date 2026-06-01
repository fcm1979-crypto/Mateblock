import os

MUSIC_JS = """
<!-- MUSICA MATEBLOCKS -->
<script>
(function(){
  var ac = null, playing = false, nodes = [], scheduleTimer = null;
  var started = false;
  var C4=261.6,D4=293.7,E4=329.6,F4=349.2,G4=392,A4=440,B4=493.9;
  var C5=523.3,D5=587.3,E5=659.3,G5=784,A5=880,F5=698.5;
  var R=0;
  var MELODY = [
    [E5,0.12],[E5,0.12],[R,0.06],[E5,0.12],[R,0.06],[C5,0.12],[E5,0.18],
    [G5,0.18],[R,0.18],[G4,0.18],[R,0.18],
    [C5,0.18],[R,0.12],[G4,0.18],[R,0.12],[E4,0.18],
    [R,0.12],[A4,0.15],[B4,0.15],[R,0.06],[A4,0.12],
    [G4,0.12],[E5,0.12],[G5,0.12],[A5,0.15],[F5,0.12],[G5,0.12],
    [R,0.06],[E5,0.15],[C5,0.12],[D5,0.12],[B4,0.18],[R,0.12]
  ];
  var BASS = [
    [C4,0.18],[R,0.06],[G4,0.12],[R,0.06],[E4,0.12],[R,0.18],
    [A4,0.15],[R,0.09],[B4,0.12],[R,0.06],[G4,0.15],[R,0.09],
    [C4,0.18],[R,0.06],[G4,0.12],[R,0.06],[E4,0.12],[R,0.18],
    [F4,0.15],[R,0.09],[G4,0.12],[R,0.06],[A4,0.15],[R,0.09]
  ];
  function getAC(){ if(!ac) ac=new(window.AudioContext||window.webkitAudioContext)(); return ac; }
  function playNote(freq,duration,startTime,type,gainVal,a){
    if(freq===0) return;
    var o=a.createOscillator(),g=a.createGain(),f=a.createBiquadFilter();
    f.type='lowpass';f.frequency.value=2000;
    o.connect(f);f.connect(g);g.connect(a.destination);
    o.type=type;o.frequency.setValueAtTime(freq,startTime);
    g.gain.setValueAtTime(0.001,startTime);
    g.gain.linearRampToValueAtTime(gainVal,startTime+0.01);
    g.gain.setValueAtTime(gainVal,startTime+duration*0.7);
    g.gain.exponentialRampToValueAtTime(0.001,startTime+duration*0.95);
    o.start(startTime);o.stop(startTime+duration);nodes.push(o);
  }
  function scheduleLoop(startTime){
    if(!playing) return;
    var a=getAC(),t=startTime,loopDur=0;
    MELODY.forEach(function(n){ playNote(n[0],n[1],t,'square',0.08,a);t+=n[1];loopDur+=n[1]; });
    var tb=startTime;
    BASS.forEach(function(n){ playNote(n[0],n[1],tb,'triangle',0.06,a);tb+=n[1]; });
    scheduleTimer=setTimeout(function(){ scheduleLoop(startTime+loopDur); },(loopDur-0.3)*1000);
  }
  function startMusic(){
    if(playing) return;
    playing=true;
    var a=getAC();
    if(a.state==='suspended') a.resume();
    scheduleLoop(a.currentTime+0.05);
  }
  function stopMusic(){
    playing=false;
    if(scheduleTimer) clearTimeout(scheduleTimer);
    nodes.forEach(function(n){try{n.stop();}catch(e){}});nodes=[];
  }
  function onFirstTouch(){
    if(started) return;
    started=true;
    startMusic();
    document.removeEventListener('touchstart',onFirstTouch);
    document.removeEventListener('mousedown',onFirstTouch);
  }
  document.addEventListener('touchstart',onFirstTouch,{passive:true});
  document.addEventListener('mousedown',onFirstTouch);
  document.addEventListener('visibilitychange',function(){ if(document.hidden){stopMusic();started=false;} });
  window.MB=window.MB||{};
  window.MB.stopMusic=stopMusic;
  window.MB.startMusic=startMusic;
})();
</script>
"""

targets = [
  'index.html','decimales-mateblocks.html','division-mateblocks.html',
  'fracciones-mateblocks.html','monedas-mateblocks.html','reloj-mateblocks.html',
  'restas-llevadas-mateblocks.html','romanos-mateblocks.html',
  'sumas-llevadas-mateblocks.html','tablas-mateblocks.html','valor-posicional-mateblocks.html',
]

for fname in targets:
    if not os.path.exists(fname):
        print(f"NO ENCONTRADO: {fname}"); continue
    with open(fname,'r',encoding='utf-8') as f: content=f.read()
    if 'MUSICA MATEBLOCKS' in content:
        print(f"YA TIENE: {fname}"); continue
    content=content.replace('</body>', MUSIC_JS+'</body>',1)
    with open(fname,'w',encoding='utf-8') as f: f.write(content)
    print(f"OK: {fname}")

print("\nAhora ejecuta:")
print("  git add .")
print('  git commit -m "Añadir musica chiptune"')
print("  git push")
