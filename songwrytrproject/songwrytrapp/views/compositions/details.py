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

@login_required
def composition_details(request, composition_id):
    if request.method == 'GET':
        composition = get_composition(composition_id)

        template = 'compositions/detail.html'
        context = {
            'composition': composition
        }

        return render(request, template, context)
    if request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for deleting a composition
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM songwrytrapp_composition
                WHERE id = ?
                """, (composition_id,))

            return redirect(reverse('songwrytrapp:compositions'))
        # Check if this POST is for editing a composition
        if (
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

            return redirect(reverse('songwrytrapp:compositions'))