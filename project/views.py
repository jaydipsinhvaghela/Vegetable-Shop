from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from . import models
import re
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
# Create your views here.

# <---------================= Function =================-------------->
def is_valid_email(email):
    # Define the regular expression pattern for a basic email address
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Use re.match to check if the email matches the pattern
    match = re.match(pattern, email)
    
    # If match is not None, the email is valid; otherwise, it's not
    return match is not None

# <---------================= Views =================-------------->
def user_dashboard(request):
    if 'userid' not in request.session:
        return redirect("/project/login")

    userid = request.session['userid']

    # Fetch total order count for the user
    total_orders = models.orders.objects.filter(userid=userid).count()

    # Fetch pending order count for the user
    pending_orders = models.orders.objects.filter(userid=userid, status='pending').count()

    # Fetch total wishlist count for the user
    total_wishlist = models.wishlist.objects.filter(userid=userid).count()

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_wishlist': total_wishlist
    }
    
    return render(request, 'user_profile.html', context)

def home(request):
     category  = models.category.objects.all().values()
     print(category)
     response = []
     for i in category:
          response.append(i)
     
     products = models.product.objects.all().values()
     print(products)
     response_product = []
     for i in products:
          response_product.append(i)
     print(response_product)
     return render(request,'home.html',{'response':response,'response_product':response_product})

def template(request):
     return render(request,'template.html')

def login(request):
     if request.method == "POST":
          email = request.POST["email"]
          password = request.POST["password"]
          if is_valid_email(email):
               if len(password) >= 8:
                    print(f"email is {email} and password is {password} ")
                    data = models.user.objects.filter(email=email,password=password).values()
                    print(data)
                    if len(data) == 0:
                         print("\n\n data is empty \n\n")
                    else:
                         print("\n\n data is not empty \n\n")
                         request.session['userid'] = data[0]['id'] 
                         print(request.session['userid'])
                         return render(request,"home.html",{'message':0})
               else:
                    message = "Password Must be atleast 8 characters "
                    return render(request,'login.html',{'message':message, 'response' : 0})
          else:
               message = "Please Enter a valid email address "
               return render(request,'login.html',{'message':message , 'response':1})
          
     return render(request,'login.html')

def register(request):
     if request.method == "POST":
          print(request.POST)
          try: 
               username  = request.POST['username']
               contact  = request.POST['contact']
               email = request.POST['email']
               password = request.POST['password']
               city = request.POST['city']
               pincode = request.POST['pincode']
               address = request.POST['address']
               data = models.user.objects
               form = data.create(name=username,contact=contact,email=email,password=password,city=city,pincode=pincode,address=address)
               form.save()
               print(f"username is {username} contact is {contact} email is {email} password is {password} city is {city} pincode is {pincode} address is {address}")    
               # request.session['message'] = 'Register Successfully ' 
               return render(request,"login.html",{'message':'Register Successfull','response':2})
          except:
               return render(request,"register.html",{ "message" : "Invalid Register Attempt " })

     return render(request,"register.html")

def category(request):
     data  = models.category.objects.all().values()
     print(data)
     response = []
     for i in data:
          response.append(i)
     return render(request,"category.html",{'response':response})

def products(request,id):
     cat_id = id
     data = models.product.objects.filter(categoryid=cat_id).values()
     print(data)
     response= []
     for i in data :
          response.append(i)
     return render(request,"products.html",{'response':response})

def single_product(request,id):
     product_id = id 
     data = models.product.objects.filter(id=product_id).values()
     print(data)
     response = []
     for i in data:
          response.append(i)
     return render(request,"single_product.html",{'response':response})
# views.py



def cart(request):
    userid = request.session.get('userid')
    products = []
    if userid:
        cart_items = models.cart.objects.filter(userid=userid)
        product_ids = [item.productid for item in cart_items]
        for product_id in product_ids:
            product_data = models.product.objects.filter(id=product_id).first()  # Use first() to retrieve a single product instance
            if product_data:
                seller_id = product_data.categoryid  # Assuming the Product model has a 'seller_id' field
                seller_name = models.seller.objects.get(id=seller_id).name  # Assuming the Seller model has a 'name' field
                
                product_data.name = seller_name  # Add the seller's name to the product_data instance
                products.append(product_data)
    return render(request, "cart.html", {'products':products})


def wishlist(request,id):
     product_id  = id 
     userid = request.session['userid']
     data = models.wishlist.objects.filter(userid=userid,productid=product_id).values()
     result = models.wishlist.objects.filter(userid=userid).values()
     product_ids = []
     for i in result:
          product_ids.append(i['productid'])
     product_list = []
     dummy_product = []
     wishlist = []
     for single_product_id in product_ids:
          product_list.append(models.product.objects.filter(id=single_product_id).values())
     print("product list ")
     result_list = [list(queryset.values()) for queryset in product_list]
     for i  in result_list:
          wishlist.append(i)
     if(id==0):
          return render(request,"wishlist.html",{'result':wishlist})
     else:
          if len(data) > 0:
               print("if")
               return render(request,"wishlist.html",{'result':wishlist})
          else:
               print("else")
               data = models.wishlist.objects
               form = data.create(userid=userid,productid=product_id)
               form.save()
     return render(request,"wishlist.html",{'result':wishlist})

