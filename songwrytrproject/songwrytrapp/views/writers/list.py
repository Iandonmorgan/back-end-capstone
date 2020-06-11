import sqlite3
from django.shortcuts import render
from songwrytrapp.models import Writer
from ..connection import Connection
from songwrytrapp.models import model_factory

def writer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Writer)
            
            db_cursor = conn.cursor()
            db_cursor.execute("""
            SELECT
                w.*
            FROM songwrytrapp_writer w
            """)

            all_writers = db_cursor.fetchall()

        template = 'writers/list.html'
        context = {
            'all_writers': all_writers
        }

        return render(request, template, context)