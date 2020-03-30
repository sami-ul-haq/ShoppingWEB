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

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "mxg": ""}
    if len(allProds) == 0 or len(query)<2:
        params = {'mxg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


# def searchmatch(query,prod):
#     if query in prod.product_name.lower() or prod.description.lower():
#         print(query)
#         return True
#     else:
#         return False
#
# def search(request):
#     query = request.GET.get('search')
#     allProds = []
#     catProds = Product.objects.values('category')
#     cats = {item['category'] for item in catProds}
#     for cat in cats:
#         prodtemp = Product.objects.filter(category=cat)
#         prod = [item for item in prodtemp if searchmatch(query,item)]
#         n = len(prod)
#         nslides = n // 4 + ceil((n // 4) - (n // 4))
#
#         if len(prod) != 0:
#             allProds.append([prod, range(1, nslides), nslides])
#
#     params = {'allProds': allProds, 'mxg' :''}
#     if len(allProds) == 0 or len(query)<4:
#         params = {'mxg' : 'Please Enter Valid Keys'}
#     return render(request, './shop/search.html', params)




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