def Viewwishlist(request,id):
     product_id  = id 
     userid = request.session['userid']
     data = models.wishlist.objects.filter(userid=userid,productid=product_id).values()
     result = models.wishlist.objects.filter(userid=userid).values()
     product_ids = []
     for i in result:
          product_ids.append(i['productid'])
     product_list = []
     dummy_product = []
     wishlist = []
     for single_product_id in product_ids:
          product_list.append(models.product.objects.filter(id=single_product_id).values())
     print("product list ")
     result_list = [list(queryset.values()) for queryset in product_list]
     for i  in result_list:
          wishlist.append(i)
     if len(data) > 0:
          print("if")
          return render(request,"wishlist.html",{'result':wishlist})

     return render(request,"wishlist.html",{'result':wishlist})
# views.py

def checkout(request):
    if 'userid' not in request.session:
        return redirect("/project/login")

    if request.method == "POST":
        userid = request.session['userid']
        address = request.POST.get('address', '')
        payment = request.POST.get('pay_mode', None)

        # Retrieve cart items for the user
        cart_items = models.cart.objects.filter(userid=userid)
        
        # Initialize variables
        total_amount_usd = 0
        products = []  # List to store products for rendering in template

        for cart_item in cart_items:
            product = models.product.objects.get(id=cart_item.productid)  # Fetch the product object
            if product:
                # Calculate total amount for the product
                total_amount_for_item = product.price * cart_item.quantity
                
                # Add total amount to the total
                total_amount_usd += total_amount_for_item

                # Retrieve seller ID from the product
                seller_id = product.sellerid

                # Save the seller ID along with the order
                order = models.orders.objects.create(
                    address=address,
                    payment_mode=payment,
                    amount=total_amount_for_item,
                    seller=seller_id,  # Save the seller ID
                    orderid=product.id,
                    cartid=product.categoryid,
                    userid=userid
                )
                order.save()

                products.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': cart_item.quantity,
                    'seller': product.sellerid,
                    'cartid': product.categoryid,
                    'total_amount_for_item': total_amount_for_item
                })

        # Clear the user's cart after placing the order
        cart_items.delete()

        # Redirect to home page with success message
        return render(request, "home.html", {'message': 11, 'products': products, 'total_amount_usd': total_amount_usd})

    # Render the checkout page
    return render(request, "checkout.html")

def remove_from_wishlist(request,productid): 
     print(productid)
     userid = request.session['userid']
     print(userid)
     models.wishlist.objects.filter(productid=productid,userid=userid).delete() 
     return redirect("/project/wishlist/0")    
    
def removeFromCartList(request,productid): 
     print(productid)
     userid = request.session['userid']
     print(userid)
     models.cart.objects.filter(productid=productid,userid=userid,quantity=1).delete() 
     return redirect("/project/cart")


def addToCart(request,product_id):
     userid= request.session['userid']
     data = models.cart.objects
     form = data.create(userid=userid,productid=product_id,quantity=1)
     form.save()
     return redirect("/project/cart")

# def orderHistory(request):
#     if 'userid' not in request.session:
#         return redirect("/project/login")

#     userid = request.session['userid']
#     orders = models.orders.objects.filter(userid=userid)
#     products = []

#     for order in orders:
#         order_items = models.orders.objects.filter(id=userid)
#         order_products = []

#         for item in order_items:
#             product = models.product.objects.get(id=item.id)
#             product_data = {
#                 'product_name': product.name,
#                 'price': product.price,
#                #  'qty': item.quantity,
#                 'total': product.price ,
#                 'image': product.image.url if product.image else None
#             }

#             order_products.append(product_data)

#         order_info = {
#             'id': order.id,
#             'order_products': order_products,
#             'address': order.address,
#             'payment_mode': order.payment_mode,
#             'amount': order.amount,
#             'status': order.status,
#             'sellerid': order.sellerid,
#             # Add other fields as needed
#         }
#         products.append(order_info)

#     return render(request, "history.html", {'products': products})
from django.shortcuts import render, redirect
from .models import orders, product

