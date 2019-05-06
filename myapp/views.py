from django.contrib.auth.decorators import login_required
from django.db import connections
from django.shortcuts import render

@login_required
def index(request):
    context = {}

    with connections['legacydb'].cursor() as cursor:
        imaginary_user_constraint = 'Osaka'
        sql = [
            'SELECT shops.name AS shop_name, items.name AS item_name, sales.quantity',
            'FROM shops, items, sales',
            'WHERE shops.id = sales.shopid',
            'AND items.id = sales.itemid',
            'AND NOT shops.name = %s', # Placeholder
        ]
        cursor.execute(' '.join(sql), [imaginary_user_constraint]);
        sales = namedtuplefetchall(cursor)
        context.update({'sales': sales})

    return render(request, 'myapp/index.html', context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def namedtuplefetchall(cursor):
    from collections import namedtuple
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
