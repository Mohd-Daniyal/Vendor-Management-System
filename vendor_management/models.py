import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

    
class Vendor(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    quality_rating_avg = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_response_time = models.FloatField(default=0, validators=[MinValueValidator(0)])
    fulfillment_rate = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    vendor_code = models.CharField(max_length=10, primary_key=True)
        
    def save(self, *args, **kwargs):
        if not self.vendor_code:
            year_last_two_digits = datetime.datetime.now().strftime("%y")
            last_vendor = Vendor.objects.order_by('-vendor_code').first()
            last_vendor_code = int(last_vendor.vendor_code.split("VM")[-1]) if last_vendor else 0
            new_vendor_code = f"{year_last_two_digits}VM{str(last_vendor_code + 1).zfill(3)}"
            self.vendor_code = new_vendor_code
        super().save(*args, **kwargs)
    
    
class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    expected_delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)]) 
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    po_number = models.CharField(max_length=50, primary_key=True)
        
    def save(self, *args, **kwargs):
        if not self.po_number:
            year_last_two_digits = datetime.datetime.now().strftime("%y")
            last_po = PurchaseOrder.objects.order_by('-po_number').first()
            last_po_number = int(last_po.po_number.split("OD")[-1]) if last_po else 0
            new_po_number = f"{year_last_two_digits}OD{str(last_po_number + 1).zfill(4)}"
            self.po_number = new_po_number
        super().save(*args, **kwargs)
    
    def clean(self):
        if (self.actual_delivery_date < self.order_date) or (self.expected_delivery_date < self.order_date):
            raise ValidationError({'delivery_date': 'Delivery date cannot be before order date.'})
        
        
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    quality_rating_avg = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_response_time = models.FloatField(default=0, validators=[MinValueValidator(0)])
    fulfillment_rate = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
