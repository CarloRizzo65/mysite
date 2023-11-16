from django.contrib import admin
from .models import Categoria, Prodotto

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug','categoria_principale']
    prepopulated_fields = {'slug': ('nome', )}

@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    list_display = ['nome','slug', 'img_preview','prezzo', 'quantita','pubblicato','categoria','data_modifica']
    search_fields = ['nome', 'descrizione']
    list_filter = ['pubblicato', 'data_inserimento','data_modifica']
    prepopulated_fields = {'slug':('nome',)}
    readonly_fields = ['img_preview']
    list_editable = ['prezzo','quantita','pubblicato']
