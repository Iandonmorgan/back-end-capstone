import sqlite3
from django.shortcuts import render, redirect, reverse
from songwrytrapp.models import Composition, model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required

@login_required
def composition_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Composition)
            
            db_cursor = conn.cursor()
            db_cursor.execute("""
            SELECT
                c.id,
                c.user_id,
                c.title,
                c.alt_titles,
                c.lyrics,
                c.notes,
                c.date_created
            FROM songwrytrapp_composition c
            ORDER BY c.title
            """)

            all_compositions = db_cursor.fetchall()

        template = 'compositions/list.html'
        context = {
            'all_compositions': all_compositions
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO songwrytrapp_composition
            (
                title, alt_titles, lyrics, notes, date_created, user_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (form_data['title'], form_data['alt_titles'],
                form_data['lyrics'], form_data['notes'],
                form_data['date_created'],
                request.user.id))

        return redirect(reverse('songwrytrapp:compositions'))