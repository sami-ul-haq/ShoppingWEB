from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Product, Contact , Orders , OrderUpdate
from math import ceil
import json
# Create your views here.

def index(request):
    #products = Product.objects.all()
    #print(products)
    #n = len(products)
    # nslides = n//4+ ceil((n//4)-(n//4))
    #params = {'products':products , 'range':range(1,nslides) , 'no_of_slides':nslides}
    #allProds = [[products, range(nslides) , nslides],
            #    [products, range(nslides) , nslides] ]

    allProds = []
    catProds = Product.objects.values('category')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n // 4) - (n // 4))
        allProds.append([prod , range(1,nslides) , nslides])
    params = {'allProds' : allProds }
    return render(request, './shop/index.html' , params)




def about(request):
    return render(request, './shop/about.html')

def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name' , '')
        email = request.POST.get('email' , '')
        phone = request.POST.get('phone' , '')
        message = request.POST.get('message' , '')
        contact = Contact(name=name , email=email , phone= phone , message=message )
        contact.save()
        thank = True
    return render(request, './shop/contact.html' , {'thank': thank})

# def tracker(request):
#     if request.method == 'POST':
#         orderid = request.POST.get('orderid' , '')
#         email = request.POST.get('Email' , '')
#         try:
#             order = Orders.objects.filter(order_id=orderid , email= email)
#             if len(order)>0:
#                 update = OrderUpdate.objects.filter(order_id=orderid)
#                 updates = []
#                 for item in update:
#                     updates.append({'text': item.update_desc, 'time':item.timestamp})
#                     response = json.dumps(updates , default=str)
#                 return HttpResponse(response)
#             else:
#                 return HttpResponse('{}')

#         except Exception as e:
#             return HttpResponse('{}')
#     return render(request, './shop/tracker.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].itemjason], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, './shop/search.html')

def productView(request , myid):
    product = Product.objects.filter(id=myid)
    return render(request, './shop/productView.html', {'product':product[0]})

def checkOut(request):
    if request.method == 'POST':
        itemjason = request.POST.get('itemsjson' , '')
        name = request.POST.get('Name' , '')
        email = request.POST.get('Email' , '')
        address = request.POST.get('Address1' , '')+" "+request.POST.get('Address1' , '')
        city = request.POST.get('City' , '')
        state = request.POST.get('State' , '')
        zip_code = request.POST.get('Zip_code' , '')
        phone = request.POST.get('Phone' , '')
        order = Orders(itemjason = itemjason , name = name ,email = email ,address = address,city=city,state = state,zip=zip_code, phone= phone)
        #order.save()

        # thank = True
        # update = OrderUpdate(update_id=order.order_id , update_desc="Your Order Has Been Placed")
        # orderid = order.order_id
        # update.save()
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id}) 
    return render(request, './shop/checkOut.html')
