from django.shortcuts import get_object_or_404, render, redirect
from .models import Slide
from .forms import LoginForm

# Create your views here.
def index(request):
    slides = Slide.objects.filter(categoria__titolo='Home', img_visibile=True)
    return render(request, 'account/index.html', { 'slides':slides })

def about(request):
    slides = Slide.objects.filter(categoria__titolo='Cellulari', img_visibile=True)
    return render(request, 'account/about.html', { 'slides':slides })
