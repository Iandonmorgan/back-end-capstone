import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import Composition, Writer, Recording, CompositionPublishing, CompositionWriter, model_factory
from ..connection import Connection
from .details import get_composition, get_composition_writers, get_composition_publishers, get_composition_recordings
from django.utils.datastructures import MultiValueDictKeyError

def get_compositions():
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
        """)

        return db_cursor.fetchall()

def get_writers():
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

        return db_cursor.fetchall()

def get_publishers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Writer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pc.id,
            pc.user_id,
            pc.name,
            pc.pro_id,
            pc.pro_acct_num,
            pc.admin
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
            r.id,
            r.user_id,
            r.audio_url,
            r.producer,
            r.artist,
            r.recording_type,
            r.date_recorded,
            r.is_mixed,
            r.is_mastered,
            r.is_delivered,
            r.composition_id,
            r.image_url,
            r.ownership_split
        FROM songwrytrapp_recording r
        WHERE id = ?
        """, (recording_id,))

        return db_cursor.fetchone()

def get_compositionpublishing(compositionpublishing_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(CompositionPublishing)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            cp.id,
            cp.composition_id,
            cp.publishing_company_id,
            cp.percentage,
            cp.pro_work_num
        FROM songwrytrapp_compositionpublishing cp
        WHERE cp.id = ?
        """, (compositionpublishing_id,))

        return db_cursor.fetchone()

def get_compositionwriter(compositionwriter_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(CompositionWriter)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            cw.id,
            cw.composition_id,
            cw.writer_id,
            cw.percentage
        FROM songwrytrapp_compositionwriter cw
        WHERE cw.id = ?
        """, (compositionwriter_id,))

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
        totalpct = 100
        for cw in composition_writers:
            totalpct -= cw.percentage
        template = 'compositions/writer_form.html'
        context = {
            'composition': composition,
            'all_writers': all_writers,
            'totalpct': totalpct
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

            return redirect(reverse('songwrytrapp:composition', args=[composition_id]))
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

            return redirect(reverse('songwrytrapp:composition', args=[composition_id]))

@login_required
def composition_writer_edit_form(request, composition_id, compositionwriter_id):

    if request.method == 'GET':
        composition = get_composition(composition_id)
        composition_writers = get_composition_writers(composition_id)
        all_writers = get_writers()
        compositionwriter = get_compositionwriter(compositionwriter_id)
        totalpct = 100
        for cw in composition_writers:
            totalpct -= cw.percentage
        totalpct += compositionwriter.percentage
        template = 'compositions/writer_form.html'
        context = {
            'composition': composition,
            'all_writers': all_writers,
            'totalpct': totalpct,
            'compositionwriter': compositionwriter
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST
        # Check if this POST is for editing a composition writer share
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            UPDATE songwrytrapp_compositionwriter
                SET writer_id = ?,
                    percentage = ?,
                    composition_id = ?
                WHERE id = ?
                """,
                (
                    form_data['writer'], form_data['percentage'],
                    composition_id, compositionwriter_id
                ))

        return redirect(reverse('songwrytrapp:composition', args=[composition_id]))

@login_required
def composition_publishing_form(request, composition_id):

    if request.method == 'GET':
        composition = get_composition(composition_id)
        composition_publishers = get_composition_publishers(composition_id)
        all_publishers = get_publishers()
        totalpct = 100
        for cp in composition_publishers:
            totalpct -= cp.percentage
        template = 'compositions/publishing_form.html'
        context = {
            'composition': composition,
            'all_publishers': all_publishers,
            'composition_publishers': composition_publishers,
            'totalpct': totalpct
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST
        # Check if this POST is for deleting a composition publishing company share
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

            return redirect(reverse('songwrytrapp:composition', args=[composition_id]))

@login_required
def composition_publishing_edit_form(request, composition_id, compositionpublishing_id):

    if request.method == 'GET':
        composition = get_composition(composition_id)
        composition_publishers = get_composition_publishers(composition_id)
        all_publishers = get_publishers()
        compositionpublishing = get_compositionpublishing(compositionpublishing_id)
        totalpct = 100
        for cp in composition_publishers:
            totalpct -= cp.percentage
        totalpct += compositionpublishing.percentage
        template = 'compositions/publishing_form.html'
        context = {
            'composition': composition,
            'all_publishers': all_publishers,
            'composition_publishers': composition_publishers,
            'totalpct': totalpct,
            'compositionpublishing': compositionpublishing
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST
        # Check if this POST is for editing a composition publishing company share
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE songwrytrapp_compositionpublishing
                SET publishing_company_id = ?,
                    percentage = ?,
                    pro_work_num = ?,
                    composition_id = ?
                WHERE id = ?
                """,
                (
                    form_data['publishingcompany'], form_data['percentage'],
                    form_data['pro_work_num'], composition_id, compositionpublishing_id
                ))

            return redirect(reverse('songwrytrapp:composition', args=[composition_id]))

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

@login_required
def composition_publishing_remove(request, composition_id, compositionpublishing_id):

    if request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM songwrytrapp_compositionpublishing
                WHERE id = ?
                """, (compositionpublishing_id,))

            return redirect(reverse('songwrytrapp:composition', args=[composition_id]))

@login_required
def composition_writer_remove(request, composition_id, compositionwriter_id):

    if request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM songwrytrapp_compositionwriter
                WHERE id = ?
                """, (compositionwriter_id,))

            return redirect(reverse('songwrytrapp:composition', args=[composition_id]))