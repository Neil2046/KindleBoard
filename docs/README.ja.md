# KindleBoard - Self-hosted Kindle and E-ink Dashboard

**現在のバージョン:** `V1.1`

KindleBoard は Docker で動作するセルフホスト型の Kindle ダッシュボード / e-ink 表示システムです。古い Kindle Paperwhite を、週間スケジュール、メモ、To-do リストを表示する常時表示ボードとして再利用できます。

Kindle Paperwhite dashboard、e-ink dashboard、self-hosted dashboard、Docker Kindle dashboard、Kindle todo list、Kindle memo board、weekly schedule display を探している場合に使いやすい軽量なプロジェクトです。

![KindleBoard self-hosted Kindle e-ink dashboard preview showing a weekly schedule](preview.png)

KindleBoard は信頼できるプライベートネットワークでの利用を想定しています。インターネットに公開する場合は、VPN、リバースプロキシ認証、または別のアクセス制御を利用してください。

## 主な利用シーン

- 古い Kindle Paperwhite を常時表示の e-ink dashboard にする。
- 個人の週間スケジュールと合計勤務時間を表示する。
- 大きく読みやすいメモや家族向けメッセージを表示する。
- Kindle 上で完了操作できる To-do リストとして使う。
- 自宅サーバー、Docker ホスト、homelab 環境でプライベートに運用する。

## 検索キーワード

Kindle dashboard, Kindle Paperwhite dashboard, e-ink dashboard, e-paper dashboard, self-hosted dashboard, Docker Kindle dashboard, Kindle todo list, Kindle memo board, Kindle schedule display, home dashboard, homelab dashboard, SQLite dashboard.
## 機能

- 週間スケジュール、勤務時間、休み、メモ、週合計時間の自動計算。
- `22:00` から `06:00` のような日跨ぎシフトに対応。
- 大きな文字で表示するメモモード。
- Kindle 上で完了/未完了を切り替えられる To-do リスト。
- 管理画面で内容編集、表示モード切り替え、言語切り替え。
- データベースバックアップのダウンロードと、ローカルバックアップからの復元。
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

管理画面には、SQLite バックアップをダウンロードし、ローカルの KindleBoard データベースバックアップファイルから復元するためのツールがあります。

## アップグレード

```bash
docker compose pull
docker compose up -d
```

## Kindle 利用メモ

- Kindle ブラウザで `http://SERVER-IP:10000/kindle` を開きます。
- Kindle またはファームウェアが常時表示、スリープ無効、kiosk 表示モードに対応している場合は有効にしてください。
- Kindle が Docker ホストに接続できる必要があります。
- ページには大きな更新ボタンがあります。
- Kindle のツールバーやスクリーンセーバーは Kindle OS 側の動作です。

## セキュリティ

KindleBoard にはログイン機能がありません。信頼できる環境で利用してください。外部公開する場合は VPN や認証付きリバースプロキシを使ってください。

