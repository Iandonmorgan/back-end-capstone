import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import Composition, model_factory
from ..connection import Connection


def get_composition(composition_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Composition)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.title,
            c.alt_titles,
            c.lyrics,
            c.notes,
            c.date_created,
            STRFTIME('%m/%d/%Y',c.date_created) as date_refactored,
            c.user_id
        FROM songwrytrapp_composition c
        WHERE c.id = ?
        """, (composition_id,))

        return db_cursor.fetchone()

def get_composition_writers(composition_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Composition)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            w.id,
            w.first_name,
            w.last_name,
            w.user_id,
            cw.percentage,
            cw.id as compositionwriter_id
        FROM songwrytrapp_composition c
        JOIN songwrytrapp_compositionwriter cw
        ON cw.composition_id = c.id
        JOIN songwrytrapp_writer w
        ON w.id = cw.writer_id
        WHERE c.id = ?
        ORDER BY w.last_name
        """, (composition_id,))

        return db_cursor.fetchall()

def get_composition_publishers(composition_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Composition)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pc.id,
            pc.user_id,
            pc.name,
            pc.pro_id,
            pc.pro_acct_num,
            pc.admin,
            cpc.percentage,
            cpc.pro_work_num,
            p.name as pro,
            cpc.id as compositionpublishing_id
        FROM songwrytrapp_publishingcompany pc
        JOIN songwrytrapp_pro p
        ON pc.pro_id = p.id
        JOIN songwrytrapp_compositionpublishing cpc
        ON cpc.publishing_company_id = pc.id
        JOIN songwrytrapp_composition c
        ON c.id = cpc.composition_id
        WHERE c.id = ?
        ORDER BY pc.name
        """, (composition_id,))

        return db_cursor.fetchall()

def get_composition_recordings(composition_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Composition)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            r.id,
            r.user_id,
            r.audio_url,
            r.producer,
            r.artist,
            r.recording_type,
            r.date_recorded,
            r.is_mixed,
            r.is_mastered,
            r.is_delivered,
            r.composition_id,
            r.image_url,
            r.ownership_split,
            STRFTIME('%m/%d/%Y',r.date_recorded) as date_refactored
        FROM songwrytrapp_composition c
        JOIN songwrytrapp_recording r
        ON r.composition_id = c.id
        WHERE c.id = ?
        ORDER BY r.date_recorded
        """, (composition_id,))

        return db_cursor.fetchall()

@login_required
def composition_details(request, composition_id):
    if request.method == 'GET':
        composition = get_composition(composition_id)
        composition_writers = get_composition_writers(composition_id)
        composition_publishingcompanies = get_composition_publishers(composition_id)
        composition_recordings = get_composition_recordings(composition_id)
        template = 'compositions/detail.html'
        context = {
            'composition': composition,
            'composition_writers': composition_writers,
            'composition_publishingcompanies': composition_publishingcompanies,
            'composition_recordings': composition_recordings
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST
        composition_writers = get_composition_writers(composition_id)
        composition_publishingcompanies = get_composition_publishers(composition_id)
        composition_recordings = get_composition_recordings(composition_id)
        # Check if this POST is for deleting a composition
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                for cw in composition_writers:
                    db_cursor.execute("""
                    DELETE FROM songwrytrapp_compositionwriter
                    WHERE id = ?
                    """, (cw.compositionwriter_id,))
                for cpc in composition_publishingcompanies:
                    db_cursor.execute("""
                    DELETE FROM songwrytrapp_compositionpublishing
                    WHERE id = ?
                    """, (cpc.compositionpublishing_id,))
                for cr in composition_recordings:
                    db_cursor.execute("""
                    DELETE FROM songwrytrapp_recording
                    WHERE id = ?
                    """, (cr.id,))
                db_cursor.execute("""
                DELETE FROM songwrytrapp_composition
                WHERE id = ?
                """, (composition_id,))

            return redirect(reverse('songwrytrapp:compositions'))
        # Check if this POST is for editing a composition
        elif (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE songwrytrapp_composition
                SET title = ?,
                    alt_titles = ?,
                    lyrics = ?,
                    notes = ?,
                    date_created = ?
                WHERE id = ?
                """,
                (
                    form_data['title'], form_data['alt_titles'],
                    form_data['lyrics'], form_data['notes'],
                    form_data['date_created'], 
                    composition_id,
                ))

            return redirect(reverse('songwrytrapp:composition', args=[composition_id]))