# KindleBoard

KindleBoard is a self-hosted Kindle display system for a private LAN or NAS. It turns a Kindle Paperwhite into a simple always-visible board for a personal schedule, memo, or to-do list.

KindleBoard is intended for trusted internal network use. It is recommended to run it inside your home LAN, office LAN, or NAS environment. Do not expose it directly to the public internet without a VPN, reverse proxy, or authentication layer.

The app is designed for Docker deployment. It uses SQLite internally, so no external database is required.

## Features

- Personal weekly schedule with automatic total hours.
- Memo display mode.
- To-do list mode with tap-to-complete support on Kindle.
- Kindle-friendly high-contrast display page.
- Admin page for editing content and switching modes.
- Persistent SQLite data.
- Multilingual UI.
- Default port: `10000`.

## Supported Languages

English, 简体中文, 繁體中文, 日本語, 한국어, Español, Deutsch, Français, Português.

The default language follows the browser language. After you manually choose and save a language in the admin page, KindleBoard will use that saved language.

## Docker Installation

Create a folder for KindleBoard:

```text
docker/kindleboard
```

Put these files into the folder:

```text
app.py
Dockerfile
docker-compose.yml
README.md
static/
```

Start with Docker Compose:

```bash
docker compose up -d
```

Open:

```text
Admin:  http://NAS-IP:10000/admin
Kindle: http://NAS-IP:10000/kindle
```

Replace `NAS-IP` with your NAS or server LAN IP address.

## docker-compose.yml

```yaml
services:
  kindleboard:
    build: .
    container_name: kindleboard
    ports:
      - "10000:10000"
    volumes:
      - ./data:/data
    restart: unless-stopped
```

## NAS Docker UI Installation

1. Open your NAS file manager.
2. Create a folder, for example `docker/kindleboard`.
3. Upload `app.py`, `Dockerfile`, `docker-compose.yml`, `README.md`, and `static/`.
4. Open the NAS Docker app.
5. Go to `Compose`.
6. Create a new project named `kindleboard`.
7. Set the project path to `docker/kindleboard`.
8. Use the included `docker-compose.yml`.
9. Start the project.
10. Open `http://NAS-IP:10000/admin`.

## Data Persistence

Data is stored in:

```text
./data/schedule.db
```

Schedule, memo, to-do items, display mode, and language settings are all stored in this single SQLite database.

The Compose file maps it into the container:

```text
./data:/data
```

Do not delete the `data` folder. It contains your schedule, memo, to-do list, display mode, and language setting.

The repository includes a default English demo database at `data/schedule.db`. A fresh Docker installation starts with this demo content.

SQLite runtime helper files are ignored by Git:

```text
data/schedule.db-wal
data/schedule.db-shm
```

## Upgrade

Replace the application files, but keep the `data` folder:

```text
app.py
Dockerfile
docker-compose.yml
static/
README.md
```

Then rebuild and restart:

```bash
docker compose up -d --build
```

## Kindle Notes

KindleBoard is intended for the Kindle browser:

- Use `http://NAS-IP:10000/kindle` on the Kindle.
- Keep the device on the same LAN as the NAS.
- The page includes a large refresh button.
- The Kindle browser toolbar and screen saver are controlled by Kindle OS, not by the web page.
- Keeping Wi-Fi and front light on will use more battery.

## 中文

KindleBoard 是一个适合部署在 NAS 内网里的 Kindle 显示系统，只需要 Docker，不需要额外数据库。

Docker 安装：

```bash
docker compose up -d
```

访问：

```text
管理端: http://NAS-IP:10000/admin
Kindle: http://NAS-IP:10000/kindle
```

数据保存在 `./data/schedule.db`。升级时不要删除 `data` 目录。

## 繁體中文

KindleBoard 是一個適合部署在 NAS 內網中的 Kindle 顯示系統，只需要 Docker，不需要額外資料庫。

Docker 安裝：

```bash
docker compose up -d
```

訪問：

```text
管理端: http://NAS-IP:10000/admin
Kindle: http://NAS-IP:10000/kindle
```

資料保存在 `./data/schedule.db`。升級時請保留 `data` 目錄。

## 日本語

KindleBoard は NAS のローカルネットワークで使う Kindle 表示システムです。Docker だけで動作し、外部データベースは不要です。

Docker インストール：

```bash
docker compose up -d
```

アクセス：

```text
Admin:  http://NAS-IP:10000/admin
Kindle: http://NAS-IP:10000/kindle
```

データは `./data/schedule.db` に保存されます。アップグレード時は `data` フォルダーを削除しないでください。

## 한국어

KindleBoard는 NAS 로컬 네트워크에서 사용하는 Kindle 표시 시스템입니다. Docker만 필요하며 외부 데이터베이스는 필요하지 않습니다.

Docker 설치:

```bash
docker compose up -d
```

접속:

```text
Admin:  http://NAS-IP:10000/admin
Kindle: http://NAS-IP:10000/kindle
```

데이터는 `./data/schedule.db`에 저장됩니다. 업그레이드할 때 `data` 폴더를 삭제하지 마세요.

## Español

KindleBoard es un sistema de pantalla para Kindle pensado para una red local o NAS. Solo necesita Docker y no requiere una base de datos externa.

Instalación con Docker:

```bash
docker compose up -d
```

Acceso:

```text
Admin:  http://NAS-IP:10000/admin
Kindle: http://NAS-IP:10000/kindle
```

Los datos se guardan en `./data/schedule.db`. No borres la carpeta `data` al actualizar.

## Deutsch

KindleBoard ist ein Kindle-Anzeigesystem für ein lokales Netzwerk oder NAS. Es benötigt nur Docker und keine externe Datenbank.

Docker-Installation:

```bash
docker compose up -d
```

Aufrufen:

```text
Admin:  http://NAS-IP:10000/admin
Kindle: http://NAS-IP:10000/kindle
```

Die Daten liegen in `./data/schedule.db`. Beim Upgrade den Ordner `data` nicht löschen.

## Français

KindleBoard est un système d’affichage Kindle pour un réseau local ou un NAS. Il nécessite seulement Docker et aucune base de données externe.

Installation Docker :

```bash
docker compose up -d
```

Accès :

```text
Admin:  http://NAS-IP:10000/admin
Kindle: http://NAS-IP:10000/kindle
```

Les données sont stockées dans `./data/schedule.db`. Ne supprimez pas le dossier `data` lors d’une mise à jour.

## Português

KindleBoard é um sistema de exibição para Kindle em uma rede local ou NAS. Ele precisa apenas de Docker e não requer banco de dados externo.

Instalação com Docker:

```bash
docker compose up -d
```

Acesso:

```text
Admin:  http://NAS-IP:10000/admin
Kindle: http://NAS-IP:10000/kindle
```

Os dados ficam em `./data/schedule.db`. Não apague a pasta `data` ao atualizar.
