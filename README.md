# Pulso

Música local, sin anuncios ni conexión. Android 8.0 o posterior.

- Lee los archivos de audio del dispositivo con el permiso de música.
- Busca por título, artista o álbum.
- Crea listas, añade canciones y cambia sus nombres. Las listas se guardan en el móvil.
- Desliza a la derecha para abrir tus listas. El botón + añade una canción.
- Reproduce con la pantalla apagada y desde la notificación. Pausa al desconectar auriculares.
- Avance, retroceso, barra de progreso, aleatorio y repetición.
- Sin permiso de internet, cuentas, vídeos ni servicios externos.

## Compilar

Java 17, Android SDK 35 y Build Tools 35.0.0. Código Java nativo, sin dependencias externas. `build.sh` compila recursos y código, alinea y firma el APK. La clave de publicación no se incluye en el código.

## Privacidad

Los archivos no salen del dispositivo. Pulso no borra ni modifica archivos de música. Eliminar una lista solo elimina la lista. Si borras los datos de la app o la desinstalas, se pierden tus listas.
