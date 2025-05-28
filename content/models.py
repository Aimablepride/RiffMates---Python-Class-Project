from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from band.models import Musician, Band

class SeekingChoice(models.TextChoices):
    MUSICIAN = "M", "Musician"
    BAND = "B", "Band"

class MusicianBandChoice(models.TextChoices):  #1
    MUSICIAN = "M", "Musician"
    BAND = "B", "Band"

class SeekingAd(models.Model):
    date = models.DateField(auto_now_add=True)  #2
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )  #3
    seeking = models.CharField(
        max_length=1,
        choices=MusicianBandChoice.choices
    )  #4
    musician = models.ForeignKey(
        Musician,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )  #5
    band = models.ForeignKey(
        Band,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )  #6
    content = models.TextField()  #7

    class Meta:
        ordering = ["-date"]  #8 (changed to descending order by date)

    def __str__(self):
        return f"SeekingAd(id={self.id}, seeking={self.seeking})"

    def clean(self):
        if self.seeking == MusicianBandChoice.MUSICIAN:
            # Validate seeking musician case  #10
            if self.band is None:
                raise ValidationError(
                    "Band field required when seeking a musician"
                )
            if self.musician is not None:
                raise ValidationError(
                    "Musician field should be empty for a band seeking a musician"
                )
        else:
            # Validate seeking band case  #11
            if self.musician is None:
                raise ValidationError(
                    "Musician field required when seeking a band"
                )
            if self.band is not None:
                raise ValidationError(
                    "Band field should be empty for a musician seeking a band"
                )
        return super().clean()