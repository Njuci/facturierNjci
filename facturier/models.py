from django.db import models

from django.contrib.auth.models import User
class Client(models.Model):
    sex_=(
        ('m','masculin'),
        ('f','feminin'),
    )
    nom=models.CharField(max_length=60)
    email=models.EmailField()
    telephone=models.CharField(max_length=20)
    addresse=models.CharField(max_length=160)
    sexe=models.CharField(max_length=1,choices=sex_)
    age=models.CharField(max_length=4)
    date_added=models.DateTimeField(auto_now_add=True)
    added_by=models.ForeignKey(User,on_delete=models.PROTECT)
    
    class Meta:
        verbose_name="client"
        verbose_name_plural="clients"
    def __str__(self):
        return self.nom
    def get_id(self):
        return self.id


class Facture(models.Model):
    inv=(
        ('R','Reçu'),
        ('P','PROFORMA FACTURE'),
        ('F','Facture'))
    client=models.ForeignKey(Client,on_delete=models.PROTECT) 
    saved_by=models.ForeignKey(User,on_delete=models.PROTECT)   
    dateajoutfac=models.DateTimeField(auto_now_add=True)
    total=models.DecimalField(max_digits=120000,decimal_places=4)
    last_update=models.DateTimeField(null=True,blank=True)
    payer=models.BooleanField(default=False)
    typedf=models.CharField(max_length=1,choices=inv,default="F")
    comments=models.TextField(null=True)
    class Meta:
        verbose_name="Facture"
        verbose_name_plural="Factures"
    def __str__(self):
        return "fac000"+str(self.id)
    
    
    
    @property
    def get_total(self):
        arti=self.article_set.all()
        total=sum(article.get_total for article in arti)
        return total
        
        
        
        
class Article(models.Model):
    fac=models.ForeignKey(Facture,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    quantite=models.IntegerField()
    image=models.ImageField(upload_to="article",blank=True,null=True)
    prix_unitaire=models.DecimalField(max_digits=1000,decimal_places=4)
    total=models.DecimalField(max_digits=1000,decimal_places=4)
    
    @property
    def get_total(self):
        total=self.prix_unitaire*self.quantite
        return total