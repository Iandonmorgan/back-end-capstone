import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import Writer, model_factory
from ..connection import Connection


def get_writer(writer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Writer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            w.id,
            w.user_id,
            w.first_name,
            w.last_name,
            w.publishing_notes,
            w.pro_id,
            w.pro_ipi
        FROM songwrytrapp_writer w
        WHERE w.id = ?
        """, (writer_id,))

        return db_cursor.fetchone()

def get_composition_writers(writer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Writer)
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
        WHERE w.id = ?
        ORDER BY w.last_name
        """, (writer_id,))

        return db_cursor.fetchall()

@login_required
def writer_details(request, writer_id):
    if request.method == 'GET':
        writer = get_writer(writer_id)

        template = 'writers/detail.html'
        context = {
            'writer': writer
        }

        return render(request, template, context)
    if request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for deleting a writer
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                composition_writers = get_composition_writers(writer_id)
                for cw in composition_writers:
                    db_cursor.execute("""
                    DELETE FROM songwrytrapp_compositionwriter
                    WHERE id = ?
                    """, (cw.compositionwriter_id,))
                db_cursor.execute("""
                DELETE FROM songwrytrapp_writer
                WHERE id = ?
                """, (writer_id,))

            return redirect(reverse('songwrytrapp:writers'))
        # Check if this POST is for editing a writer
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE songwrytrapp_writer
                SET first_name = ?,
                    last_name = ?,
                    pro_id = ?,
                    pro_ipi = ?,
                    publishing_notes = ?
                WHERE id = ?
                """,
                (
                    form_data['first_name'], form_data['last_name'],
                    form_data['pro'], form_data['pro_ipi'],
                    form_data['publishing_notes'], 
                    writer_id,
                ))

            return redirect(reverse('songwrytrapp:writer', args=[writer_id]))