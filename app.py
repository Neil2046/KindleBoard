import os
import shutil
import sqlite3
from datetime import date, datetime, timedelta
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


APP_TITLE = "KindleBoard"
APP_VERSION = "V1.0"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "data")))
DB_PATH = os.path.join(DATA_DIR, "schedule.db")
DEFAULT_DB_PATHS = [
    os.path.join(BASE_DIR, "default-data", "schedule.db"),
    os.path.join(BASE_DIR, "data", "schedule.db"),
]
PORT = int(os.environ.get("PORT", "10000"))
MODES = ("schedule", "notebook", "todo")
LANGUAGES = [
    ("zh-CN", "中文"),
    ("zh-TW", "繁體中文"),
    ("en", "English"),
    ("ja", "日本語"),
    ("ko", "한국어"),
    ("es", "Español"),
    ("de", "Deutsch"),
    ("fr", "Français"),
    ("pt", "Português"),
]

TEXT = {
    "zh-CN": {
        "weekdays": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
        "mode_schedule": "排班表", "mode_notebook": "记事本", "mode_todo": "待办清单",
        "admin_title": "KindleBoard 管理", "kindle_page": "Kindle 页面", "previous_week": "上一周",
        "next_week": "下一周", "monday_date": "周一日期", "open": "打开", "display_mode": "显示模式",
        "language": "语言", "schedule_title": "个人排班表", "this_week": "本周", "total": "合计",
        "date": "日期", "start": "上班", "end": "下班", "break_minutes": "休息分钟",
        "status": "状态", "note": "备注", "hours": "工时", "rest": "休息", "message": "留言",
        "week_note": "留言 / 本周备注", "notebook_title": "记事本", "notebook_content": "记事本内容",
        "notebook_placeholder": "写一段给 Kindle 显示的内容", "todo_title": "待办清单",
        "todo_hint": "每行一件事。Kindle 上可以点击完成 / 取消完成。",
        "todo_placeholder": "买牛奶\n整理资料\n给 Kindle 充电", "save": "保存看板",
        "view_kindle": "查看 Kindle 版", "empty": "没有内容", "empty_todo": "没有待办",
        "refresh": "刷新", "weekly_total": "本周合计", "not_filled": "未填写",
        "hour": "小时", "minute": "分钟", "break_short": "休",
    },
    "zh-TW": {
        "weekdays": ["週一", "週二", "週三", "週四", "週五", "週六", "週日"],
        "mode_schedule": "排班表", "mode_notebook": "記事本", "mode_todo": "待辦清單",
        "admin_title": "KindleBoard 管理", "kindle_page": "Kindle 頁面", "previous_week": "上一週",
        "next_week": "下一週", "monday_date": "週一日期", "open": "打開", "display_mode": "顯示模式",
        "language": "語言", "schedule_title": "個人排班表", "this_week": "本週", "total": "合計",
        "date": "日期", "start": "上班", "end": "下班", "break_minutes": "休息分鐘",
        "status": "狀態", "note": "備註", "hours": "工時", "rest": "休息", "message": "留言",
        "week_note": "留言 / 本週備註", "notebook_title": "記事本", "notebook_content": "記事本內容",
        "notebook_placeholder": "寫一段給 Kindle 顯示的內容", "todo_title": "待辦清單",
        "todo_hint": "每行一件事。Kindle 上可以點擊完成 / 取消完成。",
        "todo_placeholder": "買牛奶\n整理資料\n給 Kindle 充電", "save": "保存看板",
        "view_kindle": "查看 Kindle 版", "empty": "沒有內容", "empty_todo": "沒有待辦",
        "refresh": "刷新", "weekly_total": "本週合計", "not_filled": "未填寫",
        "hour": "小時", "minute": "分鐘", "break_short": "休",
    },
    "en": {
        "weekdays": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "mode_schedule": "Schedule", "mode_notebook": "Memo", "mode_todo": "To-do",
        "admin_title": "KindleBoard Admin", "kindle_page": "Kindle page", "previous_week": "Previous week",
        "next_week": "Next week", "monday_date": "Monday", "open": "Open", "display_mode": "Display mode",
        "language": "Language", "schedule_title": "Personal schedule", "this_week": "This week", "total": "Total",
        "date": "Date", "start": "Start", "end": "End", "break_minutes": "Break minutes",
        "status": "Status", "note": "Note", "hours": "Hours", "rest": "Rest", "message": "Message",
        "week_note": "Message / weekly note", "notebook_title": "Memo", "notebook_content": "Memo text",
        "notebook_placeholder": "Write something for Kindle", "todo_title": "To-do list",
        "todo_hint": "One item per line. Tap items on Kindle to complete.",
        "todo_placeholder": "Buy milk\nSort files\nCharge Kindle", "save": "Save board",
        "view_kindle": "View Kindle page", "empty": "No content", "empty_todo": "No to-do items",
        "refresh": "Refresh", "weekly_total": "Weekly total", "not_filled": "Not filled",
        "hour": "h", "minute": "min", "break_short": "break",
    },
    "ja": {
        "weekdays": ["月", "火", "水", "木", "金", "土", "日"],
        "mode_schedule": "勤務表", "mode_notebook": "メモ", "mode_todo": "やること",
        "admin_title": "KindleBoard 管理", "kindle_page": "Kindle ページ", "previous_week": "前の週",
        "next_week": "次の週", "monday_date": "月曜日", "open": "開く", "display_mode": "表示モード",
        "language": "言語", "schedule_title": "個人勤務表", "this_week": "今週", "total": "合計",
        "date": "日付", "start": "開始", "end": "終了", "break_minutes": "休憩分",
        "status": "状態", "note": "メモ", "hours": "時間", "rest": "休み", "message": "伝言",
        "week_note": "伝言 / 今週のメモ", "notebook_title": "メモ", "notebook_content": "メモ内容",
        "notebook_placeholder": "Kindle に表示する内容を書く", "todo_title": "やることリスト",
        "todo_hint": "1行に1件。Kindle でタップして完了できます。",
        "todo_placeholder": "牛乳を買う\n資料を整理\nKindle を充電", "save": "保存",
        "view_kindle": "Kindle 版を見る", "empty": "内容なし", "empty_todo": "項目なし",
        "refresh": "更新", "weekly_total": "今週合計", "not_filled": "未入力",
        "hour": "時間", "minute": "分", "break_short": "休憩",
    },
    "ko": {
        "weekdays": ["월", "화", "수", "목", "금", "토", "일"],
        "mode_schedule": "근무표", "mode_notebook": "메모", "mode_todo": "할 일",
        "admin_title": "KindleBoard 관리", "kindle_page": "Kindle 페이지", "previous_week": "지난주",
        "next_week": "다음 주", "monday_date": "월요일", "open": "열기", "display_mode": "표시 모드",
        "language": "언어", "schedule_title": "개인 근무표", "this_week": "이번 주", "total": "합계",
        "date": "날짜", "start": "시작", "end": "종료", "break_minutes": "휴식 분",
        "status": "상태", "note": "메모", "hours": "시간", "rest": "휴식", "message": "메시지",
        "week_note": "메시지 / 이번 주 메모", "notebook_title": "메모", "notebook_content": "메모 내용",
        "notebook_placeholder": "Kindle 에 표시할 내용을 쓰세요", "todo_title": "할 일 목록",
        "todo_hint": "한 줄에 하나씩. Kindle 에서 눌러 완료할 수 있습니다.",
        "todo_placeholder": "우유 사기\n자료 정리\nKindle 충전", "save": "저장",
        "view_kindle": "Kindle 보기", "empty": "내용 없음", "empty_todo": "할 일 없음",
        "refresh": "새로고침", "weekly_total": "이번 주 합계", "not_filled": "미입력",
        "hour": "시간", "minute": "분", "break_short": "휴식",
    },
    "es": {
        "weekdays": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
        "mode_schedule": "Turnos", "mode_notebook": "Notas", "mode_todo": "Tareas",
        "admin_title": "Administrar KindleBoard", "kindle_page": "Página Kindle", "previous_week": "Semana anterior",
        "next_week": "Semana siguiente", "monday_date": "Lunes", "open": "Abrir", "display_mode": "Modo",
        "language": "Idioma", "schedule_title": "Turnos personales", "this_week": "Esta semana", "total": "Total",
        "date": "Fecha", "start": "Inicio", "end": "Fin", "break_minutes": "Pausa min",
        "status": "Estado", "note": "Nota", "hours": "Horas", "rest": "Descanso", "message": "Mensaje",
        "week_note": "Mensaje / nota semanal", "notebook_title": "Notas", "notebook_content": "Texto",
        "notebook_placeholder": "Escribe algo para Kindle", "todo_title": "Lista de tareas",
        "todo_hint": "Una tarea por línea. Toca en Kindle para completar.",
        "todo_placeholder": "Comprar leche\nOrdenar archivos\nCargar Kindle", "save": "Guardar",
        "view_kindle": "Ver Kindle", "empty": "Sin contenido", "empty_todo": "Sin tareas",
        "refresh": "Actualizar", "weekly_total": "Total semanal", "not_filled": "Sin completar",
        "hour": "h", "minute": "min", "break_short": "pausa",
    },
    "de": {
        "weekdays": ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
        "mode_schedule": "Dienstplan", "mode_notebook": "Notizen", "mode_todo": "Aufgaben",
        "admin_title": "KindleBoard Verwaltung", "kindle_page": "Kindle-Seite", "previous_week": "Vorige Woche",
        "next_week": "Nächste Woche", "monday_date": "Montag", "open": "Öffnen", "display_mode": "Modus",
        "language": "Sprache", "schedule_title": "Persönlicher Dienstplan", "this_week": "Diese Woche", "total": "Summe",
        "date": "Datum", "start": "Start", "end": "Ende", "break_minutes": "Pause Min.",
        "status": "Status", "note": "Notiz", "hours": "Stunden", "rest": "Frei", "message": "Nachricht",
        "week_note": "Nachricht / Wochennotiz", "notebook_title": "Notizen", "notebook_content": "Notiztext",
        "notebook_placeholder": "Text für Kindle schreiben", "todo_title": "Aufgabenliste",
        "todo_hint": "Eine Aufgabe pro Zeile. Auf Kindle antippen zum Erledigen.",
        "todo_placeholder": "Milch kaufen\nDateien sortieren\nKindle laden", "save": "Speichern",
        "view_kindle": "Kindle anzeigen", "empty": "Kein Inhalt", "empty_todo": "Keine Aufgaben",
        "refresh": "Aktualisieren", "weekly_total": "Wochensumme", "not_filled": "Nicht ausgefüllt",
        "hour": "Std.", "minute": "Min.", "break_short": "Pause",
    },
    "fr": {
        "weekdays": ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"],
        "mode_schedule": "Planning", "mode_notebook": "Notes", "mode_todo": "Tâches",
        "admin_title": "Administration KindleBoard", "kindle_page": "Page Kindle", "previous_week": "Semaine précédente",
        "next_week": "Semaine suivante", "monday_date": "Lundi", "open": "Ouvrir", "display_mode": "Mode",
        "language": "Langue", "schedule_title": "Planning personnel", "this_week": "Cette semaine", "total": "Total",
        "date": "Date", "start": "Début", "end": "Fin", "break_minutes": "Pause min",
        "status": "État", "note": "Note", "hours": "Heures", "rest": "Repos", "message": "Message",
        "week_note": "Message / note semaine", "notebook_title": "Notes", "notebook_content": "Texte",
        "notebook_placeholder": "Écrire un texte pour Kindle", "todo_title": "Liste de tâches",
        "todo_hint": "Une tâche par ligne. Touchez sur Kindle pour terminer.",
        "todo_placeholder": "Acheter du lait\nRanger les fichiers\nCharger Kindle", "save": "Enregistrer",
        "view_kindle": "Voir Kindle", "empty": "Aucun contenu", "empty_todo": "Aucune tâche",
        "refresh": "Actualiser", "weekly_total": "Total semaine", "not_filled": "Non rempli",
        "hour": "h", "minute": "min", "break_short": "pause",
    },
    "pt": {
        "weekdays": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
        "mode_schedule": "Escala", "mode_notebook": "Notas", "mode_todo": "Tarefas",
        "admin_title": "Admin KindleBoard", "kindle_page": "Página Kindle", "previous_week": "Semana anterior",
        "next_week": "Próxima semana", "monday_date": "Segunda", "open": "Abrir", "display_mode": "Modo",
        "language": "Idioma", "schedule_title": "Escala pessoal", "this_week": "Esta semana", "total": "Total",
        "date": "Data", "start": "Início", "end": "Fim", "break_minutes": "Pausa min",
        "status": "Estado", "note": "Nota", "hours": "Horas", "rest": "Descanso", "message": "Mensagem",
        "week_note": "Mensagem / nota semanal", "notebook_title": "Notas", "notebook_content": "Texto",
        "notebook_placeholder": "Escreva algo para o Kindle", "todo_title": "Lista de tarefas",
        "todo_hint": "Uma tarefa por linha. Toque no Kindle para concluir.",
        "todo_placeholder": "Comprar leite\nOrganizar arquivos\nCarregar Kindle", "save": "Salvar",
        "view_kindle": "Ver Kindle", "empty": "Sem conteúdo", "empty_todo": "Sem tarefas",
        "refresh": "Atualizar", "weekly_total": "Total semanal", "not_filled": "Não preenchido",
        "hour": "h", "minute": "min", "break_short": "pausa",
    },
}


