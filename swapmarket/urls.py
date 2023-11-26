from django.urls import path
from . import views
urlpatterns = [
    path('deposit/admin/', views.deposit_admin, name='deposit_admin'),
    path('deposit/admin/<int:deposit_id>/', views.approve_deposit, name='approve_deposit'),
    path('withdraw/admin/', views.withdraw_admin, name='withdraw_admin'),
    path('withdraw/admin/<int:withdraw_id>/', views.approve_withdraw, name='approve_withdraw'),
    path('cart/', views.cart_user, name='cart_user'),
    path('cartc/<int:cart_id>/', views.cancel_cart, name='cancel_cart'),
    path('cart/<int:cart_id>/', views.approve_cart, name='approve_cart'),
    path('', views.home, name='home'),
    path('about', views.about, name="about"),
    path('sell_item/', views.sell_item, name='sell_item'),
    path('sbt/', views.sbt, name='sbt'),
    path('<str:username>/<str:itemname>/', views.item_detail, name='item_detail'),
    path('<str:username>/<str:itemname>/delete/', views.delete_item, name='delete_item'),
    path('deposit/', views.deposit_coins, name='deposit_coins'),
    path('withdraw/', views.withdraw_coins, name='withdraw_coins'),
    path('<str:username>/<str:itemname>/confirm/', views.confirm_item, name='confirm_item'),
]
    