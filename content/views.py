from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, SeekingAdForm  
from .models import MusicianBandChoice, SeekingAd 

def comment(request):
    if request.method == 'GET':
        form = CommentForm()
    else:  # POST
        form = CommentForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            comment = form.cleaned_data["comment"]

            message = f"Received comment from {name}\n\n{comment}"
            send_mail(
                "Received comment", 
                message,
                "admin@example.com", 
                ["admin@example.com"],
                fail_silently=False
            )
            return redirect("comment_accepted")

    return render(request, "comment.html", {"form": form})

def comment_accepted(request):
    return render(request, 'comment_accepted.html')

def ads_list(request):
    ads = SeekingAd.objects.all().order_by('-date')
    return render(request, 'ads_list.html', {'ads': ads})

def list_ads(request):
    data = {
        'seeking_musician': SeekingAd.objects.filter(seeking=MusicianBandChoice.MUSICIAN),
        'seeking_band': SeekingAd.objects.filter(seeking=MusicianBandChoice.BAND),
    }
    return render(request, "list_ads.html", data)

@login_required
def seeking_ad(request, ad_id=0):
    if request.method == 'GET':
        if ad_id == 0:
            form = SeekingAdForm()
        else:
            ad = get_object_or_404(SeekingAd, id=ad_id, owner=request.user)
            form = SeekingAdForm(instance=ad)
    else:  # POST
        if ad_id == 0:
            form = SeekingAdForm(request.POST)
        else:
            ad = get_object_or_404(SeekingAd, id=ad_id, owner=request.user)
            form = SeekingAdForm(request.POST, instance=ad)

        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()
            return redirect("list_ads")

    return render(request, "seeking_ad.html", {"form": form})