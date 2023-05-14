from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages
from django.db import transaction
from .serialisers import FacSerial
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .pagination import pgt



class AccueilView(View):
    template_name='facturier/index.html'
    invoices = Facture.objects.all()
    context={
        "invoices":invoices
    }
    def get(self,request,*args,**kwags):
        item_page=pgt(request,self.invoices)
        
            
        
        self.context['invoices']=item_page
        return render(request,self.template_name,self.context)    
    
    
    
class AddClient(View):
    template_name='facturier/ajout_client.html'
    def get(self,request,*args,**kwags):
        return render(request,self.template_name)   
    @transaction.atomic
    def post(self,request,*args,**kwags):
        print(request.POST)
        data = {
            'nom': request.POST.get('name'),
            'email': request.POST.get('email'),
            'telephone': request.POST.get('phone'),
            'addresse': request.POST.get('address'),
            'sexe': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'added_by': request.user

        }

        try:
            created = Client.objects.create(**data)

            if created:

                messages.success(request, "Customer registered successfully.")

            else:

                messages.error(request, "Sorry, please try again the sent data is corrupt.")

        except Exception as e:    

            messages.error(request, f"Sorry our system is detecting the following issues {e}.")
        return render(request,self.template_name)  
class AddFacture(View):
    template_name='facturier/ajout_facture.html' 
    custumers=Client.objects.all()
    context={
        'customers':custumers
    }
    def get(self,request,*args,**kwags):
        return render(request,self.template_name,self.context)   
    
    
    @transaction.atomic
    def post(self,request,*args,**kwags):
       
        items=[]
        customer = request.POST.get('customer')
        print(type(customer))
        f=int(customer)
        print(type(f))
        clien=Client.objects.get(id=f)
        try: 
           

            typedf = request.POST.get('invoice_type')

            articles = request.POST.getlist('article')

            qties = request.POST.getlist('qty')

            units = request.POST.getlist('unit')

            total_a = request.POST.getlist('total-a')

            total = request.POST.get('total')

            comment = request.POST.get('commment')
          
            invoice_object = {
                'client': clien,
                'saved_by': request.user,
                'total': total,
                'typedf': typedf,
                'comments': comment
            }
            print(invoice_object)
            print(self.custumers)

            invoice = Facture.objects.create(**invoice_object)

            for index, article in enumerate(articles):

                data = Article(
                    fac = invoice,
                    name = article,
                    quantite=qties[index],
                    prix_unitaire = units[index],
                    total = total_a[index],
                )

                items.append(data)
            
            created = Article.objects.bulk_create(items)   
            invoice.save()
            if created:
                messages.success(request, "Données enregistrées avec succès.") 
                print(request.POST)
            else:
                messages.error(request, "Desolé, vérifiez vos données")    

        except Exception as e:
                messages.error(request,f"Erreur {e}")
        
        
        
        return  render(request,self.template_name,self.context)