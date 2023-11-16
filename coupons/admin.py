from django.contrib import admin
from .models import Coupon
# Register your models here.

@admin.register(Coupon) #Alternativa con Decoratore
class CouponAdmin(admin.ModelAdmin):
    list_display = ['codice','valido_da','valido_a','sconto','attivo' ] #Crea le colonne nella visualizzazione del blog
    search_fields = ['codice','valido_da','valido_a','attivo'] #Creo una barra di ricerca e specifico su quali campi della tabella deve cercare
    list_filter = ['codice'] #Menù laterale con il filtro dei campi desiderati