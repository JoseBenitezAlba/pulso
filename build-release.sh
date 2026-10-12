#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export JAVA_HOME="${JAVA_HOME:-$HOME/jdk}" PATH="${JAVA_HOME:-$HOME/jdk}/bin:$PATH"
SDK="${ANDROID_HOME:-$HOME/android}"; BT="$SDK/build-tools/35.0.0"; PLATFORM="$SDK/platforms/android-35/android.jar"
mkdir -p build/classes
"$BT/aapt2" compile --dir res -o build/res.zip
"$BT/aapt2" link -o build/base.apk -I "$PLATFORM" --manifest AndroidManifest.xml --java build/gen build/res.zip
javac -encoding UTF-8 -source 8 -target 8 -classpath "$PLATFORM" -d build/classes src/es/pulso/music/*.java $(find build/gen -name '*.java')
jar cf build/classes.jar -C build/classes .
"$BT/d8" --lib "$PLATFORM" --min-api 26 --output build build/classes.jar
cp build/base.apk build/unsigned.apk
(cd build; zip -q unsigned.apk classes.dex)
"$BT/zipalign" -f 4 build/unsigned.apk build/aligned.apk
if [ ! -f build/pulso.jks ]; then echo "Falta la clave de firma" >&2; exit 1; fi
"$BT/apksigner" sign --ks build/pulso.jks --ks-pass pass:android --out build/pulso.apk build/aligned.apk
"$BT/apksigner" verify --verbose build/pulso.apk