def ensure_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        for default_db_path in DEFAULT_DB_PATHS:
            if os.path.abspath(default_db_path) != os.path.abspath(DB_PATH) and os.path.exists(default_db_path):
                shutil.copyfile(default_db_path, DB_PATH)
                break
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS weeks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_start TEXT NOT NULL UNIQUE,
                note TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_id INTEGER NOT NULL,
                work_date TEXT NOT NULL,
                start_time TEXT NOT NULL DEFAULT '',
                end_time TEXT NOT NULL DEFAULT '',
                break_minutes INTEGER NOT NULL DEFAULT 0,
                note TEXT NOT NULL DEFAULT '',
                is_day_off INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (week_id) REFERENCES weeks(id) ON DELETE CASCADE,
                UNIQUE (week_id, work_date)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL DEFAULT ''
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                sort_order INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL
            )
            """
        )


def monday_for(value=None):
    if value:
        current = datetime.strptime(value, "%Y-%m-%d").date()
    else:
        current = date.today()
    return current - timedelta(days=current.weekday())


def week_days(week_start):
    return [week_start + timedelta(days=index) for index in range(7)]


def minutes_between(start_text, end_text, break_minutes):
    if not start_text or not end_text:
        return 0
    try:
        start = datetime.strptime(start_text, "%H:%M")
        end = datetime.strptime(end_text, "%H:%M")
    except ValueError:
        return 0
    if end <= start:
        end += timedelta(days=1)
    worked = int((end - start).total_seconds() // 60) - int(break_minutes or 0)
    return max(worked, 0)


def valid_lang(lang):
    supported = {code for code, _label in LANGUAGES}
    return lang if lang in supported else "zh-CN"


def language_from_header(header_value):
    if not header_value:
        return "zh-CN"
    aliases = {
        "zh": "zh-CN",
        "zh-cn": "zh-CN",
        "zh-hans": "zh-CN",
        "zh-tw": "zh-TW",
        "zh-hk": "zh-TW",
        "zh-mo": "zh-TW",
        "zh-hant": "zh-TW",
        "en": "en",
        "ja": "ja",
        "ko": "ko",
        "es": "es",
        "de": "de",
        "fr": "fr",
        "pt": "pt",
    }
    choices = []
    for item in header_value.split(","):
        parts = [part.strip() for part in item.split(";")]
        code = parts[0].lower()
        quality = 1.0
        for part in parts[1:]:
            if part.startswith("q="):
                try:
                    quality = float(part[2:])
                except ValueError:
                    quality = 0.0
        choices.append((quality, code))
    for _quality, code in sorted(choices, reverse=True):
        mapped = aliases.get(code) or aliases.get(code.split("-")[0])
        if mapped:
            return mapped
    return "zh-CN"


def text(lang, key):
    lang = valid_lang(lang)
    return TEXT.get(lang, TEXT["zh-CN"]).get(key, TEXT["zh-CN"].get(key, key))


def mode_label(mode, lang):
    return text(lang, f"mode_{mode}")


def day_name(index, lang):
    return text(lang, "weekdays")[index]


def format_day(value, lang):
    if valid_lang(lang) in ("zh-CN", "zh-TW"):
        return value.strftime("%m月%d日")
    return value.strftime("%m/%d")


def format_hours(minutes, lang="zh-CN"):
    hours = minutes // 60
    rest = minutes % 60
    hour_label = text(lang, "hour")
    minute_label = text(lang, "minute")
    if rest == 0:
        return f"{hours} {hour_label}"
    return f"{hours} {hour_label} {rest} {minute_label}"


def db_connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    return conn


def load_settings(preferred_lang=None):
    ensure_db()
    defaults = {
        "mode": "schedule",
        "lang": valid_lang(preferred_lang or "zh-CN"),
        "notebook_text": "",
    }
    with db_connect() as conn:
        for row in conn.execute("SELECT key, value FROM settings"):
            defaults[row["key"]] = row["value"]
    if defaults["mode"] not in MODES:
        defaults["mode"] = "schedule"
    defaults["lang"] = valid_lang(defaults.get("lang", preferred_lang or "zh-CN"))
    return defaults


def save_settings(form):
    mode = form.get("mode", ["schedule"])[0]
    if mode not in MODES:
        mode = "schedule"
    lang = valid_lang(form.get("lang", ["zh-CN"])[0])
    values = {
        "mode": mode,
        "lang": lang,
        "notebook_text": form.get("notebook_text", [""])[0].strip(),
    }
    with db_connect() as conn:
        for key, value in values.items():
            conn.execute(
                """
                INSERT INTO settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                (key, value),
            )


