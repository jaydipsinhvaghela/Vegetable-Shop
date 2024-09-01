from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from json import dumps
from bson import json_util
import re
from django.shortcuts import redirect
from django.contrib import messages
import project.models as models
from django.http import JsonResponse
from django.core.serializers import serialize

# =====================================================================================================

def getFormatedData(data):
     my_data=[]
     for row in data:
          my_data.append(row)
     json_data = dumps(my_data,default=json_util.default)
     return json_data

# =====================================================================================================

# <---------================= Function =================-------------->
def is_valid_email(email):
    # Define the regular expression pattern for a basic email address
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Use re.match to check if the email matches the pattern
    match = re.match(pattern, email)
    
    # If match is not None, the email is valid; otherwise, it's not
    return match is not None
# <---------================= views =================-------------->

def home(request):
     return render(request,'admin_template.html')
def s_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email is valid
      
        # Check if the password meets the minimum length requirement
       

        # Query the database for a seller with the provided email and password
        try:
            seller_instance = models.seller.objects.get(email=email, password=password)
        except models.seller.DoesNotExist:
            # If no seller found with the provided credentials, display an error message
            message = "Incorrect email or password"
            return render(request, 's_login.html', {'message': message, 'response': 0})

        # If seller authentication is successful, store the seller id in session
        request.session['seller_id'] = seller_instance.id
        return render(request, "dashboard.html", {'message': 'Login success', 'response': 2})

    else:
        # If not a POST request, render the login page
        return render(request, 's_login.html')



def s_register(request):
     if request.method == "POST":
          print(request.POST)
          try:
               sellername  = request.POST['sellername']
               contact  = request.POST['contact']
               email = request.POST['email']
               password = request.POST['password']
               city = request.POST['city']
               pincode = request.POST['pincode']
               address = request.POST['address']
               data = models.seller.objects
               form = data.create(name=sellername,contact=contact,email=email,password=password,city=city,pincode=pincode,address=address)
               form.save()
               print(f"sellername is {sellername} contact is {contact} email is {email} password is {password} city is {city} pincode is {pincode} address is {address}")    
               # request.session['message'] = 'Register Successfully ' 
               return render(request,"s_login.html",{'message':'Register Successfull','response':2})
          except:
               return render(request,"s_register.html",{ "message" : "Invalid Register Attempt " })
     return render(request,'s_register.html')

def add_product(request):
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        image = request.FILES['image']
        stock = request.POST['stock']
        category = request.POST['category']
        description = request.POST['description']
        
        # Get the seller's ID from the session
        seller_id = request.session.get('seller_id')
        
        if seller_id:
            try:
                # Retrieve the seller instance based on the seller ID
                seller = models.seller.objects.get(id=seller_id)
                
                # Create the product associated with the seller
                product = models.product.objects.create(
                    name=name,
                    price=price,
                    image=image,
                    stock=stock,
                    categoryid=category,
                    description=description,
                    sellerid=seller_id  # Link the product to the seller
                )
                
                return render(request, 'add_product.html', {'success': True})
            except models.seller.DoesNotExist:
                # Handle the case where the seller does not exist
                return HttpResponse("Seller does not exist.")
        else:
            # Handle the case where the seller ID is not found in the session
            return HttpResponse("Seller ID not found in session.")
    
    return render(request, 'add_product.html')

def view_product(request):
    # Get the current user's ID from the session
    user_id = request.session.get('seller_id')
    
    if user_id:
        try:
            # Retrieve the seller associated with the current user
            seller = models.seller.objects.get(id=user_id)
            
            # Filter products pased on the seller
            products = models.product.objects.filter(sellerid=user_id)
            
            # Convert queryset to list of dictionaries for passing to template
            response = list(products.values())
            
            return render(request, "view_product.html", {'response': response})
        except models.seller.DoesNotExist:
            # Handle the case where the current user is not identified as a seller
            return HttpResponse("You are not authorized to view this page.")
    else:
        # Handle the case where the user is not logged in
        return HttpResponse("Please log in to view this page.")
