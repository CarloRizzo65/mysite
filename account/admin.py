from django.contrib import admin
from .models import Slide, CategoriaSlide, UserProfile
from django.http import HttpResponse

#Per aggiungere UserProfile dentro la vista User
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(CategoriaSlide) #Alternativa con Decoratore
class CategoriaSlideAdmin(admin.ModelAdmin):
    list_display = ['titolo','slug','descrizione'] #Crea le colonne nella visualizzazione del blog
    search_fields = ['titolo','descrizione'] #Creo una barra di ricerca e specifico su quali campi della tabella deve cercare
    list_filter = ['titolo'] #Menù laterale con il filtro dei campi desiderati
    prepopulated_fields = {'slug':('titolo',)} #Serve a popolare un campo in base ad un'altro campo del form

@admin.register(Slide) #Alternativa con Decoratore
class SlideAdmin(admin.ModelAdmin):
    list_display = ['img_preview','titolo','slug','categoria', 'img_visibile','sottotitolo','contenuto','data_inserimento'] #Crea le colonne nella visualizzazione del blog
    list_editable = ['titolo','slug','img_visibile','categoria','sottotitolo','contenuto']
    list_display_links = ['img_preview']
    search_fields = ['titolo','sottotitolo','contenuto','categoria'] #Creo una barra di ricerca e specifico su quali campi della tabella deve cercare
    list_filter = ['img_visibile','titolo','data_inserimento','categoria'] #Menù laterale con il filtro dei campi desiderati
    readonly_fields = ['img_preview'] #Per visualizzare immagine in Admin
    prepopulated_fields = {'slug':('titolo',)} #Serve a popolare un campo in base ad un'altro campo del form
  
    class Media:
        css = {
            "screen": ["css/admin.css"],
        }

#Area Utenti
class CustomUserAdmin(admin.StackedInline): #Serve a inserire nella visualizzazione User altre tabelle
    model= UserProfile
    can_delete = False
    readonly_fields = ['img_preview']
    
#Creo la nuva visualizzazione dell'account User in Admin
class AccountsUserAdmin(UserAdmin):
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(AccountsUserAdmin, self).add_view(*args,**kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [CustomUserAdmin]
        return super(AccountsUserAdmin, self).change_view(*args,**kwargs)

admin.site.unregister(User)
admin.site.register(User,AccountsUserAdmin)