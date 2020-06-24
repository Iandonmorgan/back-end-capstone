import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from songwrytrapp.models import PublishingCompany, PRO, model_factory
from ..connection import Connection
from .details import get_publishingcompany


def get_publishingcompanies():
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
            pc.admin,
            p.name as 'PRO_Name',
            p.city as 'PRO_City',
            p.state as 'PRO_State',
            p.zipcode as 'PRO_Zipcode'
        FROM songwrytrapp_publishingcompany pc
        JOIN songwrytrapp_pro p
        ON pc.pro_id = p.id
        """)

        return db_cursor.fetchall()

def get_pros():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(PRO)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.name,
            p.address,
            p.city,
            p.state,
            p.zipcode,
            p.website
        FROM songwrytrapp_pro p
        """)

        return db_cursor.fetchall()

@login_required
def publishingcompany_form(request):
    if request.method == 'GET':
        publishingcompanies = get_publishingcompanies()
        pros = get_pros()
        template = 'publishingcompanies/form.html'
        context = {
            'all_publishingcompanies': publishingcompanies,
            'all_pros': pros
        }

        return render(request, template, context)

@login_required
def publishingcompany_edit_form(request, publishingcompany_id):

    if request.method == 'GET':
        publishingcompany = get_publishingcompany(publishingcompany_id)
        publishingcompanies = get_publishingcompanies()
        pros = get_pros()
        template = 'publishingcompanies/form.html'
        context = {
            'publishingcompany': publishingcompany,
            'all_publishingcompanies': publishingcompanies,
            'all_pros': pros
        }

        return render(request, template, context)