# KindleBoard

**Current version:** `V1.0`

KindleBoard is a self-hosted Kindle display system for Docker. It turns a Kindle Paperwhite into a simple always-visible board for a personal schedule, memo, or to-do list.

![KindleBoard English preview](docs/preview.png)

KindleBoard is intended for trusted private-network use. Run it in an internal Docker environment, or protect it with a VPN, reverse proxy, or authentication layer before exposing it to the public internet.

The app uses SQLite internally, so no external database service is required.

## Features

- Personal weekly schedule with automatic total hours.
- Memo display mode.
- To-do list mode with tap-to-complete support on Kindle.
- Kindle-friendly high-contrast display page.
- Admin page for editing content and switching modes.
- One SQLite database for schedule, memo, to-do items, display mode, and language settings.
- Multilingual UI.
- Default port: `10000`.

## Supported Languages

English, 简体中文, 繁體中文, 日本語, 한국어, Español, Deutsch, Français, Português.

The default language follows the browser language. After you manually choose and save a language in the admin page, KindleBoard will use that saved language.

## Docker Installation

The published image is:

```text
neil2046/kindleboard:latest
```

Mirror image:

```text
ghcr.io/neil2046/kindleboard:latest
```

### Option A: Docker Compose

Create a project folder:

```bash
mkdir kindleboard
cd kindleboard
```

Create `docker-compose.yml` in that folder:

```yaml
services:
  kindleboard:
    image: neil2046/kindleboard:latest
    container_name: kindleboard
    ports:
      - "10000:10000"
    volumes:
      - ./data:/data
    restart: unless-stopped
```

Start the container:

```bash
docker compose up -d
```

Open:

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

Replace `SERVER-IP` with the IP address of the machine running Docker.

### Option B: docker run

```bash
docker run -d \
  --name kindleboard \
  -p 10000:10000 \
  -v ./data:/data \
  --restart unless-stopped \
  neil2046/kindleboard:latest
```

GHCR mirror:

```bash
docker pull ghcr.io/neil2046/kindleboard:latest
```

If you use `docker run`, run the command from the folder where you want KindleBoard to store its `data` directory.

## Build From Source

You usually do not need this. Use it only if you want to build the image yourself from the repository source:

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

Do not delete the `data` folder. It contains all user data.

The Docker image includes a default English demo database. On first start, if `/data/schedule.db` does not exist, KindleBoard copies the demo database into `/data/schedule.db`. Existing user data is never overwritten.

SQLite runtime helper files are ignored by Git:

```text
data/schedule.db-wal
data/schedule.db-shm
```

## Upgrade

Pull the latest image and restart:

```bash
docker compose pull
docker compose up -d
```

## Kindle Notes

KindleBoard is intended for the Kindle browser:

- Use `http://SERVER-IP:10000/kindle` on the Kindle.
- Keep the Kindle connected to the same reachable network as the Docker host.
- The page includes a large refresh button.
- The Kindle browser toolbar and screen saver are controlled by Kindle OS, not by the web page.
- Keeping Wi-Fi and front light on will use more battery.

## 中文

KindleBoard 是一个可运行在 Docker 里的 Kindle 显示系统，不需要额外数据库。建议部署在受信任的私有网络或内网环境中，不建议直接暴露到公网。

Docker 安装：

```bash
docker compose up -d
```

访问：

```text
管理端: http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

三个功能都在同一个数据库 `./data/schedule.db` 内：排班表、记事本、待办清单。升级时不要删除 `data` 目录。

## 繁體中文

KindleBoard 是一個可運行在 Docker 裡的 Kindle 顯示系統，不需要額外資料庫。建議部署在受信任的私有網路或內網環境中，不建議直接暴露到公網。

Docker 安裝：

```bash
docker compose up -d
```

訪問：

```text
管理端: http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

三個功能都在同一個資料庫 `./data/schedule.db` 內：排班表、記事本、待辦清單。升級時請保留 `data` 目錄。

## 日本語

KindleBoard は Docker で動作する Kindle 表示システムです。外部データベースは不要です。信頼できるプライベートネットワークでの利用を推奨します。

Docker インストール：

```bash
docker compose up -d
```

アクセス：

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

勤務表、メモ、やることリストはすべて `./data/schedule.db` に保存されます。アップグレード時は `data` フォルダーを削除しないでください。

## 한국어

KindleBoard는 Docker에서 실행되는 Kindle 표시 시스템입니다. 외부 데이터베이스는 필요하지 않습니다. 신뢰할 수 있는 사설 네트워크에서 사용하는 것을 권장합니다.

Docker 설치:

```bash
docker compose up -d
```

접속:

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

근무표, 메모, 할 일 목록은 모두 `./data/schedule.db` 하나에 저장됩니다. 업그레이드할 때 `data` 폴더를 삭제하지 마세요.

## Español

KindleBoard es un sistema de pantalla para Kindle que se ejecuta en Docker. No requiere una base de datos externa. Se recomienda usarlo en una red privada de confianza.

Instalación con Docker:

```bash
docker compose up -d
```

Acceso:

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

El horario, las notas y las tareas se guardan en una sola base de datos: `./data/schedule.db`. No borres la carpeta `data` al actualizar.

## Deutsch

KindleBoard ist ein Kindle-Anzeigesystem für Docker. Es benötigt keine externe Datenbank. Der Betrieb in einem vertrauenswürdigen privaten Netzwerk wird empfohlen.

Docker-Installation:

```bash
docker compose up -d
```

Aufrufen:

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

Dienstplan, Notizen und Aufgaben werden in einer einzigen Datenbank gespeichert: `./data/schedule.db`. Beim Upgrade den Ordner `data` nicht löschen.

## Français

KindleBoard est un système d’affichage Kindle qui fonctionne avec Docker. Il ne nécessite aucune base de données externe. Il est recommandé de l’utiliser dans un réseau privé de confiance.

Installation Docker :

```bash
docker compose up -d
```

Accès :

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

Le planning, les notes et les tâches sont stockés dans une seule base de données : `./data/schedule.db`. Ne supprimez pas le dossier `data` lors d’une mise à jour.

## Português

KindleBoard é um sistema de exibição para Kindle que roda em Docker. Ele não requer banco de dados externo. Recomenda-se usá-lo em uma rede privada confiável.

Instalação com Docker:

```bash
docker compose up -d
```

Acesso:

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

Escala, notas e tarefas ficam em um único banco de dados: `./data/schedule.db`. Não apague a pasta `data` ao atualizar.
