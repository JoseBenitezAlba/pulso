# Compilar Pulso desde cero

Guía para alguien que **nunca ha compilado una app de Android**. Al final tendrás tu propio `pulso.apk` instalado en el móvil. Tiempo aproximado: 30-40 minutos, casi todo esperando descargas.

## Qué necesitas

- Un ordenador con **Linux (Ubuntu)**, **macOS** o **Windows 10/11** (en Windows se usa WSL, ver más abajo).
- Unos 3 GB libres y conexión a internet.
- Un móvil con Android 8.0 o posterior.

No hace falta Android Studio. Pulso se compila con herramientas de línea de comandos.

## Qué vamos a instalar (y para qué)

| Herramienta | Para qué sirve |
|---|---|
| JDK 17 (Java) | Compila el código `.java` |
| Android SDK + build-tools 35 | Convierte el código en una app de Android (`aapt2`, `d8`, `zipalign`, `apksigner`) |
| Una clave de firma | Android solo instala apps firmadas; la creas tú una vez |
| `git`, `zip` | Descargar el código y empaquetar el APK |

## Solo en Windows: instalar WSL

`build.sh` es un script de Linux, así que en Windows se trabaja dentro de **Ubuntu en WSL**.

1. Abre PowerShell como administrador (clic derecho en el menú Inicio).
2. Escribe `wsl --install -d Ubuntu` y pulsa Enter.
3. Reinicia el ordenador cuando lo pida y crea un usuario y contraseña de Ubuntu.
4. Abre "Ubuntu" desde el menú Inicio. Esa ventana es tu terminal.
5. Trabaja siempre dentro de tu carpeta personal de Ubuntu (`cd ~`), **no** en `/mnt/c/...`. Si no, aparecen errores raros de finales de línea.

Desde aquí, el resto de pasos son los de Linux.

## Pasos

### 1. Instala Java, git y zip

Ubuntu / WSL:

```
sudo apt update
sudo apt install -y openjdk-17-jdk git zip unzip curl
```

macOS: instala **Temurin 17** desde https://adoptium.net (el instalador `.pkg`). `git` y `zip` ya vienen con el sistema (si pide instalar las "command line developer tools", acepta).

Comprueba que funciona:

```
java -version
javac -version
```

Los dos deben decir `17`. Si `javac` no se encuentra, Java no está bien instalado.

### 2. Descarga el código

```
cd ~
git clone https://github.com/JoseBenitezAlba/pulso.git
cd pulso
```

### 3. Instala el Android SDK

1. Entra en https://developer.android.com/studio#command-line-tools-only y descarga **Command line tools only** para tu sistema (Linux o Mac). En WSL puedes copiar el enlace de Linux y bajarlo con `curl -O <enlace>`.
2. Prepara la carpeta (el script espera el SDK en `~/android`) y descomprime:

```
mkdir -p ~/android/cmdline-tools
cd ~/android/cmdline-tools
unzip ~/Downloads/commandlinetools-*_latest.zip
mv cmdline-tools latest
cd ~/pulso
```

Si bajaste el zip con `curl` en otra carpeta, cambia `~/Downloads` por esa carpeta.

3. Acepta las licencias e instala lo necesario:

```
export ANDROID_HOME=$HOME/android
yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "platforms;android-35" "build-tools;35.0.0"
```

Comprueba que existe `~/android/build-tools/35.0.0`:

```
ls ~/android/build-tools
```

### 4. Crea tu clave de firma

Es un archivo que identifica "quién publica" la app. Se crea una sola vez.

```
mkdir -p build
keytool -genkeypair -keystore build/pulso.jks -alias pulso -keyalg RSA -keysize 2048 -validity 10000 -storepass android -keypass android -dname "CN=Pulso"
```

Importante:

- **No subas `pulso.jks` a internet** (el repositorio ya lo ignora) y **guarda una copia**. Si lo pierdes, no podrás actualizar la app instalada sin desinstalarla antes, y se pierden las listas.
- Para aprender, la contraseña `android` vale. Si usas otra, díselo a `build.sh` con `export PULSO_KS_PASS=tu_contraseña` antes del paso 5 (y cambia `-storepass` y `-keypass` en el comando de arriba).

### 5. Compila

```
export ANDROID_HOME=$HOME/android
bash build.sh
```

Si todo va bien, la última parte de la salida empieza por `Verifies` y se crea `build/pulso.apk`. Si sale un error en rojo antes, mira la tabla de problemas más abajo.

### 6. Instala en el móvil

**Opción A, sin cable:** pásate `build/pulso.apk` al móvil (Telegram, correo, Drive, cable USB como almacenamiento...), ábrelo y acepta "Instalar apps desconocidas" para la app desde la que lo abres.

Desde WSL, para sacarlo a Windows: `cp build/pulso.apk /mnt/c/Users/TU_USUARIO/Downloads/`.

**Opción B, con cable (`adb`):**

1. En el móvil, activa las **opciones de desarrollador**: Ajustes > Acerca del teléfono > pulsa 7 veces en "Versión" (en Xiaomi, en la versión de MIUI o HyperOS).
2. Dentro de opciones de desarrollador, activa **Depuración USB** (y en Xiaomi también "Instalar vía USB").
3. En el ordenador: `sudo apt install -y adb`. En WSL, usa mejor la opción A.
4. Conecta el móvil, acepta el aviso de "Permitir depuración" y ejecuta:

```
adb devices
adb install -r build/pulso.apk
```

**Si ya tenías Pulso instalado** con otra clave de firma, Android responderá "App no instalada" o `INSTALL_FAILED_UPDATE_INCOMPATIBLE`. Habría que desinstalar la anterior primero, y **se pierden tus listas**, favoritos y reproducciones. Haz esto solo si lo tienes claro.

### 7. Pruébala

1. Abre Pulso y pulsa "Elegir mi música" para dar el permiso de audio.
2. Reproduce una canción, apaga la pantalla y comprueba que sigue sonando.
3. Mira que la notificación tiene los botones de anterior, pausa y siguiente.
4. Gira el móvil y comprueba que no pierdes la pantalla en la que estabas.

## Problemas frecuentes

| Mensaje | Causa y arreglo |
|---|---|
| `javac: command not found` | Java no instalado o no es el JDK. Repite el paso 1. |
| `zip: command not found` | `sudo apt install zip` |
| `aapt2: No such file or directory` | El SDK no está en `~/android` o falta `build-tools;35.0.0`. Repite el paso 3 y comprueba con `ls ~/android/build-tools`. |
| `Falta la clave de firma` | No existe `build/pulso.jks`. Haz el paso 4 desde la carpeta `pulso`. |
| `Licenses not accepted` / licencias | Repite el comando `sdkmanager --licenses` del paso 3. |
| `bad interpreter: /bin/bash^M` | El script tiene finales de línea de Windows. Trabaja dentro de `~` en WSL, no en `/mnt/c`, y vuelve a clonar. |
| `warning: [options] source value 8 is obsolete` | Es solo un aviso. Se puede ignorar. |
| `Password verification failed` al firmar | La contraseña de la clave no coincide con `PULSO_KS_PASS`. |

## Cómo está organizado el proyecto

- `src/es/pulso/music/`: el código (`MainActivity` pinta las pantallas, `PlayerService` reproduce, `Song` es una canción).
- `res/`: recursos (el icono). `AndroidManifest.xml`: nombre, versión y permisos de la app.
- `build.sh`: el script que hace todos los pasos de compilar, alinear y firmar.
- `tests/`: pruebas que se ejecutan en un emulador (las lanza GitHub Actions).
- `build/`: se crea al compilar, no se sube a git.
