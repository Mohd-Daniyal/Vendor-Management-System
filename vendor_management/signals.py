from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from django.db.models import Avg, F

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    vendor = instance.vendor

    # On-Time Delivery Rate
    if instance.status == 'completed':
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_delivery_orders = completed_orders.filter(actual_delivery_date__lte=F('expected_delivery_date'))
        on_time_delivery_count = on_time_delivery_orders.count()
        total_completed_orders_count = completed_orders.count()

        if total_completed_orders_count > 0:
            on_time_delivery_rate = (on_time_delivery_count / total_completed_orders_count) * 100
        else:
            on_time_delivery_rate = 0

        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

    # Quality Rating Average
    if instance.status == 'completed' and instance.quality_rating is not None:
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        quality_rating_avg = completed_orders.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()

    # Average Response Time
    if instance.acknowledgment_date is not None:
        acknowledged_purchases = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        total_acknowledged_purchases = acknowledged_purchases.count()
        total_response_time = sum(
            (purchase.acknowledgment_date - purchase.issue_date).total_seconds() for purchase in acknowledged_purchases)
        if total_acknowledged_purchases > 0:
            vendor.average_response_time = ((total_response_time/3600) / total_acknowledged_purchases)
        else:
            vendor.average_response_time = 0
        vendor.save()
        
    # Fulfillment Rate
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', issue_date__isnull=True)
    if total_orders > 0:
        fulfillment_rate = (fulfilled_orders.count() / total_orders) * 100
    else:
        fulfillment_rate = 0

    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

