# KindleBoard - Self-hosted Kindle and E-ink Dashboard

**Aktuelle Version:** `V1.1`

KindleBoard ist ein selbst gehostetes Kindle-Dashboard und E-Ink-Display-System für Docker. Es macht aus einem alten Kindle Paperwhite ein dauerhaft sichtbares Board für Wochenpläne, Notizen und Aufgabenlisten.

KindleBoard eignet sich für alle, die ein Kindle Paperwhite dashboard, e-ink dashboard, self-hosted dashboard, Docker Kindle dashboard, Kindle todo list, Kindle memo board oder weekly schedule display auf dem eigenen Server suchen.

![KindleBoard self-hosted Kindle e-ink dashboard preview mit Wochenplan](preview.png)

KindleBoard ist für vertrauenswürdige private Netzwerke gedacht. Wenn du es im Internet bereitstellst, nutze VPN, Reverse-Proxy-Authentifizierung oder eine andere Zugriffskontrolle.

## Typische Anwendungsfälle

- Einen alten Kindle Paperwhite als dauerhaft sichtbares E-Ink-Dashboard nutzen.
- Persönliche Wochenpläne mit automatischer Gesamtstundenberechnung anzeigen.
- Große gut lesbare Notizen, Nachrichten oder Erinnerungen anzeigen.
- Den Kindle als einfache antippbare To-do-Liste verwenden.
- Privat zu Hause, auf einem Docker-Host oder im Homelab betreiben.

## Suchbegriffe

Kindle dashboard, Kindle Paperwhite dashboard, e-ink dashboard, e-paper dashboard, self-hosted dashboard, Docker Kindle dashboard, Kindle todo list, Kindle memo board, Kindle schedule display, home dashboard, homelab dashboard, SQLite dashboard.
## Funktionen

- Persönlicher Wochenplan mit Schichten, freien Tagen, Notizen und automatischer Wochenstundensumme.
- Unterstützung für Nachtschichten wie `22:00` bis `06:00`.
- Notizmodus mit großer Schrift.
- Aufgabenliste mit direktem Abhaken auf dem Kindle.
- Admin-Seite zum Bearbeiten von Inhalten, Umschalten des Modus und Ändern der Sprache.
- Datenbank-Backup herunterladen und lokale Datenbank-Backups wiederherstellen.
- Kindle-optimierte Anzeige mit hohem Kontrast und großem Aktualisieren-Button.
- Eine einzige SQLite-Datenbank für Zeitplan, Notizen, Aufgaben, Anzeigemodus und Sprache.
- Mehrsprachige Oberfläche.
- Standard-Port: `10000`.

## Anzeigemodi

- **Schedule**: Wochenplan und Gesamtstunden.
- **Memo**: große Notiz.
- **To-do**: anklickbare Aufgabenliste.

Auf der Kindle-Seite wird nur der ausgewählte Modus angezeigt.

## Docker-Installation

Empfohlenes Image:

```text
neil2046/kindleboard:latest
```

Mirror:

```text
ghcr.io/neil2046/kindleboard:latest
```

```bash
mkdir kindleboard
cd kindleboard
```

`docker-compose.yml` erstellen:

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

Starten:

```bash
docker compose up -d
```

Aufrufen:

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

## Datenpersistenz

Die Daten liegen in `./data/schedule.db`. Zeitplan, Notizen, Aufgaben, Anzeigemodus und Spracheinstellungen werden in dieser einen SQLite-Datenbank gespeichert.

Die Admin-Seite enthält Werkzeuge zum Herunterladen eines SQLite-Backups und zum Wiederherstellen aus einer lokalen KindleBoard-Datenbankdatei.

Beim ersten Start kopiert KindleBoard eine englische Demo-Datenbank, wenn `/data/schedule.db` noch nicht existiert. Vorhandene Daten werden nie überschrieben.

## Aktualisierung

```bash
docker compose pull
docker compose up -d
```

## Kindle-Hinweise

- Öffne `http://SERVER-IP:10000/kindle` im Kindle-Browser.
- Aktiviere Always-on, Kein-Ruhezustand oder einen Kiosk-Anzeigemodus, falls dein Kindle oder deine Firmware das unterstützt.
- Der Kindle muss den Docker-Host erreichen können.
- Die Seite enthält einen großen Aktualisieren-Button.
- Browserleiste und Bildschirmschoner werden von Kindle OS gesteuert.

## Sicherheit

KindleBoard hat keine Benutzerkonten oder Login-Funktion. Nutze es in vertrauenswürdigen Umgebungen. Für externen Zugriff verwende VPN oder einen authentifizierten Reverse Proxy.

