from django.shortcuts import render

VOIVODESHIPS = [
    "Dolnośląskie", "Kujawsko-pomorskie", "Lubelskie", "Lubuskie",
    "Łódzkie", "Małopolskie", "Mazowieckie", "Opolskie",
    "Podkarpackie", "Podlaskie", "Pomorskie", "Śląskie",
    "Świętokrzyskie", "Warmińsko-mazurskie", "Wielkopolskie",
    "Zachodniopomorskie",
]

def index(request):
    return render(request,
                  'core/index.html',
                  {'title':'Main',
                   'voivodeships': VOIVODESHIPS})