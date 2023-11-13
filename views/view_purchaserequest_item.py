from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
# from population.models import Population,DetailFamily,Family,Religion,Profession,Citizen,Aldeia,Village,User,Migration,Death,Migrationout,Temporary,ChangeFamily
# from population.utils import getnewidp,getnewidf
# from population.forms import Family_form,Family_form,FamilyPosition,Population_form,DetailFamily_form,CustumDetailFamily_form,Death_form,Migration_form,Migrationout_form,Changefamily_form
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

# from custom.utils import getnewid, getjustnewid, hash_md5, getlastid
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import date
from django.http import JsonResponse

from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from rekrutamentu.forms import FileUploadForm
from purchase_request.models import *
from custom.models import RequestSet

from settingapps.utils import  decrypt_id, encrypt_id
from django.core.paginator import Paginator

from django.utils import translation
from django.utils import timezone
from datetime import datetime

from django.contrib.auth.models import User, Group

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from purchase_request.forms import RequestOrderForm, ItemRequestForm
from employee.models import EmployeeUser
import logging
from django.core.exceptions import ObjectDoesNotExist





def additempurchase(request,id_riquest):
    encript_id_riquest = id_riquest
    id_riquest = decrypt_id(id_riquest)
    requestorder = RequestOrder.objects.get(id=id_riquest)

    form = ItemRequestForm()

    if request.method == 'POST':
        form = ItemRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.request_order = requestorder
            instance.status = "Pendente"
            instance.save()
            messages.success(request, 'Request created successfully.')  # Success message
            return redirect('purchase_request:detallupurchaserequest', id = encript_id_riquest )
        else:
            messages.error(request, 'There was an error. Please correct the form.')  # Error message
            return redirect('purchase_request:purchaserequest', id_riquest = encript_id_riquest)

    context = {
        "form" : form,
        "pajina_purchase_request" : "active",
            }
    return render(request, 'purchase_request/request_purchaserequest.html',context)



def edititempurchase(request,id_item):


    dec_id_item = decrypt_id(id_item)
    itemedit = ItemRequest.objects.get(id=dec_id_item)

    id_request = encrypt_id(str(itemedit.request_order.id))

    form = ItemRequestForm(instance = itemedit)

    if request.method == 'POST':
        form = ItemRequestForm(request.POST, instance = itemedit)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Request created successfully.')  # Success message
            return redirect('purchase_request:detallupurchaserequest', id = id_request )
        else:
            messages.error(request, 'There was an error. Please correct the form.')  # Error message
            return redirect('purchase_request:edititempurchase', id_item = id_item)

    context = {
        "form" : form,
        "pajina_purchase_request" : "active",
            }
    return render(request, 'purchase_request/request_purchaserequest.html',context)


def apagaitempurchase(request, id_item):
    id_item = decrypt_id(id_item)
    itemapaga = ItemRequest.objects.get(id=id_item)
    id_request = encrypt_id(str(itemapaga.request_order.id))
    item = itemapaga
    item.delete(user=request.user)
    return redirect('purchase_request:detallupurchaserequest', id = id_request )


def aproveditempurchase(request, id_item):
    id_item = decrypt_id(id_item)
    itemprosses = ItemRequest.objects.get(id=id_item)
    id_request = encrypt_id(str(itemprosses.request_order.id))
    item = itemprosses
    item.status = "Aproved"
    item.save()
    return redirect('purchase_request:detallupurchaserequest', id = id_request )

def rijectitempurchase(request, id_item):
    id_item = decrypt_id(id_item)
    itemprosses = ItemRequest.objects.get(id=id_item)
    id_request = encrypt_id(str(itemprosses.request_order.id))
    item = itemprosses
    item.status = "Rejected"
    item.save()
    return redirect('purchase_request:detallupurchaserequest', id = id_request )


def deliveritempurchase(request, id_item):
    id_item = decrypt_id(id_item)
    itemprosses = ItemRequest.objects.get(id=id_item)
    id_request = encrypt_id(str(itemprosses.request_order.id))
    item = itemprosses
    item.is_delivery = True
    item.save()
    return redirect('purchase_request:detallupurchaserequest', id = id_request )
