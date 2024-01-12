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

@csrf_exempt
def create_payment(request):
    payment_id = request.POST['payment_id']
    project_id = request.POST['project_id']
    amount = request.POST['amount']
    timestamp = datetime.datetime.now()
    
    cur = connection.cursor()
    cur.execute("""INSERT INTO public.web_payments
                (payment_id, project_id_id, amount, "timestamp") VALUES
                ({}, {}, {}, '{}');""".format(payment_id, project_id, amount, timestamp))    
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
def get_project_costs(request):
    project_id = request.POST['project_id']
    cur = connection.cursor()
    cur.execute("""SELECT sum(total_price)
                FROM public.web_buy
                WHERE project_id_id = {};""".format(project_id))   
    temp = cur.fetchone()
    total_products_costs = temp[0]
    if(total_products_costs is None):
        total_products_costs = 0
    total_products_costs = int(total_products_costs)
    
    cur.execute("""SELECT sum(total_price)
                FROM public.web_work_report
                WHERE work_id_id IN(SELECT work_id
                                    FROM public.web_works w, public.web_projects p
                                    WHERE p.project_id = w.project_id_id)
                """)
    temp = cur.fetchone()
    total_works_costs = temp[0]
    if(total_works_costs is None):
        total_works_costs = 0
    total_works_costs = int(total_works_costs)            
    cur.execute("""SELECT sum(amount)
                FROM public.web_payments
                WHERE project_id_id = {};""".format(project_id))
    temp = cur.fetchone()
    total_payments = temp[0]
    if(total_payments is None):
        total_payments = 0
    total_payments = int(total_payments)
    
    remaining = total_products_costs + total_works_costs - total_payments
    remaining = str(remaining)  
    cur.close()
    return JsonResponse({
        'status': 'ok',
        'total works costs': str(total_works_costs),
        'total product costs': str(total_products_costs),
        'total payments': str(total_payments),
        'remaining': remaining,
    }, encoder=JSONEncoder)

@csrf_exempt
def delete_payment(request):
    payment_id = request.POST['payment_id']
    cur = connection.cursor()
    cur.execute("""DELETE FROM public.web_payments
                WHERE payment_id = {}""".format(payment_id))    
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)


@csrf_exempt
def delete_project(request):
    project_id = request.POST['project_id']
    cur = connection.cursor()
    cur.execute("""DELETE FROM public.web_projects
                WHERE project_id = {}""".format(project_id))    
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
def delete_buy(request):
    id = request.POST['id']
    cur = connection.cursor()
    cur.execute("""SELECT count, code_id
                FROM public.web_buy
                WHERE id = {}""".format(id))
    temp = cur.fetchone()
    back_count = int(temp[0])
    back_code = int(temp[1])

    cur.execute("""UPDATE public.web_products
                    SET count = count + {}
                    WHERE code = {};""".format(back_count, back_code))
    
    cur.execute("""DELETE FROM public.web_buy
                WHERE id = {}""".format(id))    
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
def create_service(request):
    name = request.POST['name']
    price_per_unit = float(request.POST['price_per_unit'])

    cur = connection.cursor()
    cur.execute("""INSERT INTO public.web_services
                (name, price_per_unit)VALUES
                ('{}', {});""".format(name, price_per_unit))
    
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
def delete_service(request):
    code = request.POST['code']
    cur = connection.cursor()
    cur.execute("""DELETE FROM public.web_services
                WHERE code = {};""".format(code))
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
def services_list(request):
    cur = connection.cursor()
    cur.execute("""SELECT *
                FROM public.web_services""")
    temp = cur.fetchall()
    cur.close()
    return JsonResponse({
        'status': temp,
    }, encoder=JSONEncoder)

@csrf_exempt
def products_list(request):
    cur = connection.cursor()
    cur.execute("""SELECT *
                FROM public.web_products""")
    temp = cur.fetchall()
    cur.close()
    return JsonResponse({
        'status': temp,
    }, encoder=JSONEncoder)

@csrf_exempt
def create_work(request):
    # in this func, we just make a work template for a project
    # report of work is stored in works_report table
    project_id = request.POST['project_id']
    timestamp = datetime.datetime.now()
    cur = connection.cursor()
    cur.execute("""INSERT INTO public.web_works
                (project_id_id, "timestamp") VALUES
                ({}, '{}');""".format(project_id, timestamp))
    cur.close()
    return JsonResponse({
        'status': "ok",
    }, encoder=JSONEncoder)

@csrf_exempt
def delete_work(request):
    work_id = request.POST['work_id']
    cur = connection.cursor()
    cur.execute("""DELETE FROM public.web_works
                WHERE work_id = {};""".format(work_id))
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
def work_list(request):
    # return the list of works of a project
    project_id = request.POST['project_id']
    cur = connection.cursor()
    cur.execute("""SELECT *
                FROM public.web_works
                WHERE project_id_id = {};""".format(project_id))
    temp = cur.fetchall()
    cur.close()
    return JsonResponse({
        'status': json.dumps(temp, default=str),
    }, encoder=JSONEncoder)

@csrf_exempt
def create_work_report(request):
    work_id = request.POST['work_id']
    service_code = request.POST['service_code']
    unit = int(request.POST['unit'])
    
    cur = connection.cursor()
    cur.execute("""SELECT price_per_unit
                FROM public.web_services
                WHERE code = {};""".format(service_code))
    price = cur.fetchone()
    price =int(price[0])
    total_price = unit * price

    cur.execute("""INSERT INTO public.web_work_report
                (work_id_id, service_code_id, unit, price_per_unit, total_price) VALUES
                ({}, {}, {}, {}, {});""".format(work_id, service_code, unit, price, total_price))
    cur.close()
    return JsonResponse({
        'status': "ok",
    }, encoder=JSONEncoder)

@csrf_exempt
def delete_work_report(request):
    id = request.POST['id']
    cur = connection.cursor()
    cur.execute("""DELETE FROM public.web_work_report
                WHERE id = {};""".format(id))
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
def work_report_list(request):
    # return the list of works_report of a work
    work_id = request.POST['work_id']
    cur = connection.cursor()
    cur.execute("""SELECT *
                FROM public.web_work_report
                WHERE work_id_id = {};""".format(work_id))
    temp = cur.fetchall()
    cur.close()
    return JsonResponse({
        'status': json.dumps(temp, default=str),
    }, encoder=JSONEncoder)