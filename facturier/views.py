from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.db import transaction
from .serialisers import FacSerial
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .pagination import pgt,ct
import pdfkit as pdf
import datetime as dt
from django.utils.translation import gettext as _
from django.template.loader import get_template

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
    def post(self,request,*args,**kwags):
        
        id_j=request.POST.get('id_modified')
    
        if id_j:
            paid = request.POST.get('modified')
            try:
                fac=Facture.objects.get(id=id_j)
                if paid == 'True':
                    fac.payer=True
                else:
                    fac.payer= False
                fac.save() 

                messages.success(request,  _("Change made successfully.")) 
                    
            except Exception as e:
                  messages.error(request, f"Sorry, the following error has occured {e}.")  
        if request.POST.get('id_supprimer'):
            print(request.POST.get('id_supprimer'))
            try:
                obj = Facture.objects.get(id=request.POST.get('id_supprimer'))
                obj.delete()
                messages.success(request, _("The deletion was successful.")) 
            except Exception as e:
                messages.error(request, f"Sorry, the following error has occured {e}.") 
        
        item_page=pgt(request,self.invoices)              
        self.context['invoices']=item_page
        return render(request,self.template_name,self.context) 
 
 
class voirArticleHtm(View):
    template_name='facturier/facture.html'
    def get(self,request,*args,**kwags):
        id=kwags.get('pk')
        context=ct(id) 
        return render(request,self.template_name,context)

def get_fac(request,*args,**kwags):
    pk=kwags.get('pk')
    context=ct(pk)
    context['date']=dt.datetime.today()
    template= get_template('facturier/facturepdf.html')
    ht=template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }
    config = pdf.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe") #replace with your path
     
    file=pdf.from_string(ht,False,options,configuration=config)
    r= HttpResponse(file,content_type='application/pdf')
    r['Content-Disposition'] = "attachement"
    return r
    
    
    
    



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