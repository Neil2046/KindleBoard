# KindleBoard - Self-hosted Kindle and E-ink Dashboard

**Versión actual:** `V1.1`

KindleBoard es un panel autoalojado para Kindle y pantallas e-ink que se ejecuta con Docker. Convierte un Kindle Paperwhite antiguo en un tablero siempre visible para horarios semanales, notas y listas de tareas.

Es útil si buscas Kindle Paperwhite dashboard, e-ink dashboard, self-hosted dashboard, Docker Kindle dashboard, Kindle todo list, Kindle memo board o weekly schedule display para usar en tu propio servidor.

![Vista previa de KindleBoard como panel autoalojado para Kindle y e-ink con horario semanal](preview.png)

KindleBoard está pensado para redes privadas de confianza. Si lo expones a internet, usa una VPN, autenticación en un proxy inverso u otra capa de control de acceso.

## Casos de uso

- Convertir un Kindle Paperwhite antiguo en un panel e-ink siempre visible.
- Mostrar un horario semanal personal con total automático de horas.
- Mostrar notas, mensajes o recordatorios grandes y legibles.
- Usar el Kindle como lista de tareas con toque para completar.
- Ejecutarlo en casa, en un servidor Docker o en un entorno homelab.

## Palabras clave de búsqueda

Kindle dashboard, Kindle Paperwhite dashboard, e-ink dashboard, e-paper dashboard, self-hosted dashboard, Docker Kindle dashboard, Kindle todo list, Kindle memo board, Kindle schedule display, home dashboard, homelab dashboard, SQLite dashboard.
## Funciones

- Horario semanal personal con turnos, días de descanso, notas y total automático de horas.
- Soporte para turnos nocturnos o cruzados, como `22:00` a `06:00`.
- Modo de notas con texto grande.
- Lista de tareas con marcado de completado directamente desde Kindle.
- Panel de administración para editar contenido, cambiar modo y cambiar idioma.
- Descarga de copia de seguridad de la base de datos y restauración desde un archivo local.
- Página optimizada para Kindle con alto contraste y botón grande de actualización.
- Una sola base de datos SQLite para horario, notas, tareas, modo de pantalla e idioma.
- Interfaz multilingüe.
- Puerto predeterminado: `10000`.

## Modos

- **Schedule**: horario semanal y total de horas.
- **Memo**: una nota grande y legible.
- **To-do**: lista de tareas clicable.

La página Kindle solo muestra el modo seleccionado.

## Instalación con Docker

Imagen recomendada:

```text
neil2046/kindleboard:latest
```

Imagen espejo:

```text
ghcr.io/neil2046/kindleboard:latest
```

```bash
mkdir kindleboard
cd kindleboard
```

Crea `docker-compose.yml`:

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

Inicia:

```bash
docker compose up -d
```

Accede:

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

## Persistencia de datos

Los datos se guardan en `./data/schedule.db`. Horario, notas, tareas, modo de pantalla e idioma se almacenan en esta única base de datos SQLite.

El panel de administración incluye herramientas para descargar una copia de seguridad SQLite y restaurar datos desde un archivo local de copia de seguridad de KindleBoard.

En el primer arranque, si `/data/schedule.db` no existe, KindleBoard copia una base de datos demo en inglés. Los datos existentes nunca se sobrescriben.

## Actualización

```bash
docker compose pull
docker compose up -d
```

## Uso en Kindle

- Abre `http://SERVER-IP:10000/kindle` en el navegador del Kindle.
- Activa el modo siempre encendido, sin suspensión o kiosk si tu Kindle o firmware lo permite.
- El Kindle debe poder acceder al host Docker.
- La página incluye un botón grande de actualización.
- Las barras del navegador y el protector de pantalla dependen de Kindle OS.

## Seguridad

KindleBoard no incluye cuentas ni inicio de sesión. Úsalo en entornos de confianza. Para acceso externo, usa VPN o autenticación mediante proxy inverso.

