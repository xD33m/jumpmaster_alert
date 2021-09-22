# Apex Jumpmaster Detection

## 🛠️ Setup

Ensure you have [Node](https://nodejs.org/en/download/) and [Python](https://www.python.org/downloads/) installed, then clone this repository. After it's cloned, navigate to the project's root directory on your computer and
run the following scrips in a terminal application _(e.g., Git Bash)_:

**Install Python dependencies:**

```bash
pip3 install -r ./backend/requirements.txt
```

**Install Node dependencies:**

```bash
yarn install
```

<br>

## ⚙️ Config

**Electron:** Electron's `main.js`, `preload.js`, and `renderer.js` files can be found in the project's root directory.

**React:** React files can be found in the `./src/` folder, the custom toolbar is in `./src/components/toolbar`.

**Python:** Python scripts can be created in the `./app.py` file and used on events via [REST](https://developer.mozilla.org/en-US/docs/Glossary/REST) calls.

<br>

## 📜 Scripts

Below are the scripts you'll need to run and package your application, as well as build out JSDoc documentation, if you choose to do so. An exhaustive list of scripts that are available can be found in the `package.json` file of the project's root directory, in the `scripts` section.

**Start Developer Mode:**

```bash
yarn run start
```

**Package Linux:**

```bash
yarn run build:package:linux
```

**Package macOS:**

```bash
yarn run build:package:mac
```

**Package Windows:**

```bash
yarn run build:package:windows
```

**Build Documentation:**

```bash
yarn run build:docs
```

_Note: For packaging, you must install [PyInstaller](https://pypi.org/project/pyinstaller) and include its path in your environment variables. Windows uses [electron-wix-msi](https://github.com/felixrieseberg/electron-wix-msi), which must also be installed and have its path included in your environment variables. MacOS uses [electron-installer-dmg](https://github.com/electron-userland/electron-installer-dmg)._
<br><br>

## 🏷️ License

[MIT](https://github.com/iPzard/electron-react-python-template/blob/master/LICENSE)
