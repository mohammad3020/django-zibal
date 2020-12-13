
Zibal
=====

A Django app for bank payments by Zibal (https://zibal.ir/)

Detailed documentation is in the "docs" directory.

Quick start
-----------
### 0. install

    pip install requests
    pip install zibal-django
    
### 1. start
Add "zibal" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'zibal',
    ]

### 2. migrate
Run ``python manage.py migrate`` to create the zibal models.

### 3. admin
Start the development server and visit http://127.0.0.1:8000/admin/
to create a zibal (you'll need the Admin app enabled).

### 4.Instructions
For each transaction you first need to request and then confirm it.
For this operation, you can use 2 methods : request and callback.
You can use the Request method anywhere in the project. For the callback method, it is recommended to write once in a view with a fixed address and always use it.

### 4.1. user request method :
Suppose in a Django view we want to send a user to the bank page. In the first step you have to import the dependencies and set the Merchant variable  ! Merchant code will be given to you after registering on Zibal site. For testing, as mentioned in the documents of Zibal site, the amount of merchant can be set to zibal


```sh
from django.http import HttpResponse
from django.shortcuts import render, redirect
from zibal.zb import Zibal as zb

merchant = "zibal" # example : merchant = "8g8xx74718f4341b02503xx8"

``` 

Now suppose we want to write a view function called request_test() or whatever name you want.
You must first create an object of zb (In the previous step, we imported it) and its input argument is Merchant, which we defined above as a variable.
The zb class has several methods. The "request" method that we want to use now has several inputs, which you can see below the list and its description, and its output has two modes! If there is no error, it is a link to which you should redirect the user, and if an error occurs, it will show you the error. In this case (error occurs) , I used HttpResponse to show the error to the user directly and raw! But you can use all the features of Django here, for example, use Django Template and show a beautiful HTML page to the user or ...

order : This is a number for you that you can use to search for a transaction in the future
In the database of this package, a special order_id is registered for each transaction, which is different from this order number! Note that this number is not unique, if you do not want to use it, give it a value of -1
mobile : Buyer contact number
description : Purchase description
callback_url : We'll talk about callback in the next section, don't forget to quantify it in the future

```sh
def request_test(request):
    order = 78
    amount = 100000 # Rial !!! 
    mobile = 09120987654
    description = "In publishing and graphic design, Lorem ipsum is a placeholder text commonly"
    callback_url = "http://example.com/zibal/callback/"
    
    zb_object = zb(merchant)
    data = zb_object.request(callback_url ,order , amount , mobile , description , request.user )
    if data['status'] == "successful":
        return redirect(data['start_pay_url'])
    else:
        return HttpResponse(data["message"])
``` 


### 4.2 user callback method
excellent ! So far, the user has been sent to the bank page and has made his payment successful or unsuccessful. It will now be returned to our site for us to confirm.
Here we first write a view Django function and then define it in the urls.py 

Like the previous series, first create an object from the beauty class and then call it the callback method. This method has only one input, that you must give the request (input of this view function)

```sh
def callback(request):
    zb_obj = zb(merchant)
    data = zb_obj.callback(request)
    purchase_history_object = data["PurchaseHistory"]
    if data['status'] == "successful":
        return HttpResponse(data['message'])
    else:
        return HttpResponse(data["message"])
``` 

All calculations are done and the message of successful or unsuccessful payment is shown to the user in raw form (by HttpResponse method), provided that you see that like the previous series, you can use all Django features such as Django Template, etc. for a better display.


### 5. Database
In this package, there is a model called PurchaseHistory that stores all the information from the time the user is sent to the bank until his return. You will quantify a lot of information by calling the Request method in Section 4.1 with its input arguments.
Now you can use Django ORM to query your desired queries on this database and perform your operations! For example, in section 4.2, after the user confirms, you have a variable called purchase_history_object, which is an object of the paid model.

Below is an overview of the model:

```sh
class PurchaseHistory(models.Model):
    user = models.ForeignKey(User , on_delete =models.CASCADE , null=True , blank=True)
    amount = models.IntegerField(help_text="Rial")
    order = models.CharField(max_length=30 , null=True , blank=True)
    is_call_verify = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    trackId = models.CharField(max_length=255 , null=True , blank=True)
    result = models.CharField(max_length=255 , null=True , blank=True)
    message = models.CharField(max_length=255 , null=True , blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    paidAt = models.DateTimeField(null=True , blank=True)
    cardNumber = models.CharField(max_length=255 , null=True , blank=True)
    refNumber = models.CharField(max_length=255 , null=True , blank=True)

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
``` 


### 6. Good luck :) 
Bye
