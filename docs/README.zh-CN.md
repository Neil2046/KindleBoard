# KindleBoard

**当前版本：** `V1.1`

KindleBoard 是一个运行在 Docker 里的自托管 Kindle / 墨水屏显示系统。它可以把旧 Kindle Paperwhite 变成一个常驻显示的个人看板，用来显示每周排班、备忘录或待办清单。

![KindleBoard 英文预览](preview.png)

KindleBoard 建议运行在受信任的私有网络或内网 Docker 环境中。如果要暴露到公网，请先放到 VPN、反向代理认证或其他访问控制之后。

## 功能

- 个人每周排班表，支持每天班次、休息日、备注和本周总工时统计。
- 支持跨天班次，例如 `22:00` 到 `06:00`。
- 记事本模式，用大字号显示一段文字。
- 待办清单模式，可以直接在 Kindle 页面点击完成或取消完成。
- 管理端用于编辑内容、切换显示模式和切换语言。
- 支持下载数据库备份，并可上传本地数据库备份恢复数据。
- Kindle 专用显示页，黑白高对比、大字号、带大刷新按钮。
- 一个 SQLite 数据库保存所有数据：排班、记事本、待办清单、显示模式、语言设置。
- 支持多语言界面。
- 默认端口：`10000`。

## 显示模式

KindleBoard 有三种显示模式：

- **排班表**：显示一周班次和总工时。
- **记事本**：显示一段大字号备忘录。
- **待办清单**：显示可点击完成的任务列表。

Kindle 页面只显示当前选中的模式。

## Docker 安装

推荐镜像：

```text
neil2046/kindleboard:latest
```

备用镜像：

```text
ghcr.io/neil2046/kindleboard:latest
```

### Docker Compose

创建目录：

```bash
mkdir kindleboard
cd kindleboard
```

创建 `docker-compose.yml`：

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

启动：

```bash
docker compose up -d
```

访问：

```text
管理端: http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

把 `SERVER-IP` 换成运行 Docker 的机器 IP。

### docker run

在你希望保存数据的目录中运行：

```bash
docker run -d \
  --name kindleboard \
  -p 10000:10000 \
  -v ./data:/data \
  --restart unless-stopped \
  neil2046/kindleboard:latest
```

## 数据持久化

数据保存在：

```text
./data/schedule.db
```

排班表、记事本、待办清单、显示模式和语言设置都保存在这一个 SQLite 数据库中。

首次启动时，如果 `/data/schedule.db` 不存在，程序会把镜像内置的英文演示数据库复制过去。已有数据库不会被覆盖。

升级或重启时不要删除 `data` 目录，除非你想重置系统。

管理页面提供数据库工具，可以下载 SQLite 备份，也可以上传本地 KindleBoard 数据库备份文件来恢复数据。

## 升级

```bash
docker compose pull
docker compose up -d
```

数据会继续保存在 `./data/schedule.db`。

## Kindle 使用说明

- 在 Kindle 浏览器打开 `http://SERVER-IP:10000/kindle`。
- Kindle 需要能访问运行 Docker 的机器。
- 页面内有大刷新按钮。
- Kindle 浏览器工具栏、系统状态栏、屏保由 Kindle 系统控制，不是网页能完全控制的。
- 长期开 Wi-Fi 和前光会增加耗电。

## 安全说明

KindleBoard 不带账号和登录系统，适合个人可信环境。不要直接裸露到公网；如果必须公网访问，请使用 VPN、反向代理认证或其他访问控制。

