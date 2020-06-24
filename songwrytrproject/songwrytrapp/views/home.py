import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import Recording, Composition, CompositionWriter, CompositionPublishing, model_factory
from .connection import Connection

def get_recent_recordings(request):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Recording)
        user_id = request.user.id
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            r.user_id,
            r.audio_url,
            r.producer,
            r.artist,
            r.recording_type,
            r.date_recorded,
            r.composition_id,
            r.image_url,
            r.is_mixed,
            r.is_mastered,
            r.is_delivered,
            c.title,
            STRFTIME('%m/%d/%Y',r.date_recorded) as date_refactored
        FROM songwrytrapp_composition c
        JOIN songwrytrapp_recording r
        ON r.composition_id = c.id
        WHERE r.user_id = ?
        ORDER BY r.date_recorded DESC
        LIMIT 5
        """, (user_id,))

        return db_cursor.fetchall()

def get_recent_compositions(request):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Composition)
        user_id = request.user.id
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            c.id,
            c.title,
            STRFTIME('%m/%d/%Y',c.date_created) as date_refactored,
            c.user_id
        FROM songwrytrapp_composition c
        WHERE c.user_id = ?
        ORDER BY c.date_created DESC
        LIMIT 5
        """, (user_id,))

        return db_cursor.fetchall()

def get_all_composition_writers(request):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(CompositionWriter)
        user_id = request.user.id
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            cw.id,
            cw.writer_id,
            cw.composition_id,
            w.user_id,
            w.first_name,
            w.last_name
        FROM songwrytrapp_compositionwriter cw
        JOIN songwrytrapp_writer w
        ON w.id = cw.writer_id
        WHERE w.user_id = ?
        """, (user_id,))

        return db_cursor.fetchall()

def get_all_composition_publishing(request):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(CompositionPublishing)
        user_id = request.user.id
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            cp.id,
            cp.publishing_company_id,
            cp.composition_id,
            pc.user_id,
            pc.name
        FROM songwrytrapp_compositionpublishing cp
        JOIN songwrytrapp_publishingcompany pc
        ON pc.id = cp.publishing_company_id
        WHERE pc.user_id = ?
        """, (user_id,))

        return db_cursor.fetchall()

@login_required
def home(request):
    if request.method == 'GET':
        recent_recordings = get_recent_recordings(request)
        recent_compositions = get_recent_compositions(request)
        all_composition_writers = get_all_composition_writers(request)
        all_composition_publishing = get_all_composition_publishing(request)
        template = 'home.html'
        context = {
            'recent_recordings': recent_recordings,
            'recent_compositions': recent_compositions,
            'all_composition_writers': all_composition_writers,
            'all_composition_publishing': all_composition_publishing
        }

        return render(request, template, context)
