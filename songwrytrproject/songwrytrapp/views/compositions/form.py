import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import Composition, model_factory
from ..connection import Connection
from .details import get_composition


def get_compositions():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Composition)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.*
        FROM songwrytrapp_composition c
        """)

        return db_cursor.fetchall()

@login_required
def composition_form(request):
    if request.method == 'GET':
        compositions = get_compositions()
        template = 'compositions/form.html'
        context = {
            'all_compositions': compositions
        }

        return render(request, template, context)

@login_required
def composition_edit_form(request, composition_id):

    if request.method == 'GET':
        composition = get_composition(composition_id)
        compositions = get_compositions()
        template = 'compositions/form.html'
        context = {
            'composition': composition,
            'all_compositions': compositions
        }

        return render(request, template, context)