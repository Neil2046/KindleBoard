# KindleBoard

**현재 버전:** `V1.0`

KindleBoard는 Docker에서 실행되는 셀프 호스팅 Kindle / e-ink 대시보드입니다. 오래된 Kindle Paperwhite를 주간 일정, 메모, 할 일 목록을 표시하는 상시 표시 보드로 사용할 수 있습니다.

![KindleBoard English preview](preview.png)

KindleBoard는 신뢰할 수 있는 사설 네트워크에서 사용하는 것을 권장합니다. 인터넷에 공개하려면 VPN, 리버스 프록시 인증, 또는 별도의 접근 제어를 사용하세요.

## 기능

- 개인 주간 근무표, 휴무일, 메모, 주간 총 근무시간 자동 계산.
- `22:00`부터 `06:00`까지 같은 야간/익일 근무 지원.
- 큰 글자로 표시되는 메모 모드.
- Kindle에서 직접 완료 처리할 수 있는 할 일 목록.
- 관리자 화면에서 내용 편집, 표시 모드 전환, 언어 변경.
- Kindle 브라우저에 맞춘 고대비 표시 페이지.
- 근무표, 메모, 할 일, 표시 모드, 언어 설정을 하나의 SQLite 데이터베이스에 저장.
- 다국어 UI.
- 기본 포트: `10000`.

## 표시 모드

- **Schedule**: 주간 일정과 총 시간.
- **Memo**: 큰 글자의 메모.
- **To-do**: 클릭 가능한 할 일 목록.

Kindle 페이지에는 선택한 모드만 표시됩니다.

## Docker 설치

권장 이미지:

```text
neil2046/kindleboard:latest
```

미러:

```text
ghcr.io/neil2046/kindleboard:latest
```

```bash
mkdir kindleboard
cd kindleboard
```

`docker-compose.yml` 생성:

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

실행:

```bash
docker compose up -d
```

접속:

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

## 데이터 보존

데이터는 `./data/schedule.db`에 저장됩니다. 근무표, 메모, 할 일, 표시 모드, 언어 설정이 모두 이 하나의 SQLite 데이터베이스에 저장됩니다.

처음 실행할 때 `/data/schedule.db`가 없으면 내장 영어 데모 데이터베이스가 복사됩니다. 기존 데이터는 덮어쓰지 않습니다.

## 업그레이드

```bash
docker compose pull
docker compose up -d
```

## Kindle 사용 메모

- Kindle 브라우저에서 `http://SERVER-IP:10000/kindle`을 엽니다.
- Kindle이 Docker 호스트에 접근할 수 있어야 합니다.
- 페이지에는 큰 새로고침 버튼이 있습니다.
- Kindle 툴바와 화면 보호기는 Kindle OS가 제어합니다.

## 보안

KindleBoard에는 로그인 기능이 없습니다. 신뢰할 수 있는 개인 환경에서 사용하세요. 외부 공개가 필요하다면 VPN 또는 인증이 있는 리버스 프록시를 사용하세요.
