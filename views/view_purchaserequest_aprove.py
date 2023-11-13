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
from purchase_request.forms import RequestOrderAproveForm
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



def aceptedpurchaserequest(request, id):
    form = RequestOrderAproveForm()


    iddecript = decrypt_id(id)
    dados = RequestOrderAprove.objects.get(id=iddecript)
    idrequest = RequestOrder.objects.get(id = dados.request_order.id)
    idrequest2 =  encrypt_id(str(idrequest.id))

    if request.method == 'POST':
        form = RequestOrderAproveForm(request.POST, instance = dados )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.status = "Acepted"
            instance.save()
            messages.success(request, 'Rejeita ho susesu')  # Success message
            return redirect('purchase_request:detallupurchaserequest', id = idrequest2)
        else:
            messages.success(request, 'Rejeita ho susesu')  # Success message
            return redirect('purchase_request:detallupurchaserequest', id = idrequest2)


    context = {
        "form" : form,
        "asaun" : "aceita",
        "dados" : dados ,
        "pajina_purchase_request" : "active",
            }
    return render(request, 'purchase_request/purchase_request__actiondescription.html',context)


def rijectedpurchaserequest(request, id):



    form = RequestOrderAproveForm()
    iddecript = decrypt_id(id)
    dados = RequestOrderAprove.objects.get(id=iddecript)
    idrequest = RequestOrder.objects.get(id = dados.request_order.id)
    idrequest2 =  encrypt_id(str(idrequest.id))



    if request.method == 'POST':
        form = RequestOrderAproveForm(request.POST, instance = dados )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.status = "Rejected"
            instance.save()
            messages.success(request, 'Rejeita ho susesu')  # Success message
            return redirect('purchase_request:detallupurchaserequest', id = idrequest2)
        else:
            messages.success(request, 'Rejeita ho susesu')  # Success message
            return redirect('purchase_request:detallupurchaserequest', id = idrequest2)


    context = {
        "form" : form,
        "asaun" : "rejeita",
        "dados" : dados ,
        "pajina_purchase_request" : "active",
            }
    
    
    return render(request, 'purchase_request/purchase_request__actiondescription.html',context)




