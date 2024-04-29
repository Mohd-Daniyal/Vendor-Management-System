from django.urls import path
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/vendors/', views.VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/<str:vendor_id>/', views.VendorRetrieveUpdateDestroyView.as_view(), name='vendor-retrieve'),
    path('api/purchase_orders/', views.PurchaseOrderListCreateView.as_view(), name='purchase-order-list'),
    path('api/purchase_orders/<str:po_number>/', views.PurchaseOrderRetrieveUpdateDestroyView.as_view(), name='po-retrieve'),
    path('api/purchase_orders/<str:po_id>/acknowledge/', views.PurchaseOrderAcknowledgeView.as_view(), name='purchase-order-acknowledge'),
    path('api/vendors/<str:vendor_id>/performance/', views.VendorPerformanceView.as_view(), name='vendor-performance'),
]
