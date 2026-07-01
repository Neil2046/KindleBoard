# KindleBoard

**現在のバージョン:** `V1.0`

KindleBoard は Docker で動作するセルフホスト型の Kindle / e-ink ダッシュボードです。古い Kindle Paperwhite を、週間スケジュール、メモ、To-do リストを表示する常時表示ボードとして再利用できます。

![KindleBoard English preview](preview.png)

KindleBoard は信頼できるプライベートネットワークでの利用を想定しています。インターネットに公開する場合は、VPN、リバースプロキシ認証、または別のアクセス制御を利用してください。

## 機能

- 週間スケジュール、勤務時間、休み、メモ、週合計時間の自動計算。
- `22:00` から `06:00` のような日跨ぎシフトに対応。
- 大きな文字で表示するメモモード。
- Kindle 上で完了/未完了を切り替えられる To-do リスト。
- 管理画面で内容編集、表示モード切り替え、言語切り替え。
- Kindle 向けの高コントラスト表示ページ。
- スケジュール、メモ、To-do、表示モード、言語設定を 1 つの SQLite データベースに保存。
- 多言語 UI。
- デフォルトポート: `10000`。

## 表示モード

- **Schedule**: 週間スケジュールと合計時間。
- **Memo**: 大きな文字のメモ。
- **To-do**: クリック可能なタスクリスト。

Kindle ページには選択中のモードだけが表示されます。

## Docker インストール

推奨イメージ:

```text
neil2046/kindleboard:latest
```

ミラー:

```text
ghcr.io/neil2046/kindleboard:latest
```

```bash
mkdir kindleboard
cd kindleboard
```

`docker-compose.yml` を作成:

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

起動:

```bash
docker compose up -d
```

アクセス:

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

## データ永続化

データは `./data/schedule.db` に保存されます。スケジュール、メモ、To-do、表示モード、言語設定はすべてこの 1 つの SQLite データベースに入ります。

初回起動時に `/data/schedule.db` が存在しない場合、内蔵の英語デモデータベースがコピーされます。既存データは上書きされません。

## アップグレード

```bash
docker compose pull
docker compose up -d
```

## Kindle 利用メモ

- Kindle ブラウザで `http://SERVER-IP:10000/kindle` を開きます。
- Kindle が Docker ホストに接続できる必要があります。
- ページには大きな更新ボタンがあります。
- Kindle のツールバーやスクリーンセーバーは Kindle OS 側の動作です。

## セキュリティ

KindleBoard にはログイン機能がありません。信頼できる環境で利用してください。外部公開する場合は VPN や認証付きリバースプロキシを使ってください。
