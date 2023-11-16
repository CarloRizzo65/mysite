from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.conf import settings
from django.urls import reverse #Serve per riscrivere un url

#Librerie per Resize Img
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToCover, ResizeToFill

#Per cancellare le immagini
from django_cleanup import cleanup

#Per caricare l'editor di testo avanzato
from ckeditor.fields import RichTextField #Senza la funzione di upload delle immagini
from ckeditor_uploader.fields import RichTextUploadingField #Con la possibilità di fare l'upload delle immagini

#Librerie per Espandere le informazioni su utenti
from django.contrib.auth.admin import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    categoria_principale = models.ForeignKey('self', related_name='sottocategorie', on_delete=models.CASCADE, null=True, blank=True, default=None)

    class Meta:
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome'])
        ]

        unique_together = ('slug','categoria_principale')
        verbose_name = 'categoria'
        verbose_name_plural = 'categorie'

    def __str__(self):
        fullpath = [self.nome]
        k = self.categoria_principale
        while k is not None:
            fullpath.append(k.nome)
            k = k.categoria_principale
        fullpath.reverse()
        return "-->".join(fullpath)

    @property
    def catstr(self):
        return str(self)

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])

@cleanup.select
class Prodotto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='prodotti', on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    img = models.ImageField(upload_to='img_prodotti/%Y/%m/%d/', default='img_prodotti/no-image.jpg')
    img_resized = ImageSpecField(source='img',
                                      processors=[ResizeToFill(600,800)],
                                      format='PNG',
                                      options={'quality': 60})
    descrizione = RichTextField(blank=True)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)
    quantita = models.IntegerField("Quantità in magazzino", default=0)
    pubblicato = models.BooleanField(default=False)
    data_inserimento = models.DateTimeField(auto_now_add=True)
    data_modifica = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        indexes = [
            models.Index(fields=['id','slug']),
            models.Index(fields=['nome']),
            models.Index(fields=['-data_inserimento']),
        ]
        verbose_name = 'prodotto'
        verbose_name_plural = 'prodotti'

    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse("shop:dettaglio_prodotto", args=[self.id, self.slug])
    
    def img_preview(self):
        return mark_safe(f'<img src="{self.img.url}" width="150" />')
