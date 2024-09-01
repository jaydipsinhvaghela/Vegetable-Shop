from . import views 
from django.urls import path

urlpatterns = [
     path('/home',views.home,name="home"),
     path('/s_login',views.s_login,name="s_login"),
     path('/s_register',views.s_register,name="s_register"),
     path('/add_product',views.add_product,name="add_product"),
     path('/view_product',views.view_product,name="view_product"),
     path('/edit_product/<int:id>',views.edit_product,name="edit_product"),
     path('/view_orders',views.view_orders,name="view_orders"),
     path('/view_feedback',views.view_feedback,name="view_feedback"),
     path('/update_product/<int:id>',views.update_product,name="update_product"),
     path('/seller_profile',views.seller_profile,name="seller_profile"),
     path('/delete_product/<int:id>',views.delete_product,name="delete_product"),
     path('/confirm_order/<int:id>',views.confirm_order,name="confirm_order"),
     path('/completed_order/<int:id>',views.completed_order,name="completed_order"),
     path('/',views.dashboard,name="dashboard"),
     path('/s_logout',views.s_logout,name='s_logout'),
     
]