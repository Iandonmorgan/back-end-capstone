import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import Composition, Writer, model_factory
from ..connection import Connection
from .details import get_composition, get_composition_writers

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

def get_writers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Writer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            w.*
        FROM songwrytrapp_writer w
        ORDER BY w.last_name
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

@login_required
def composition_writer_form(request, composition_id):

    if request.method == 'GET':
        composition = get_composition(composition_id)
        composition_writers = get_composition_writers(composition_id)
        all_writers = get_writers()
        template = 'compositions/writer_form.html'
        context = {
            'composition': composition,
            'all_writers': all_writers
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST
        # Check if this POST is for deleting a composition
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM songwrytrapp_compositionwriter
                WHERE id = ?
                """, (composition_id,))

            return redirect(reverse('songwrytrapp:compositions'))
        else:
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                INSERT INTO songwrytrapp_compositionwriter
                (
                    writer_id, percentage, composition_id
                )
                VALUES (?, ?, ?)
                """,
                (form_data['writer'], form_data['percentage'],
                    composition_id))

            return redirect(reverse('songwrytrapp:compositions'))