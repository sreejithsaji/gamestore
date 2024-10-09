"""
URL configuration for GameStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpview.as_view(),name='signup'),
    path('',views.SignInView.as_view(),name='signin'),
    path('logout',views.SignOutView.as_view(),name='signout'),
    path('index/',views.IndexView.as_view(),name='index'),
    path('profile/<int:pk>/change/',views.ProfileUpdateView.as_view(),name='edit'),
    path('project/detail/<int:pk>/',views.ProjectDetailView.as_view(),name='project-detail'),
    path('project/cart/add/<int:pk>/',views.AddToCartView.as_view(),name="add-cart"),
    path('project/cart/',views.MyCartView.as_view(),name='cart'),
    path('project/cart/delete/<int:pk>/',views.CartDeleteView.as_view(),name="cart-delete"),
    path('payment/',views.CheckOutView.as_view(),name='razor'),
    path("payment/verification/",views.PaymentVerificationView.as_view(),name="payment-verfiy"),
    path('order/summary',views.PurchaseView.as_view(),name='order-summary'),
    path('search/',views.SearchView.as_view(),name="search")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
