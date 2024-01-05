from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
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
                (national_id, name, phone_number, address)
                VALUES ('{}', '{}', '{}', '{}');""".format(national_id, name, phone_number, address))
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
                (national_id_id, text, "timestamp", status)
                VALUES ('{}', '{}', '{}', {});""".format(national_id, text, datetime.datetime.now(), status))
    cur.close()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

