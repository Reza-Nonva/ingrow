from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
# Create your views here.
from django.db import connection


@csrf_exempt
def create_customer(request):

    cur = connection.cursor()
    national_id = request.POST['national_id']
    name = request.POST['name']
    phone_number = request.POST['phone_number']
    address = request.POST['address']
    cur.execute("""INSERT INTO public.web_customers
                (national_id, name, phone_number, address)VALUES 
                ('{}', '{}', '{}', '{}');""".format(national_id, name, phone_number, address))
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)


@csrf_exempt
def broadcast(request):

    cur = connection.cursor()
    #First, we send a request to the SMS provider to send an SMS to the customer, and then we specify the status variable.
    national_id = request.POST['national_id']
    text = request.POST['text']
    status = request.POST['status']
    cur.execute("""INSERT INTO public.web_broadcasts
                (national_id_id, text, "timestamp", status)VALUES 
                ('{}', '{}', '{}', {});""".format(national_id, text, datetime.datetime.now(), status))
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
def create_product(request):

    name = request.POST['name']
    order_point = int(request.POST['order_point'])
    price = float(request.POST['price'])
    count = int(request.POST['count'])
    status = True if count > 0 else False

    cur = connection.cursor()
    cur.execute("""INSERT INTO public.web_products
                (name, order_point, price, count, status)VALUES
                ('{}', {}, {}, {}, {});""".format(name, order_point, price, count, status))
    
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
def create_project(request):

    national_id = request.POST['national_id']
    descr = request.POST['descriptions']

    cur = connection.cursor()
    cur.execute("""INSERT INTO public.web_projects
                (national_id_id, description)VALUES 
                ('{}', '{}');""".format(national_id, descr))
    
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)
    

@csrf_exempt
def insert_buy(request):

    code = int(request.POST['code'])
    project = int(request.POST['project'])
    timestamp = datetime.datetime.now()
    count = int(request.POST['count'])
    
    cur = connection.cursor()
    
    cur.execute("""SELECT price, count
                FROM web_products
                WHERE code = {}
                """.format(code))
    temp = cur.fetchone()
    price_per_unit = temp[0]
    avaiable_count = temp[1]
    if (count <= avaiable_count):
        # insert into buy table
        cur.execute("""INSERT INTO public.web_buy
                    ( code_id, project_id_id, "timestamp", count, price_per_unit , total_price) VALUES
                    ( {}, {}, '{}', {}, {}, {});""".format(code, project, timestamp, count, price_per_unit, count * price_per_unit))
        
        #cur.execute(sql = """INSERT INTO public.web_buy
        #            ( code_id, project_id_id, "timestamp", count, price_per_unit , total_price) VALUES
        #            ( {}, {}, '{}', {}, {}, {});""".format(code, project, timestamp, count, price_per_unit, count * price_per_unit)+
        #            """UPDATE public.web_products
        #                SET count = count - {}
        #                WHERE code = {};""".format(count, code))
        # update count of product in product table
        cur.execute("""UPDATE public.web_products
                    SET count = count - {}
                    WHERE code = {};""".format(count, code))
        status = True
    else:
        status = False
    cur.close()
    return JsonResponse({
        'status': status,
    }, encoder=JSONEncoder)



@csrf_exempt
def delete_customer(request):

    national_id = request.POST['national_id']

    cur = connection.cursor()
    cur.execute("""DELETE FROM public.web_customers
                WHERE national_id = '{}';""".format(national_id))
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
def customer_list(request):
    cur = connection.cursor()
    cur.execute("""SELECT * 
                FROM public.web_customers""")
    x = cur.fetchall()
    
    cur.close()
    return JsonResponse({
        'list': x,
    }, encoder=JSONEncoder)

@csrf_exempt
def project_list(request):
    national_id = request.POST['national_id']
    cur = connection.cursor()
    cur.execute("""SELECT * 
                FROM public.web_projects
                WHERE national_id_id = '{}';""".format(national_id))
    x = cur.fetchall()
    cur.close()
    return JsonResponse({
        'list': x,
    }, encoder=JSONEncoder)

