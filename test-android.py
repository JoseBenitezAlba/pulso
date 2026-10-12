import subprocess,time,xml.etree.ElementTree as ET,re,wave,math,struct,os
os.makedirs('build',exist_ok=True)
def adb(*args):return subprocess.check_output(['adb',*args],text=True)
def shell(*args):return adb('shell',*args)
def tree():
 shell('uiautomator','dump','/sdcard/ui.xml');return ET.fromstring(shell('cat','/sdcard/ui.xml'))
def tap(text):
 for _ in range(10):
  nodes=[n for n in tree().iter('node') if n.get('text')==text]
  if nodes:
   b=list(map(int,re.findall(r'\d+',nodes[0].get('bounds'))));shell('input','tap',str((b[0]+b[2])//2),str((b[1]+b[3])//2));time.sleep(1);return
  time.sleep(1)
 raise AssertionError('No aparece: '+text)
def snap(name):shell('screencap','-p','/sdcard/'+name+'.png');adb('pull','/sdcard/'+name+'.png','build/'+name+'.png')
def input_text(text):shell('input','text',text)
shell('wm','size','390x844');shell('wm','density','160')
adb('install','-r','build/pulso.apk');shell('am','start','-n','es.pulso.music/.MainActivity');time.sleep(3);snap('permiso')
shell('pm','grant','es.pulso.music','android.permission.READ_EXTERNAL_STORAGE')
for j in range(2):
 path='build/Prueba'+str(j)+'.wav'
 with wave.open(path,'w') as w:
  w.setparams((1,2,22050,0,'NONE','not compressed'));frame=b''.join(struct.pack('<h',int(7000*math.sin(2*math.pi*(440+j*220)*i/22050))) for i in range(22050));w.writeframes(frame*120)
 adb('push',path,'/sdcard/Music/Prueba'+str(j)+'.wav');shell('am','broadcast','-a','android.intent.action.MEDIA_SCANNER_SCAN_FILE','-d','file:///sdcard/Music/Prueba'+str(j)+'.wav')
time.sleep(4);shell('am','force-stop','es.pulso.music');shell('am','start','-n','es.pulso.music/.MainActivity');time.sleep(3);snap('biblioteca')
shell('input','swipe','40','220','300','220','250');time.sleep(1);tap('+  Crear lista');input_text('MiLista');tap('Crear');snap('listas')
tap('Canciones');tap('+');tap('MiLista');shell('input','swipe','40','220','300','220','250');time.sleep(1);tap('MiLista');snap('detalle-lista')
tap('Prueba0');time.sleep(3);snap('reproductor');state=shell('dumpsys','media_session');assert 'state=3' in state,state
shell('input','keyevent','26');time.sleep(5);state=shell('dumpsys','media_session');assert 'state=3' in state,state
shell('input','keyevent','26');shell('wm','dismiss-keyguard');time.sleep(1)
shell('am','force-stop','es.pulso.music');shell('am','start','-n','es.pulso.music/.MainActivity');time.sleep(2);tap('Listas');tap('MiLista');assert any(n.get('text')=='Prueba0' for n in tree().iter('node'))
errors=adb('logcat','-d','-s','AndroidRuntime');open('build/errors.txt','w').write(errors);assert 'FATAL EXCEPTION' not in errors,errors
print('OK: permiso, biblioteca, gesto, lista, reproducción, pantalla apagada y persistencia')
