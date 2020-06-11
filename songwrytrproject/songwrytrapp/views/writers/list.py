import sqlite3
from django.shortcuts import render
from songwrytrapp.models import Writer
from ..connection import Connection


def writer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                w.*
            FROM songwrytrapp_writer w
            """)

            all_writers = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                writer = Writer()
                writer.id = row['id']
                writer.first_name = row['first_name']
                writer.last_name = row['last_name']
                writer.publishing_notes = row['publishing_notes']
                writer.user_id = row['user_id']

                all_writers.append(writer)

        template = 'writers/list.html'
        context = {
            'all_writers': all_writers
        }

        return render(request, template, context)