def orderHistory(request):
    if 'userid' not in request.session:
        return redirect("/project/login")

    userid = request.session['userid']
    orders = models.orders.objects.filter(userid=userid)
    order_details = []

    for order in orders:
        order_items = product.objects.filter(id=order.orderid)
        order_products = []

        for item in order_items:
            product_data = {
                'product_name': item.name,
                'price': item.price,
               #  'total': item.price * item.quantity,
                'image': item.image.url if item.image else None
            }
            order_products.append(product_data)

        order_info = {
            'id': order.id,
            'order_products': order_products,
            'address': order.address,
            'payment_mode': order.payment_mode,
            'amount': order.amount,
            'orderid':order.orderid,
            'status': order.status,
            'sellerid': order.seller,
        }
        order_details.append(order_info)

    return render(request, "history.html", {'order_details': order_details})


def logout(request):
     if 'userid' in request.session:
      del(request.session['userid'])
     return redirect("/project/login")

def forgot_password(request):
     if request.method == "POST":
          email = request.POST['email']
          subject = 'Forgot Password'
          message = 'New password is '
          # from_email = 'hevinharvin5@gmail.com'
          to_email = [email]
          send_mail(subject, message,"hevinharvin5@gmail.com", to_email)
          print('Email sent successfully')
     return render(request,"forgot_password.html")

def contact_us(request):
    if request.method == "POST":
            userid = request.session.get('userid')
            try:
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                mobile_no = request.POST['mobile_no']
                message = request.POST['message']
                
                # Get the user ID of the logged-in user
                user_id = request.user.id
                
                # Create a new contact object associated with the logged-in user
                contact = models.contact.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    mobile_no=mobile_no,
                    message=message,
                    userid=userid  # Associate the contact with the logged-in user
                )
                
                print(f"User ID: {user_id} First Name: {first_name} Last Name: {last_name} Email: {email} Mobile No: {mobile_no} Message: {message}")
                
                return render(request, "contact_us.html", {'message': 'Successful', 'response': 2})
            except Exception as e:
                print(f"Error: {str(e)}")
               #  return render(request, "login.html", {"message": "Please Login Here", 'response' :5})
            # Redirect to the login page
 
    return render(request,"contact_us.html")
from django.contrib import messages
from django.http import HttpResponseRedirect

def update_user(request, id):
    if request.method == "POST":
        try:
            data = models.user.objects.get(id=id)

            # Update user fields based on form data
            data.name = request.POST.get('name', data.name)
            data.email = request.POST.get('email', data.email)
            data.password = request.POST.get('email', data.password)
            data.contact = request.POST.get('contact', data.contact)
            data.city = request.POST.get('city', data.city)
            data.address = request.POST.get('address', data.address)
            data.pincode = request.POST.get('pincode', data.pincode)

            data.save()
            messages.success(request, 'Data updated successfully.')
        except models.user.DoesNotExist:
            messages.error(request, 'User with specified ID does not exist.')
        except Exception as e:
            messages.error(request, f'Error updating data: {str(e)}')
    else:
        messages.error(request, 'Invalid request method.')

    return HttpResponseRedirect(f'/project/user_profile/{id}')



def feedback(request):
        if request.method == "POST":
            userid = request.session.get('userid')
            try:
                title = request.POST['title']
                description = request.POST['description']
              
                # Get the user ID of the logged-in user
                user_id = request.user.id
                
                # Create a new contact object associated with the logged-in user
                contact = models.feedback.objects.create(
                    title=title,
                    description=description,
                    userid=userid  # Associate the contact with the logged-in user
                )
                
                print(f"User ID: {user_id} title: {title} description: {description} ")
                
                return render(request, "feedback.html", {'message': 'Successful', 'response': 6})
            except Exception as e:
                print(f"Error: {str(e)}")
               #  return render(request, "login.html", {"message": "Please Login Here", 'response' :5})
        return render(request,"feedback.html")
def aboutus(request):
     return render(request,'aboutus.html')


def user_profile(request):
    logged_in_user_id = request.session.get('userid')
    
    if not logged_in_user_id:
        # If no user is logged in, redirect to the login page
        return redirect('login')

    try:
        # Retrieve the user instance using the ID from the session
        logged_in_user = models.user.objects.get(pk=logged_in_user_id)
        
    except models.user.DoesNotExist:
        # Handle the case where the logged-in user does not exist
        # For example, redirect them to the login page
        return redirect('login')

    if request.method == "POST":
        # Update the user's information based on the form data
        logged_in_user.name = request.POST.get('name')
        logged_in_user.email = request.POST.get('email')
        logged_in_user.password = request.POST.get('password')
        logged_in_user.contact = request.POST.get('contact')
        logged_in_user.city = request.POST.get('city')
        logged_in_user.address = request.POST.get('address')
        logged_in_user.pincode = request.POST.get('pincode')

        # Save the changes to the user instance
        logged_in_user.save()
        
        # Redirect back to the user profile page
        return redirect('user_profile')
    
    # Render the user profile page with the logged-in user's information
    return render(request, 'user_profile.html', {'user': logged_in_user})

