from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('titile','url','description')
        widgets = {
            'url':forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg']
        extension = url.rsplit('.',1)[1].lower()
        print('h------ex',extension)
        if extension not in valid_extensions:
            raise forms.ValidationError('The given url does not match valid image extention.')
        return url

    def save(self,force_insert=False,force_update=False,commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.titile)  
        extention = image_url.rsplit('.',1)[1].lower()
        image_name = f'{name}.{extention}'
        #  download image from the given url
        response = request.urlopen(image_url)
        image.image.save(image_name,ContentFile(response.read()),save=False)

        if commit:
            image.save()
        return image