from django.contrib import admin
from .models import Client, Facture ,Article

class VueClient(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'addresse', 'sexe', 'age', 'date_added')

class ViewInvoice(admin.ModelAdmin):
    list_display = ('saved_by', 'dateajoutfac', 'client','total', 'last_update', 'payer', 'typedf')    

class ViewArticle(admin.ModelAdmin):
    list_display=('fac','name','quantite','prix_unitaire')

admin.site.register(Client,VueClient)
admin.site.register(Facture,ViewInvoice)
admin.site.register(Article,ViewArticle)




# Register your models here.
