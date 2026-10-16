# Apex Jumpmaster Alert

A Windows desktop app that watches Apex Legends and alerts you with a voice clip or a Discord DM when you become jumpmaster.

## Why

In Apex Legends one player per squad is picked as jumpmaster and steers the squad's drop. This tool detects the jumpmaster indicator in the game window so you don't miss being picked, for example while tabbed out. It was built in September and October 2021 by Lucas Keller ([@xD33m](https://github.com/xD33m)) and Felix Keller, with a small contribution from Julius, for their own use (the Discord DM recipients are mapped to the three of them).

> Screenshot: not yet added.

## Features

- **Game detection**: waits for a window titled "Apex Legends" and starts detecting automatically once the game is running.
- **Character-select detection**: every 20 seconds, captures a region of the game window and template-matches it (OpenCV, normalized cross-correlation, threshold 0.8) against a reference icon of the character-selection screen.
- **Jumpmaster detection**: after character selection, checks once per second (for up to 120 seconds) for the jumpmaster icon, then goes back to waiting for the next match.
- **1080p and 1440p support**: capture regions and reference images are chosen based on the screen height.
- **Alerts** (toggle each on or off):
  - plays one of eight voice clips at random,
  - sends a Discord DM through a bot to the user mapped to the current Windows login.
- **Desktop UI**: custom title bar, start/stop and alert toggles, a live log panel fed over WebSockets, a loading spinner while detection starts, and a light/dark theme toggle.

## Tech stack

| Part | Technologies |
| --- | --- |
| Desktop shell | Electron 15, React 17 (Create React App), SCSS modules, socket.io-client |
| Detection backend (`backend/`) | Python, Flask, Flask-SocketIO, OpenCV, NumPy, pywin32 (window capture), winsound |
| Packaging | PyInstaller (backend executable), electron-packager, electron-wix-msi (Windows), electron-installer-dmg (macOS), electron-installer-debian (Linux) |

The project was started from the [electron-react-python-template](https://github.com/iPzard/electron-react-python-template) by Daniel Wade.

## Getting started

Requirements: Windows (the backend uses `pywin32` and `winsound`), [Node.js](https://nodejs.org/en/download/) with Yarn, and [Python](https://www.python.org/downloads/) 3. Dependencies are pinned to 2021 versions, so a Python version from that time (for example 3.9) is the safest choice.

```bash
pip install -r ./backend/requirements.txt
yarn install
yarn start        # starts React, Electron and the Flask backend in developer mode
```

For Discord DMs, create `backend/.env` (ignored by git) with a bot token and one Discord user ID per person:

```
DISCORD_BOT_TOKEN=...
LUCAS_ID=...
FELIX_ID=...
JULIUS_ID=...
```

The ID is picked from the Windows login name in `backend/lib/utils.py` (`getEnvId`), so adjust that mapping for other users.

### Packaging

```bash
yarn run build:package:windows   # also: build:package:mac, build:package:linux
yarn run build:docs              # JSDoc documentation
```

Packaging needs [PyInstaller](https://pypi.org/project/pyinstaller) on your `PATH`; Windows installers additionally need [electron-wix-msi](https://github.com/felixrieseberg/electron-wix-msi) and macOS uses [electron-installer-dmg](https://github.com/electron-userland/electron-installer-dmg).

## Architecture

```
Electron main process (main.js)
  ├─ picks a free port (3001-3999) and spawns the Python backend on it
  └─ loads the React UI
        └─ socket.io  <──>  Flask-SocketIO backend (backend/app.py)
                              ├─ DetectJumpmaster.py   window capture + OpenCV template matching
                              └─ lib/alerts.py         voice clips and Discord DMs
```

The UI sends `toggle` events (start/stop, sound, Discord DM) to the backend; the backend pushes `logs` and detection-state events back to the UI.

## Status

Finished in October 2021 and archived. The detection relies on fixed screen positions and reference images of the 2021 game UI, so it will most likely need new reference images to work with the current version of Apex Legends.

## License

[MIT](LICENSE)
