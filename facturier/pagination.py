

from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator     
from .models import Facture       
        
        
def pgt(request,invoices):  

        
    page_par_defaut=1
    page = request.GET.get('page',page_par_defaut)
    
    fac_par_page = 3
    pagination = Paginator(invoices,fac_par_page)
    try:
        item_page=pagination.page(page)
        
    except PageNotAnInteger :
        item_page=pagination.page(page_par_defaut)
    except EmptyPage:
        item_page=pagination.page(pagination.num_pages)
    return item_page

    