def edit_product(request,id):
     print("==============================================")
     print(id)
     print("==============================================")
     if request.method == "POST":
          name = request.POST['name']
          price = request.POST['price']
          stock = request.POST['stock']
          category = request.POST['category']
          description = request.POST['description']

          print(f"name is {name} price is {price} stock is {stock} category is {category} description {description}")

          if len(request.FILES) >= 1:
               image = request.FILES['image']

          data = models.product.objects.get(id=id)
          print(data)
          data.name = name
          data.price = price
          data.stock = int(stock)
          data.categoryid = int(category)
          data.description = description
          if len(request.FILES) >= 1:
               data.image = image
          data.save()
     return redirect('/seller/view_product')

def update_product(request,id):
     data = models.product.objects.filter(id=id).values()
     print("======================================================")
     print(data)
     response = getFormatedData(data)
     print(response)
     print("======================================================")
     return render(request,"edit_product.html",{'response' :response , 'id' : id})


def view_orders(request):
    orders = models.orders.objects.all()
    response = []
    for order in orders:
        # Fetching customer name from the User table
        customer_name = models.user.objects.get(id=order.userid).name
        response.append({'name': customer_name, 'amount': order.amount, 'address': order.address, 'payment_mode': order.payment_mode, 'status': order.status})
    return render(request, "view_orders.html", {'response': response})

def view_feedback(request):
    orders = models.feedback.objects.all()
    response = []
    for order in orders:
        # Fetching customer name from the User table
        customer_name = models.user.objects.get(id=order.userid).name
        response.append({'name': customer_name, 'title': order.title, 'description': order.description})
    return render(request, "view_feedback.html", {'response': response})

def dashboard(request):
     return render(request,'dashboard.html')

def seller_profile(request):
     
    # Get the current seller's ID from the session
    logged_in_seller_id = request.session.get('seller_id')
    
    if not logged_in_seller_id:
        # If no seller is logged in, redirect to the login page
        return redirect('s_login')

    try:
        # Retrieve the seller instance using the ID from the session
        logged_in_seller = models.seller.objects.get(pk=logged_in_seller_id)
        
        # Set the seller's name in the session
        request.session['name'] = logged_in_seller.name
    except models.seller.DoesNotExist:
        # Handle the case where the logged-in seller does not exist
        # For example, redirect them to the login page
        return redirect('s_login')

    if request.method == "POST":
        # Update the seller's information based on the form data
        logged_in_seller.name = request.POST.get('name')
        logged_in_seller.email = request.POST.get('email')
        logged_in_seller.contact = request.POST.get('contact')
        logged_in_seller.address = request.POST.get('address')
        logged_in_seller.city = request.POST.get('city')
        logged_in_seller.pincode = request.POST.get('pincode')
        
        # Save the changes to the seller instance
        logged_in_seller.save()
        
        # Redirect back to the seller profile page
        return redirect('seller_profile')
    
    # Render the seller profile page with the logged-in seller's information
    return render(request, 'seller_profile.html', {'seller': logged_in_seller})


    # Pass the logged-in seller instance to the template for rendering
#     return render(request, 'seller_profile.html', {'seller': logged_in_seller})


def delete_product(request,id):
     models.product.objects.filter(id=id).delete() 
     return redirect("/seller/view_product")

def confirm_order(request,id):
     order = models.orders.objects.get(id=id)
     order.status = 1 
     order.save()
     return redirect("/seller/view_orders")

def completed_order(request,id):
     order = models.orders.objects.get(id=id)
     order.status = 2
     order.save()
     return redirect("/seller/view_orders")
from django.contrib import auth
def s_logout(request):
   
    # Clear the session data for the seller
    auth.logout(request)
    return redirect('s_login')