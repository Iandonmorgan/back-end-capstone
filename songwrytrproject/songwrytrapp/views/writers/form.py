import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import Writer, PRO, model_factory
from ..connection import Connection
from .details import get_writer


def get_writers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Writer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            w.*,
            p.name as 'PRO_Name',
            p.city as 'PRO_City',
            p.state as 'PRO_State',
            p.zipcode as 'PRO_Zipcode'
        FROM songwrytrapp_writer w
        JOIN songwrytrapp_pro p
        ON w.pro_id = p.id
        """)

        return db_cursor.fetchall()

def get_pros():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(PRO)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.*
        FROM songwrytrapp_pro p
        """)

        return db_cursor.fetchall()

@login_required
def writer_form(request):
    if request.method == 'GET':
        writers = get_writers()
        pros = get_pros()
        template = 'writers/form.html'
        context = {
            'all_writers': writers,
            'all_pros': pros
        }

        return render(request, template, context)

@login_required
def writer_edit_form(request, writer_id):

    if request.method == 'GET':
        writer = get_writer(writer_id)
        writers = get_writers()
        pros = get_pros()
        template = 'writers/form.html'
        context = {
            'writer': writer,
            'all_writers': writers,
            'all_pros': pros
        }

        return render(request, template, context)