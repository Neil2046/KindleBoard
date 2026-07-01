# KindleBoard

**目前版本：** `V1.1`

KindleBoard 是一個運行在 Docker 裡的自託管 Kindle / 墨水屏顯示系統。它可以把舊 Kindle Paperwhite 變成常駐顯示的個人看板，用來顯示每週排班、記事或待辦清單。

![KindleBoard 英文預覽](preview.png)

KindleBoard 建議運行在受信任的私有網路或內網 Docker 環境中。如果要暴露到公網，請先放到 VPN、反向代理認證或其他存取控制之後。

## 功能

- 個人每週排班表，支援每日班次、休息日、備註和本週總工時計算。
- 支援跨日班次，例如 `22:00` 到 `06:00`。
- 記事本模式，用大字號顯示一段文字。
- 待辦清單模式，可直接在 Kindle 頁面點擊完成或取消完成。
- 管理端用於編輯內容、切換顯示模式和切換語言。
- 支援下載資料庫備份，並可上傳本機資料庫備份恢復資料。
- Kindle 專用顯示頁，黑白高對比、大字號、帶大型刷新按鈕。
- 一個 SQLite 資料庫保存所有資料：排班、記事本、待辦清單、顯示模式、語言設定。
- 支援多語言介面。
- 預設連接埠：`10000`。

## 顯示模式

- **排班表**：顯示一週班次和總工時。
- **記事本**：顯示一段大字號記事。
- **待辦清單**：顯示可點擊完成的任務列表。

Kindle 頁面只顯示目前選中的模式。

## Docker 安裝

推薦映像：

```text
neil2046/kindleboard:latest
```

備用映像：

```text
ghcr.io/neil2046/kindleboard:latest
```

建立目錄並建立 `docker-compose.yml`：

```bash
mkdir kindleboard
cd kindleboard
```

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

啟動：

```bash
docker compose up -d
```

訪問：

```text
管理端: http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

## 資料持久化

資料保存在 `./data/schedule.db`。排班表、記事本、待辦清單、顯示模式和語言設定都在同一個 SQLite 資料庫中。

首次啟動時，如果 `/data/schedule.db` 不存在，程式會複製內建英文示範資料庫。已有資料不會被覆蓋。

升級時請保留 `data` 目錄。

管理頁面提供資料庫工具，可以下載 SQLite 備份，也可以上傳本機 KindleBoard 資料庫備份檔案來恢復資料。

## 升級

```bash
docker compose pull
docker compose up -d
```

## Kindle 使用說明

- 在 Kindle 瀏覽器打開 `http://SERVER-IP:10000/kindle`。
- Kindle 需要能連到 Docker 主機。
- 頁面內有大型刷新按鈕。
- Kindle 工具列、狀態列、螢幕保護由 Kindle 系統控制。

## 安全說明

KindleBoard 不包含登入系統，適合可信任的個人環境。不要直接暴露到公網；如需外網訪問，請使用 VPN 或反向代理認證。

