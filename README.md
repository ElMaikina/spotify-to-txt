# 🎧 Spotify to Text

Este proyecto permite conectarse a tu cuenta de Spotify mediante la API oficial de SpotiPy y exportar tus Albumes y Playlists en 
archivos de Texto Plano (.txt). Cada Album o Playlist se guarda como un archivo independiente que contiene todas sus canciones.

## 🚀 Funcionamiento

- Se conecta a Spotify usando OAuth.
- Exporta todos tus:
  - Albumes
  - Playlists
- Cada Album y Playlist se guarda en "spotify_exports/"
- Corre en Multi-Hilo al estilo Map-Reduce

## 📦 Requisistos

- Python 3.7+ (yo use Python 3.11)
- Libreria de SpotiPy instalada
- Cuenta de Spotify Premium
- Habilitar API de [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## 😎 Instalacion

Primero hay que actualizar Pip e instalar SpotiPy

```bash
python -m pip install --upgrade pip
pip install spotipy
```

Luego, crear la API de [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), anotar las credenciales (client_id, 
client_secret, redirect_uri, scope) en un archivo .txt y guardarlo en una carpeta facil de recordar y finalmente poner el Path
absoluto del archivo en main.py para poder conectarse.