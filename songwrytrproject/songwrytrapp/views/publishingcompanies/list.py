import sqlite3
from django.shortcuts import render, redirect, reverse
from songwrytrapp.models import PublishingCompany, PRO
from ..connection import Connection
from songwrytrapp.models import model_factory
from django.contrib.auth.decorators import login_required

@login_required
def publishingcompany_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(PublishingCompany)
            
            db_cursor = conn.cursor()
            db_cursor.execute("""
            SELECT
                pc.*,
                p.name as 'PRO_Name',
                p.city as 'PRO_City',
                p.state as 'PRO_State',
                p.zipcode as 'PRO_Zipcode'
            FROM songwrytrapp_publishingcompany pc
            JOIN songwrytrapp_pro p
            ON pc.pro_id = p.id
            ORDER BY pc.name
            """)

            all_publishingcompanies = db_cursor.fetchall()

        template = 'publishingcompanies/list.html'
        context = {
            'all_publishingcompanies': all_publishingcompanies
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO songwrytrapp_publishingcompany
            (
                name, pro_id, pro_acct_num, admin, user_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (form_data['name'], form_data['pro'], form_data['pro_acct_num'],
                form_data['admin'],
                request.user.id))

        return redirect(reverse('songwrytrapp:publishingcompanies'))