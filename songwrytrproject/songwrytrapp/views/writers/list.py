import sqlite3
from django.shortcuts import render, redirect, reverse
from songwrytrapp.models import Writer
from ..connection import Connection
from songwrytrapp.models import model_factory
from django.contrib.auth.decorators import login_required

@login_required
def writer_list(request):
    if request.method == 'GET':
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
            ORDER BY w.last_name
            """)

            all_writers = db_cursor.fetchall()

        template = 'writers/list.html'
        context = {
            'all_writers': all_writers
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO songwrytrapp_writer
            (
                first_name, last_name, pro_id, pro_ipi, publishing_notes, user_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (form_data['first_name'], form_data['last_name'],
                form_data['pro'], form_data['pro_ipi'],
                form_data['publishing_notes'],
                request.user.id))

        return redirect(reverse('songwrytrapp:writers'))