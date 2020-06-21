import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import Composition, Writer, Recording, model_factory
from ..connection import Connection
from .details import get_composition, get_composition_writers, get_composition_publishers, get_composition_recordings
from django.utils.datastructures import MultiValueDictKeyError

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

def get_publishers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Writer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pc.*
        FROM songwrytrapp_publishingcompany pc
        ORDER BY pc.name
        """)

        return db_cursor.fetchall()

def get_recording(recording_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Recording)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            r.*
        FROM songwrytrapp_recording r
        WHERE id = ?
        """, (recording_id,))

        return db_cursor.fetchone()

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

@login_required
def composition_publishing_form(request, composition_id):

    if request.method == 'GET':
        composition = get_composition(composition_id)
        composition_publishers = get_composition_publishers(composition_id)
        all_publishers = get_publishers()
        template = 'compositions/publishing_form.html'
        context = {
            'composition': composition,
            'all_publishers': all_publishers,
            'composition_publishers': composition_publishers
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
                DELETE FROM songwrytrapp_compositionpublishing
                WHERE id = ?
                """, (composition_id,))

            return redirect(reverse('songwrytrapp:compositions'))
        else:
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                INSERT INTO songwrytrapp_compositionpublishing
                (
                    publishing_company_id, percentage, pro_work_num, composition_id
                )
                VALUES (?, ?, ?, ?)
                """,
                (form_data['publishingcompany'], form_data['percentage'],
                    form_data['pro_work_num'], composition_id))

            return redirect(reverse('songwrytrapp:compositions'))

@login_required
def composition_recording_form(request, composition_id):

    if request.method == 'GET':
        composition = get_composition(composition_id)
        composition_recordings = get_composition_recordings(composition_id)
        template = 'compositions/recording_form.html'
        context = {
            'composition': composition,
            'composition_recordings': composition_recordings
        }
        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            try:
                is_mixed = form_data["is_mixed"]
            except MultiValueDictKeyError:
                is_mixed = "off"
            try:
                is_mastered = form_data["is_mastered"]
            except MultiValueDictKeyError:
                is_mastered = "off"
            try:
                is_delivered = form_data["is_delivered"]
            except MultiValueDictKeyError:
                is_delivered = "off"
            db_cursor.execute("""
            INSERT INTO songwrytrapp_recording
            (
                audio_url, image_url, producer, artist, recording_type, date_recorded, is_mixed, is_mastered, is_delivered, ownership_split, user_id, composition_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (form_data['audio_url'], form_data['image_url'],
                form_data['producer'], form_data['artist'],
                form_data['recording_type'], form_data['date_recorded'],
                is_mixed, is_mastered, is_delivered,
                form_data['ownership_split'], request.user.id, composition_id))

        return redirect(reverse('songwrytrapp:composition', args=[composition_id]))

@login_required
def composition_recording_edit_form(request, composition_id, recording_id):

    if request.method == 'GET':
        composition = get_composition(composition_id)
        composition_recordings = get_composition_recordings(composition_id)
        recording = get_recording(recording_id)
        template = 'compositions/recording_form.html'
        context = {
            'composition': composition,
            'composition_recordings': composition_recordings,
            'recording': recording
        }
        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                try:
                    is_mixed = form_data["is_mixed"]
                except MultiValueDictKeyError:
                    is_mixed = "off"
                try:
                    is_mastered = form_data["is_mastered"]
                except MultiValueDictKeyError:
                    is_mastered = "off"
                try:
                    is_delivered = form_data["is_delivered"]
                except MultiValueDictKeyError:
                    is_delivered = "off"
                db_cursor.execute("""
                UPDATE songwrytrapp_recording
                SET audio_url = ?,
                    image_url = ?,
                    producer = ?,
                    artist = ?,
                    recording_type = ?,
                    date_recorded = ?,
                    is_mixed = ?,
                    is_mastered = ?,
                    is_delivered = ?,
                    ownership_split = ?
                WHERE id = ?
                """,
                (
                    form_data['audio_url'], form_data['image_url'],
                    form_data['producer'], form_data['artist'],
                    form_data['recording_type'], form_data['date_recorded'],
                    is_mixed, is_mastered, is_delivered,
                    form_data['ownership_split'], recording_id,
                ))

            return redirect(reverse('songwrytrapp:composition', args=[composition_id]))

@login_required
def composition_recording_delete(request, composition_id, recording_id):

    if request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM songwrytrapp_recording
                WHERE id = ?
                """, (recording_id,))

            return redirect(reverse('songwrytrapp:composition', args=[composition_id]))