def load_todos():
    ensure_db()
    with db_connect() as conn:
        rows = [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM todos ORDER BY completed ASC, sort_order ASC, id ASC"
            )
        ]
        if rows:
            return rows
        legacy = conn.execute(
            "SELECT value FROM settings WHERE key = 'todo_text'"
        ).fetchone()
        legacy_text = legacy["value"] if legacy else ""
        lines = [line.strip() for line in legacy_text.splitlines() if line.strip()]
        if not lines:
            return rows
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        for index, text in enumerate(lines):
            conn.execute(
                """
                INSERT INTO todos (text, completed, sort_order, updated_at)
                VALUES (?, 0, ?, ?)
                """,
                (text, index, now),
            )
        return [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM todos ORDER BY completed ASC, sort_order ASC, id ASC"
            )
        ]


def save_todos_from_text(todo_text):
    lines = [line.strip() for line in todo_text.splitlines() if line.strip()]
    now = datetime.utcnow().replace(microsecond=0).isoformat()
    with db_connect() as conn:
        existing = {}
        for row in conn.execute("SELECT text, completed FROM todos ORDER BY sort_order, id"):
            existing.setdefault(row["text"], []).append(row["completed"])
        conn.execute("DELETE FROM todos")
        for index, text in enumerate(lines):
            completed_values = existing.get(text) or [0]
            completed = completed_values.pop(0)
            conn.execute(
                """
                INSERT INTO todos (text, completed, sort_order, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (text, int(completed), index, now),
            )


def toggle_todo(todo_id):
    ensure_db()
    now = datetime.utcnow().replace(microsecond=0).isoformat()
    with db_connect() as conn:
        conn.execute(
            """
            UPDATE todos
            SET completed = CASE completed WHEN 1 THEN 0 ELSE 1 END,
                updated_at = ?
            WHERE id = ?
            """,
            (now, todo_id),
        )


def load_week(week_start):
    ensure_db()
    week_start_text = week_start.isoformat()
    with db_connect() as conn:
        week = conn.execute(
            "SELECT * FROM weeks WHERE week_start = ?", (week_start_text,)
        ).fetchone()
        shifts = {}
        if week:
            for row in conn.execute(
                "SELECT * FROM shifts WHERE week_id = ? ORDER BY work_date", (week["id"],)
            ):
                shifts[row["work_date"]] = dict(row)

    rows = []
    for index, work_day in enumerate(week_days(week_start)):
        key = work_day.isoformat()
        row = shifts.get(
            key,
            {
                "work_date": key,
                "start_time": "",
                "end_time": "",
                "break_minutes": 0,
                "note": "",
                "is_day_off": 0,
            },
        )
        row["day_name"] = day_name(index, "zh-CN")
        row["day_index"] = index
        row["minutes"] = 0 if row["is_day_off"] else minutes_between(
            row["start_time"], row["end_time"], row["break_minutes"]
        )
        rows.append(row)

    total_minutes = sum(row["minutes"] for row in rows)
    return {
        "week_start": week_start,
        "week_end": week_start + timedelta(days=6),
        "note": week["note"] if week else "",
        "rows": rows,
        "total_minutes": total_minutes,
    }


def save_week(week_start_text, form):
    ensure_db()
    week_start = monday_for(week_start_text)
    now = datetime.utcnow().replace(microsecond=0).isoformat()
    note = form.get("week_note", [""])[0].strip()
    with db_connect() as conn:
        conn.execute(
            """
            INSERT INTO weeks (week_start, note, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(week_start) DO UPDATE SET note = excluded.note, updated_at = excluded.updated_at
            """,
            (week_start.isoformat(), note, now),
        )
        week_id = conn.execute(
            "SELECT id FROM weeks WHERE week_start = ?", (week_start.isoformat(),)
        ).fetchone()["id"]
        for work_day in week_days(week_start):
            key = work_day.isoformat()
            is_day_off = 1 if key in form.get("day_off", []) else 0
            start_time = form.get(f"start_{key}", [""])[0].strip()
            end_time = form.get(f"end_{key}", [""])[0].strip()
            break_raw = form.get(f"break_{key}", ["0"])[0].strip() or "0"
            note_value = form.get(f"note_{key}", [""])[0].strip()
            try:
                break_minutes = max(int(break_raw), 0)
            except ValueError:
                break_minutes = 0
            conn.execute(
                """
                INSERT INTO shifts
                    (week_id, work_date, start_time, end_time, break_minutes, note, is_day_off)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(week_id, work_date) DO UPDATE SET
                    start_time = excluded.start_time,
                    end_time = excluded.end_time,
                    break_minutes = excluded.break_minutes,
                    note = excluded.note,
                    is_day_off = excluded.is_day_off
                """,
                (week_id, key, start_time, end_time, break_minutes, note_value, is_day_off),
            )
    return week_start


def html_page(title, body, css_path="/static/app.css", lang="zh-CN"):
    return f"""<!doctype html>
<html lang="{escape(valid_lang(lang))}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{escape(title)}</title>
  <link rel="stylesheet" href="{css_path}">
</head>
<body>
{body}
</body>
</html>"""


def admin_script():
    return """
<script>
(function () {
  function syncPanels() {
    var checked = document.querySelector('input[name="mode"]:checked');
    if (!checked) return;
    var mode = checked.value;
    document.querySelectorAll('.mode-button').forEach(function (label) {
      var input = label.querySelector('input[name="mode"]');
      label.classList.toggle('active', input && input.checked);
    });
    document.querySelectorAll('.module-panel').forEach(function (panel) {
      panel.hidden = panel.getAttribute('data-module') !== mode;
    });
  }
  document.querySelectorAll('input[name="mode"]').forEach(function (input) {
    input.addEventListener('change', syncPanels);
  });
  var languageSelect = document.querySelector('select[name="lang"]');
  if (languageSelect) {
    languageSelect.addEventListener('change', function () {
      var form = languageSelect.closest('form');
      if (form) form.submit();
    });
  }
  syncPanels();
})();
</script>
"""


def render_admin(week, settings, todos):
    lang = settings["lang"]
    previous_week = (week["week_start"] - timedelta(days=7)).isoformat()
    next_week = (week["week_start"] + timedelta(days=7)).isoformat()
    week_start = week["week_start"].isoformat()
    mode_options = []
    for value in MODES:
        checked = " checked" if settings["mode"] == value else ""
        active_class = " active" if settings["mode"] == value else ""
        mode_options.append(
            f'<label class="mode-button{active_class}"><input type="radio" name="mode" value="{value}"{checked}> {escape(mode_label(value, lang))}</label>'
        )
    language_options = []
    for code, label in LANGUAGES:
        selected = " selected" if lang == code else ""
        language_options.append(
            f'<option value="{escape(code)}"{selected}>{escape(label)}</option>'
        )
    todo_text = "\n".join(todo["text"] for todo in todos)
    rows = []
    for row in week["rows"]:
        work_date = row["work_date"]
        checked = " checked" if row["is_day_off"] else ""
        rows.append(
            f"""
          <tr>
            <th scope="row">
              <span>{escape(day_name(row["day_index"], lang))}</span>
              <small>{escape(work_date[5:])}</small>
            </th>
            <td><input type="time" name="start_{work_date}" value="{escape(row["start_time"])}"></td>
            <td><input type="time" name="end_{work_date}" value="{escape(row["end_time"])}"></td>
            <td><input class="short-input" type="number" min="0" step="5" name="break_{work_date}" value="{int(row["break_minutes"])}"></td>
            <td class="off-cell"><label><input type="checkbox" name="day_off" value="{work_date}"{checked}> {escape(text(lang, "rest"))}</label></td>
            <td><input type="text" name="note_{work_date}" value="{escape(row["note"])}" placeholder="{escape(text(lang, "note"))}"></td>
            <td class="hours">{format_hours(row["minutes"], lang) if row["minutes"] else "-"}</td>
          </tr>
            """
        )
    schedule_hidden = " hidden" if settings["mode"] != "schedule" else ""
    notebook_hidden = " hidden" if settings["mode"] != "notebook" else ""
    todo_hidden = " hidden" if settings["mode"] != "todo" else ""
    body = f"""
<main class="admin-shell">
  <header class="topbar">
    <div>
      <h1>KindleBoard</h1>
      <p class="version-line">{APP_VERSION}</p>
    </div>
    <nav>
      <a href="/kindle">{escape(text(lang, "kindle_page"))}</a>
    </nav>
  </header>

  <section class="week-strip">
    <a href="/admin?week_start={previous_week}">{escape(text(lang, "previous_week"))}</a>
    <form method="get" action="/admin">
      <label for="week_start">{escape(text(lang, "monday_date"))}</label>
      <input id="week_start" type="date" name="week_start" value="{week_start}">
      <button type="submit">{escape(text(lang, "open"))}</button>
    </form>
    <a href="/admin?week_start={next_week}">{escape(text(lang, "next_week"))}</a>
  </section>

  <form method="post" action="/admin" class="schedule-form">
    <input type="hidden" name="week_start" value="{week_start}">
    <section class="settings-panel">
      <h2>{escape(text(lang, "display_mode"))}</h2>
      <div class="mode-options">
        {''.join(mode_options)}
      </div>
      <label class="language-select">
        <span>{escape(text(lang, "language"))}</span>
        <select name="lang">
          {''.join(language_options)}
        </select>
      </label>
    </section>

    <section class="module-panel" id="schedule-module" data-module="schedule"{schedule_hidden}>
      <h2>{escape(text(lang, "schedule_title"))}</h2>
      <div class="summary-band">
      <div>
        <span>{escape(text(lang, "this_week"))}</span>
        <strong>{format_day(week["week_start"], lang)} - {format_day(week["week_end"], lang)}</strong>
      </div>
      <div>
        <span>{escape(text(lang, "total"))}</span>
        <strong>{format_hours(week["total_minutes"], lang)}</strong>
      </div>
      </div>

      <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>{escape(text(lang, "date"))}</th>
            <th>{escape(text(lang, "start"))}</th>
            <th>{escape(text(lang, "end"))}</th>
            <th>{escape(text(lang, "break_minutes"))}</th>
            <th>{escape(text(lang, "status"))}</th>
            <th>{escape(text(lang, "note"))}</th>
            <th>{escape(text(lang, "hours"))}</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
      </div>

      <label class="note-box">
      <span>{escape(text(lang, "week_note"))}</span>
      <textarea name="week_note" rows="3">{escape(week["note"])}</textarea>
      </label>
    </section>

    <section class="module-panel" id="notebook-module" data-module="notebook"{notebook_hidden}>
      <h2>{escape(text(lang, "notebook_title"))}</h2>
      <label class="note-box module-note">
        <span>{escape(text(lang, "notebook_content"))}</span>
        <textarea name="notebook_text" rows="7" placeholder="{escape(text(lang, "notebook_placeholder"))}">{escape(settings["notebook_text"])}</textarea>
      </label>
    </section>

    <section class="module-panel" id="todo-module" data-module="todo"{todo_hidden}>
      <h2>{escape(text(lang, "todo_title"))}</h2>
      <label class="note-box module-note">
        <span>{escape(text(lang, "todo_hint"))}</span>
        <textarea name="todo_text" rows="7" placeholder="{escape(text(lang, "todo_placeholder"))}">{escape(todo_text)}</textarea>
      </label>
    </section>

    <div class="actions">
      <button type="submit">{escape(text(lang, "save"))}</button>
      <a href="/kindle?week_start={week_start}">{escape(text(lang, "view_kindle"))}</a>
    </div>
  </form>
  <p class="app-version">KindleBoard {APP_VERSION}</p>
</main>
{admin_script()}
"""
    return html_page(text(lang, "admin_title"), body, lang=lang)


def render_kindle_schedule(week, lang):
    rows = []
    for row in week["rows"]:
        if row["is_day_off"]:
            main_text = text(lang, "rest")
            hours_text = ""
        elif row["start_time"] and row["end_time"]:
            main_text = f"{row['start_time']} - {row['end_time']}"
            if row["break_minutes"]:
                main_text += f" / {text(lang, 'break_short')} {int(row['break_minutes'])} {text(lang, 'minute')}"
            hours_text = format_hours(row["minutes"], lang)
        else:
            main_text = text(lang, "not_filled")
            hours_text = ""
        note = f"<p>{escape(row['note'])}</p>" if row["note"] else ""
        rows.append(
            f"""
      <section class="kindle-row">
        <div class="date">
          <b>{escape(day_name(row["day_index"], lang))}</b>
          <span>{escape(row["work_date"][5:])}</span>
        </div>
        <div class="shift">
          <strong>{escape(main_text)}</strong>
          {note}
        </div>
        <div class="row-hours">{escape(hours_text)}</div>
      </section>
            """
        )
    message = (
        f"<section class=\"kindle-message\"><span>{escape(text(lang, 'message'))}</span><p>{escape(week['note'])}</p></section>"
        if week["note"]
        else ""
    )
    refresh_href = f"/kindle?week_start={week['week_start'].isoformat()}"
    return f"""
  <header>
    <a class="refresh-link" href="{refresh_href}">{escape(text(lang, "refresh"))}</a>
    <p>{format_day(week["week_start"], lang)} - {format_day(week["week_end"], lang)}</p>
    <h1>{escape(mode_label("schedule", lang))}</h1>
  </header>
  {message}
  <div class="kindle-list">
    {''.join(rows)}
  </div>
  <footer>
    <span>{escape(text(lang, "weekly_total"))}</span>
    <strong>{format_hours(week["total_minutes"], lang)}</strong>
    <small>KindleBoard {APP_VERSION}</small>
  </footer>
"""


def render_kindle_notebook(settings):
    lang = settings["lang"]
    note_text = settings["notebook_text"] or text(lang, "empty")
    return f"""
  <header>
    <a class="refresh-link" href="/kindle">{escape(text(lang, "refresh"))}</a>
    <p>{escape(mode_label("notebook", lang))}</p>
    <h1>{escape(mode_label("notebook", lang))}</h1>
  </header>
  <section class="kindle-note-page">{escape(note_text)}</section>
  <footer class="simple-footer"><small>KindleBoard {APP_VERSION}</small></footer>
"""


def render_kindle_todo(todos, lang):
    if not todos:
        items = f'<li><span class="todo-box"></span><strong>{escape(text(lang, "empty_todo"))}</strong></li>'
    else:
        rows = []
        for todo in todos:
            done_class = " completed" if todo["completed"] else ""
            box_text = "X" if todo["completed"] else ""
            rows.append(
                f"""
    <li class="{done_class.strip()}">
      <a class="todo-toggle" href="/todo-toggle?id={int(todo["id"])}">
        <span class="todo-box">{box_text}</span>
        <strong>{escape(todo["text"])}</strong>
      </a>
    </li>
                """
            )
        items = "".join(rows)
    return f"""
  <header>
    <a class="refresh-link" href="/kindle">{escape(text(lang, "refresh"))}</a>
    <p>{escape(mode_label("todo", lang))}</p>
    <h1>{escape(mode_label("todo", lang))}</h1>
  </header>
  <ol class="kindle-todo-list">
    {items}
  </ol>
  <footer class="simple-footer"><small>KindleBoard {APP_VERSION}</small></footer>
"""


def render_kindle(week, settings, todos):
    lang = settings["lang"]
    if settings["mode"] == "notebook":
        content = render_kindle_notebook(settings)
    elif settings["mode"] == "todo":
        content = render_kindle_todo(todos, lang)
    else:
        content = render_kindle_schedule(week, lang)
    body = f"""
<main class="kindle-page">
{content}
</main>
"""
    return html_page(mode_label(settings["mode"], lang), body, "/static/kindle.css", lang=lang)


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        preferred_lang = language_from_header(self.headers.get("Accept-Language", ""))
        if parsed.path == "/":
            self.redirect("/admin")
            return
        if parsed.path == "/admin":
            week = load_week(monday_for(query.get("week_start", [None])[0]))
            self.send_html(render_admin(week, load_settings(preferred_lang), load_todos()))
            return
        if parsed.path == "/kindle":
            week = load_week(monday_for(query.get("week_start", [None])[0]))
            self.send_html(render_kindle(week, load_settings(preferred_lang), load_todos()))
            return
        if parsed.path == "/todo-toggle":
            try:
                todo_id = int(query.get("id", ["0"])[0])
            except ValueError:
                todo_id = 0
            if todo_id:
                toggle_todo(todo_id)
            self.redirect("/kindle")
            return
        if parsed.path == "/static/app.css":
            self.send_static("static/app.css", "text/css; charset=utf-8")
            return
        if parsed.path == "/static/kindle.css":
            self.send_static("static/kindle.css", "text/css; charset=utf-8")
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/admin":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        form = parse_qs(body, keep_blank_values=True)
        save_settings(form)
        save_todos_from_text(form.get("todo_text", [""])[0])
        week_start = save_week(form.get("week_start", [date.today().isoformat()])[0], form)
        self.redirect(f"/admin?week_start={week_start.isoformat()}")

    def send_html(self, content):
        raw = content.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def send_static(self, path, content_type):
        try:
            with open(path, "rb") as file:
                raw = file.read()
        except FileNotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def redirect(self, location):
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", location)
        self.end_headers()

    def log_message(self, format_text, *args):
        print("%s - %s" % (self.address_string(), format_text % args))


if __name__ == "__main__":
    ensure_db()
    server = ThreadingHTTPServer(("0.0.0.0", PORT), AppHandler)
    print(f"Serving on http://0.0.0.0:{PORT}")
    server.serve_forever()
