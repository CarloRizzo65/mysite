from django.shortcuts import render, get_object_or_404
from .models import Categoria, Prodotto
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

# def lista_prodotti(request):
#     categorie = Categoria.objects.all()
#     lista_prodotti = Prodotto.objects.all()
#     #Vado a configurare la paginazione
#     """paginator = Paginator(lista_prodotti, 3)#Vado a dire quanti prodotti per pagina devono essere visibili
#     page_number = request.GET.get('page',1)

#     try:
#         lista_prodotti = paginator.page(page_number)
#     except PageNotAnInteger:
#         lista_prodotti = paginator.page(1)
#     except EmptyPage:
#         lista_prodotti = paginator.page(paginator.num_pages)"""
#     return render(request,'shop/lista_prodotti.html', {'categorie':categorie, 'prodotti':lista_prodotti})

def lista_prodotti(request, categoria_slug=None):
    categoria = None
    categorie = Categoria.objects.all()
    prodotti = Prodotto.objects.filter(pubblicato=True)
    #Se viene passata uno slug di categoria faccio i filtri
    if categoria_slug:
        categoria = get_object_or_404(Categoria, slug=categoria_slug)#Salvo in catogoria il nome dello slug
        prodotti = Prodotto.objects.filter(categoria=categoria).filter(pubblicato=True) #Estraggo solo i prodotti della categoria passata
    
    #print(categoria)
    return render(request,'shop/lista_prodotti.html', {'categorie':categorie, 'prodotti':prodotti, 'categoria':categoria})

def dettaglio_prodotto(request, id, slug):
    prodotto = get_object_or_404(Prodotto, id=id, slug=slug, pubblicato=True)
    cart_prodotto_form = CartAddProductForm()
    return render(request, 'shop/dettaglio_prodotto.html', {'prodotto':prodotto,
                                                            'cart_prodotto_form':cart_prodotto_form,
                                                            'max_buy':range(1,prodotto.quantita+1)})