import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import PublishingCompany, model_factory
from ..connection import Connection


def get_publishingcompany(publishingcompany_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(PublishingCompany)
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
        WHERE pc.id = ?
        """, (publishingcompany_id,))

        return db_cursor.fetchone()

def get_composition_publishers(publishingcompany_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(PublishingCompany)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pc.user_id,
            pc.name,
            pc.pro_id,
            pc.pro_acct_num,
            pc.admin,
            cpc.percentage,
            cpc.pro_work_num,
            cpc.id as compositionpublishing_id
        FROM songwrytrapp_publishingcompany pc
        JOIN songwrytrapp_pro p
        ON pc.pro_id = p.id
        JOIN songwrytrapp_compositionpublishing cpc
        ON cpc.publishing_company_id = pc.id
        JOIN songwrytrapp_composition c
        ON c.id = cpc.composition_id
        WHERE pc.id = ?
        ORDER BY pc.name
        """, (publishingcompany_id,))

        return db_cursor.fetchall()

@login_required
def publishingcompany_details(request, publishingcompany_id):
    if request.method == 'GET':
        publishingcompany = get_publishingcompany(publishingcompany_id)

        template = 'publishingcompanies/detail.html'
        context = {
            'publishingcompany': publishingcompany
        }

        return render(request, template, context)
    if request.method == 'POST':
        form_data = request.POST
        composition_publishingcompanies = get_composition_publishers(publishingcompany_id)
        # Check if this POST is for deleting a Publishing Company
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                for cpc in composition_publishingcompanies:
                    db_cursor.execute("""
                    DELETE FROM songwrytrapp_compositionpublishing
                    WHERE id = ?
                    """, (cpc.compositionpublishing_id,))
                db_cursor.execute("""
                DELETE FROM songwrytrapp_publishingcompany
                WHERE id = ?
                """, (publishingcompany_id,))

            return redirect(reverse('songwrytrapp:publishingcompanies'))
        # Check if this POST is for editing a Publishing Company
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE songwrytrapp_publishingcompany
                SET name = ?,
                    pro_id = ?,
                    pro_acct_num = ?,
                    admin = ?
                WHERE id = ?;
                """,
                (
                    form_data['name'], form_data['pro'], form_data['pro_acct_num'],
                    form_data['admin'], 
                    publishingcompany_id,
                ))

            return redirect(reverse('songwrytrapp:publishingcompany', args=[publishingcompany_id]))