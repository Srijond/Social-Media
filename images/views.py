from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from bookmarks.common.decorators import ajax_required
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import Image

# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request,'Image added successfully')

            return redirect(new_item.get_absolute_url())
    
    else:
        mutable_get = request.GET.copy()
        title_value = mutable_get.get('title')
        del mutable_get['title']
        mutable_get['titile'] = title_value
        form = ImageCreateForm(data=mutable_get)
    return render(request,'images/image/create.html',{'section':'images','form':form})

def image_detail(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    # when user upload the pics own user like put
    like_user_manager = image.users_like
    like_user_manager.add(request.user)
    return render(request,'images/image/detail.html',{'section':'images','image':image})

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
        except:
            pass

    return JsonResponse({'status':'ok'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images,8)
    page = request.GET.get('page') 
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)

    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        
        images = paginator.page(paginator.num_pages)
        

    if request.is_ajax():
        return render(request,'images/image/list_ajax.html',{'section':'images','images':images})

    return render(request,'images/image/list.html',{'section':'images','images':images})
