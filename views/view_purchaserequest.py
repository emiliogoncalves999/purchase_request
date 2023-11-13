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

def listapurchaserequest(request):
    # dadospr = RequestOrder.objects.filter(contract__id = request.contract.id).order_by('-id')
    dadospr = RequestOrder.objects.all().order_by('-id')
    context = {
        "dadospr" : dadospr ,
        "pajina_purchase_request" : "active",
            }
    return render(request, 'purchase_request/lista_purchaserequest.html',context)






def requestpurchase(request):
    form = RequestOrderForm()
    if request.method == 'POST':
        form = RequestOrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.contract = request.contract
            instance.created_by = User.objects.get(id=request.user.id) 
            instance.save()
            messages.success(request, 'Request created successfully.')  # Success message
            return redirect('purchase_request:listapurchaserequest')
        else:
            error_messages = []  # Initialize an empty list to store custom error messages
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            print(str(error_messages))
            messages.error(request, 'There was an error. Please correct the form.')  # Error message
            return redirect('purchase_request:requestpurchase')

    context = {
        "form" : form,
        "pajina_purchase_request" : "active",
            }
    return render(request, 'purchase_request/request_purchaserequest.html',context)



def editrequestpurchase(request, id):

    id = decrypt_id(id)
    requestorder = RequestOrder.objects.get(id=id)
    form = RequestOrderForm(instance=requestorder)

    if request.method == 'POST':
        form = RequestOrderForm(request.POST, instance=requestorder)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Request created successfully.')  # Success message
            return redirect('purchase_request:listapurchaserequest')
        else:
            # error_messages = []  # Initialize an empty list to store custom error messages
            # for field, errors in form.errors.items():
            #     for error in errors:
            #         error_messages.append(f"{field}: {error}")
            # print(str(error_messages))
            messages.error(request, 'There was an error. Please correct the form.')  # Error message
            return redirect('purchase_request:requestpurchase')

    context = {
        "form" : form,
        "pajina_purchase_request" : "active",
            }
    return render(request, 'purchase_request/request_purchaserequest.html',context)




def detallupurchaserequest(request,id):
    id = decrypt_id(id)
    purchaserequest = RequestOrder.objects.get(id=id)
    itempurchaserequest = ItemRequest.objects.filter(request_order=id)

    timeline = RequestOrderAprove.objects.filter(request_order=id)
    print(timeline)

    context = {

        "purchaserequest" : purchaserequest,
        "itempurchaserequest" : itempurchaserequest,
        "pajina_purchase_request" : "active",
        "timeline" : timeline,
            }
    return render(request, 'purchase_request/detallu_purchaserequest.html',context)



def sendpurchaserequest(request, id):
    id = decrypt_id(id)

    try:
        request_order_aprove = RequestOrderAprove.objects.filter(request_order__id=id)
        request_order_aprove.delete()
    except ObjectDoesNotExist:
        print("RequestOrderAprove instance not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


    unique_group_names = RequestSet.objects.filter(category__name='purchase_request',level__name='jeral')

    for group_name in unique_group_names.iterator():
        contract = Contract.objects.get(employeeuser__user__groups__name=group_name.group.name, employeeuser__user__is_active=True)

    
        addtimeline = RequestOrderAprove()
        addtimeline.request_order = RequestOrder.objects.get(id=id)
        addtimeline.contract = contract
        addtimeline.status = "Review"
        addtimeline.created_by = request.user


        try:
            addtimeline.save()

        except Exception as e:
            print(e)
            messages.success(request, 'Falhansu teknika favor manda fali')  
            return redirect('purchase_request:listapurchaserequest')


    requestorder = RequestOrder.objects.get(id=id)
    requestorder.is_draft = False
    requestorder.save()
    messages.success(request, 'Pedidu Prossesa ona')  


    return redirect('purchase_request:listapurchaserequest')




