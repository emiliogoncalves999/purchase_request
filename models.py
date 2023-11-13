from django.db import models
from django.contrib.auth.models import User, Group
from employee.models import Employee,EmployeeUser
from custom.models import Unit, Level, Donor
from contract.models import Contract
from django.utils import timezone
# Create your models here.
from ckeditor.fields import RichTextField

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class RequestOrder(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name="RequestOrdercontract")
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, null=True, blank=False, related_name="RequestOrderdonor")
    is_urgent = models.BooleanField(default=False, verbose_name = "Is Urgent?")
    routine = models.CharField(max_length=100, null=True, blank=True)
    em_parts = models.CharField(max_length=100, null=True, blank=True)
    request_date = models.DateField(null=True, blank=True)
    budget_limite = models.CharField(max_length=100, null=True, blank=True)
    activity = models.CharField(max_length=100, null=True, blank=True)
    project = models.CharField(max_length=100, null=True, blank=True)
    is_draft = models.BooleanField(default=True)
   

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="RequestOrdercreatedby")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="RequestOrderupdatedby")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="RequestOrderdeletedby")
    deleted_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        template = '{0.activity}'
        return template.format(self)
    
    def delete(self, user):
        self.deleted_at = str(timezone.now())
        self.deleted_by = user
        self.save()

    default_objects = models.Manager()  # The default manager
    objects = ActiveManager()

    class Meta:
        verbose_name_plural='1-Data_Purchase-Request_Purchase-Order'


class ItemRequest(models.Model):
    request_order = models.ForeignKey(RequestOrder, on_delete=models.CASCADE, null=True, blank=False, related_name="ItemRequestrequestorder")
    quantity = models.IntegerField(null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=False, related_name="ItemRequestrequestunit")
    is_delivery = models.BooleanField(default=False, blank=True, null=True)
    status = models.CharField(choices=[('Aproved','Aproved'),('Rejected','Rejected'),('Pendende','Pendende')],max_length=30, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True, related_name="ItemRequestlevel")
    item_description = models.CharField(max_length=200,null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="ItemRequestcreatedby")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="ItemRequestupdatedby")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="ItemRequestdeletedby")
    deleted_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        template = '{0.description}'
        return template.format(self)
    
    def delete(self, user):
        self.deleted_at = str(timezone.now())
        self.deleted_by = user
        self.save()

    default_objects = models.Manager()  # The default manager
    objects = ActiveManager()

    class Meta:
        verbose_name_plural='1-Data_Purchase-Request_Item-Request'


class RequestOrderAprove(models.Model):
    request_order = models.ForeignKey(RequestOrder, on_delete=models.CASCADE, null=True, blank=False, related_name="RequestOrderAproverequestorder")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=False, related_name="RequestOrderAproveuser")
    status = models.CharField(choices=[('Review','Review'),('Acepted','Acepted'),('Rejected','Rejected')],max_length=30, null=True, blank=True)
    description = RichTextField(null=False, blank=False)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="RequestOrderAprovecreatedby")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="RequestOrderAproveupdatedby")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="RequestOrderAprovedeletedby")
    deleted_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        template = '{0.description}'
        return template.format(self)
    
    def delete(self, user):
        self.deleted_at = str(timezone.now())
        self.deleted_by = user
        self.save()

    default_objects = models.Manager()  # The default manager
    objects = ActiveManager()

    class Meta:
        verbose_name_plural='1-Data-Purchase_Request-Request_Order_Aprove'