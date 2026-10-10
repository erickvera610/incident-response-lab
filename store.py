"""SQLite incident records with transactional events and optimistic concurrency."""
import sqlite3, json
from pathlib import Path
from datetime import datetime, timezone
from core import transition

class Conflict(ValueError):
    pass

class IncidentStore:

    def __init__(self, path='incidents.db'):
        self.path = str(path)
        self.initialize()

    def connect(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        return db

    def initialize(self):
        with self.connect() as db:
            db.executescript('CREATE TABLE IF NOT EXISTS incidents(id INTEGER PRIMARY KEY,title TEXT NOT NULL,service TEXT NOT NULL,severity TEXT NOT NULL,state TEXT NOT NULL,version INTEGER NOT NULL,created_at TEXT NOT NULL); CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,incident_id INTEGER NOT NULL REFERENCES incidents(id),state TEXT NOT NULL,version INTEGER NOT NULL,request_key TEXT NOT NULL,created_at TEXT NOT NULL,UNIQUE(incident_id,request_key));')

    def list(self):
        with self.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT * FROM incidents ORDER BY id DESC')]
            for r in rows:
                r['history'] = [dict(e) for e in db.execute('SELECT state,version,created_at FROM events WHERE incident_id=? ORDER BY version', (r['id'],))]
            return rows

    def create(self, title, service, severity):
        if not isinstance(title, str) or not 1 <= len(title.strip()) <= 120:
            raise ValueError('Title must be 1–120 characters')
        if service not in ['API', 'Database', 'Web'] or severity not in ['High', 'Medium', 'Low']:
            raise ValueError('Unknown service or severity')
        now = datetime.now(timezone.utc).isoformat()
        with self.connect() as db:
            cursor = db.execute('INSERT INTO incidents(title,service,severity,state,version,created_at) VALUES(?,?,?,?,?,?)', (title.strip(), service, severity, 'Open', 1, now))
            ident = cursor.lastrowid
            db.execute('INSERT INTO events(incident_id,state,version,request_key,created_at) VALUES(?,?,?,?,?)', (ident, 'Open', 1, 'creation', now))
        return next((r for r in self.list() if r['id'] == ident))

    def move(self, ident, new, version, request_key):
        if not isinstance(request_key, str) or not 1 <= len(request_key) <= 100:
            raise ValueError('Request key required, max 100 characters')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT * FROM incidents WHERE id=?', (ident,)).fetchone()
            if row is None:
                raise ValueError('Incident not found')
            previous = db.execute('SELECT state,version FROM events WHERE incident_id=? AND request_key=?', (ident, request_key)).fetchone()
            if previous:
                if previous['state'] != new or previous['version'] != version + 1:
                    raise Conflict('Request key reused with different event')
            else:
                if row['version'] != version:
                    raise Conflict('Stale version; refresh before changing state')
                transition(row['state'], new)
                now = datetime.now(timezone.utc).isoformat()
                db.execute('UPDATE incidents SET state=?,version=version+1 WHERE id=?', (new, ident))
                db.execute('INSERT INTO events(incident_id,state,version,request_key,created_at) VALUES(?,?,?,?,?)', (ident, new, version + 1, request_key, now))
        return next((r for r in self.list() if r['id'] == ident))
