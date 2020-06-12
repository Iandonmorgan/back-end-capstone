import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import Writer, model_factory
from ..connection import Connection


def get_writers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Writer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            w.*
        FROM songwrytrapp_writer w
        """)

        return db_cursor.fetchall()

@login_required
def writer_form(request):
    if request.method == 'GET':
        writers = get_writers()
        template = 'writers/form.html'
        context = {
            'all_writers': writers
        }

        return render(request, template, context)