from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.conf import settings
from django.urls import reverse #Serve per riscrivere un url

#Librerie per Resize Img
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToCover

#Per cancellare le immagini
from django_cleanup import cleanup

#Per caricare l'editor di testo avanzato
from ckeditor.fields import RichTextField #Senza la funzione di upload delle immagini
from ckeditor_uploader.fields import RichTextUploadingField #Con la possibilità di fare l'upload delle immagini

#Librerie per Espandere le informazioni su utenti
from django.contrib.auth.admin import User
from django.dispatch import receiver
from django.db.models.signals import post_save
#importo il validatore
from django.core.validators import RegexValidator
# Create your models here.
class CategoriaSlide(models.Model):
    titolo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    descrizione = models.CharField(max_length=150, default="")

    def __str__(self) -> str:
        return self.titolo

@cleanup.select
class Slide(models.Model):
    #Come codice userò l'id generato dal DB
    titolo = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150,default='')
    sottotitolo = models.CharField(max_length=255)
    #contenuto = RichTextField(default='')
    contenuto = RichTextUploadingField(default='')
    categoria = models.ForeignKey(CategoriaSlide, on_delete=models.SET_NULL, default=1, null=True)
    img = models.ImageField("Immagine da visualizzare", null=True, blank=True, upload_to='img_slide/',default="no-image.png")
    img_resized = ImageSpecField(source='img',
                                      processors=[ResizeToCover(800,800)],
                                      format='PNG',
                                      options={'quality': 60})
    img_visibile = models.BooleanField("Pubblicata", default=False)
    data_inserimento = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.titolo}"
    
    def img_preview(self):
        return mark_safe(f"<img src='{self.get_image()}' width='120'>")

    #Riscrivo la url
    def get_absolute_url(self):
        return reverse("slide", args=[self.id, self.slug])
    
    def get_image(self):
        if not self.img:
            return f'{settings.MEDIA_URL}no-image.png'
        return self.img.url
    
    def get_image_url(self):
        if not self.img:
            return f'{settings.MEDIA_URL}no-image.png'
        return self.img_resized.url
    

#MODELS PER UTENTI
#Vado ad incrementare le informazioni di base sull'utente
@cleanup.select
class UserProfile(models.Model):
    #Creo le scelte per il campo di tipo select
    ACCOUNT_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('developer', 'Developer'),
        ('cliente', 'Cliente')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Creo la relazione uno a uno con Utente
    cf = models.CharField(max_length=16, blank=True, null=True, validators=[
            RegexValidator(
                regex=r'(?i)[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]',
                message="Inserisci un cap corretto",
                code="invalid_registration",
            ),
        ])
    data_nascita = models.DateField("Data di nascita", null=True, blank=True)
    tipo_account = models.CharField("Tipologia Utente", max_length=50, default='cliente', choices=ACCOUNT_TYPE_CHOICES)
    img_profilo = ProcessedImageField(upload_to='user_profile/%Y/%m/%d/', processors=[ResizeToCover(128,128)], format='PNG', options={'quality':60}, default='user_profile/no-user.png')
    indirizzo = models.CharField(max_length=255, blank=True, null=True)
    comune = models.CharField(max_length=255, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    cap = models.CharField(max_length=5, blank=True, null=True, validators=[
            RegexValidator(
                regex=r'[0-9]{5}',
                message="Inserisci un cap corretto",
                code="invalid_registration",
            ),
        ])


    def __str__(self):
        return self.user.username
    
    #Metodo per visulizzare l'immagine in admin
    def img_preview(self):
        return mark_safe(f'<img src="{self.img_profilo.url}" width="100" />')
    
    def save(self, *args, **kwargs):
        self.cf = self.cf.upper()
        super(UserProfile, self).save(*args, **kwargs)
    
    #Salvo il profilo utente appena si crea un nuovo utente nel DB
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)