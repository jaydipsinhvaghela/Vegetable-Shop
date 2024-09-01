from django.urls import path
from . import views

urlpatterns = [
     path('/',views.home,name='home'),
     path('/template',views.template,name="template"),
     path('/login',views.login,name='login'),
     path('/register',views.register,name='register'),
     path('/category',views.category,name='category'),
     path('/products/<int:id>',views.products,name='products'),
     path('/single-product/<int:id>',views.single_product,name='single_product'),
     path('/cart/',views.cart,name='cart'),
     path('/wishlist/<int:id>',views.wishlist,name='wishlist'),
     path('/Viewwishlist/<int:id>',views.wishlist,name='wishlist'),
     path('/checkout',views.checkout,name='checkout'),
     path('/user_profile',views.user_profile,name='user_profile'),
     path('/cart/removeFromCartList/<int:productid>',views.removeFromCartList,name='removeFromCartList'),
     path('/wishlist/remove_from_wishlist/<int:productid>',views.remove_from_wishlist,name='remove_from_wishlist'),
     path('/add_to_cart/<int:product_id>',views.addToCart,name='add_to_cart'),
     path('/order-history',views.orderHistory,name='order_history'),
     path('/forgot_password',views.forgot_password,name='forgot_password'),
     path('/contact_us',views.contact_us,name='contact_us'),
     path('/feedback',views.feedback,name='feedback'),
     path('/aboutus',views.aboutus,name='aboutus'),
     path('/user_profile/<int:id>',views.user_profile,name="user_profile"),
     path('/update_user/<int:id>',views.update_user,name='update_user'),
     path('/user_dashboard',views.user_dashboard,name='user_dashboard'),
     path('/logout',views.logout,name='logout'),
     
     
] 
