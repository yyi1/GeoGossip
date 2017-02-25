from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db import transaction
from mimetypes import guess_type

from utils import calculate_bounds
from geogossip.forms import *
from geogossip.models import *

import logging

DEFAULT_RADIUS = 500
logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')
    pass


@transaction.atomic
def register(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'registration.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'registration.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email1'],
                                        password=form.cleaned_data['password1'])
    try:
        new_user.save()

        new_user = authenticate(username=form.cleaned_data['username'],
                                first_name=form.cleaned_data['first_name'],
                                last_name=form.cleaned_data['last_name'],
                                email=form.cleaned_data['email1'],
                                password=form.cleaned_data['password1'])

        new_user.profile.first_name = form.cleaned_data['first_name']
        new_user.profile.last_name = form.cleaned_data['last_name']
        new_user.profile.email = form.cleaned_data['email1']
        new_user.profile.password = form.cleaned_data['password1']

        login(request, new_user)
        pass
    except Exception as e:
        logger.error(e.message)
        pass

    return redirect('/')
    pass


@login_required
def get_groups(request):
    if request.method != 'POST':
        raise Http404
    latlon_form = LatLonForm(request.POST)
    if not latlon_form.is_valid():
        return HttpResponse(content='invalid parameters', status=400)
    lat_upper, lat_lower, lon_upper, lon_lower =\
        calculate_bounds(latlon_form.cleaned_data['lat'], latlon_form.cleaned_data['lon'], DEFAULT_RADIUS)
    groups = Group.objects.filter(lat__lte=lat_upper, lat__gte=lat_lower, lon__lte=lon_upper, lon__gte=lon_lower)
    res = serializers.serialize('json', groups)
    return JsonResponse(res, safe=False)
    pass


@login_required
def get_businesses(request):
    if request.method != 'POST':
        raise Http404
    latlon_form = LatLonForm(request.POST)
    if not latlon_form.is_valid():
        return HttpResponse(content='invalid parameters', status=400)
    lat_upper, lat_lower, lon_upper, lon_lower =\
        calculate_bounds(latlon_form.cleaned_data['lat'], latlon_form.cleaned_data['lon'], DEFAULT_RADIUS)
    businesses = Business.objects.filter(lat__lte=lat_upper, lat__gte=lat_lower, lon__lte=lon_upper, lon__gte=lon_lower)
    res = serializers.serialize('json', businesses)
    return JsonResponse(res, safe=False)
    pass


@login_required
def create_group_with_latlon(request, lat, lon):
    group = Group(lat=float(lat), lon=float(lon))
    create_group_form = GroupForm(instance=group)
    return render(request, 'create_group.html', {'create_group_form': create_group_form})
    pass


@login_required
@transaction.atomic
def create_group(request):
    if request.method != 'POST':
        return render(request, 'create_group.html', {'create_group_form': GroupForm()})
    create_group_from = GroupForm(request.POST)
    if not create_group_from.is_valid():
        return render(request, 'create_group.html', {'create_group_form': create_group_from})
    try:
        create_group_from.save()
        pass
    except Exception as e:
        logger.error(e.message)
        pass
    return redirect('/')
    pass


@login_required
def profile(request, id):
    context = {}
    try:
        current_user = User.objects.get(id=id)
        profile = Profile.objects.get(user=current_user)
        if current_user != request.user:
            if current_user not in request.user.profile.follower.all():
                context['follow'] = 'follow'
            else:
                context['unfollow'] = 'unfollow'
        context['current_user'] = current_user
        context['profile'] = profile
        return render(request, 'profile.html', context)
    except Exception as e:
        logger.error(e.message)
        raise Http404
    pass


@login_required
def edit_profile(request):
    if request.method != 'POST':
        try:
            form = ProfileForm(instance=request.user.profile)
            context = {'form': form, 'id': request.user.id, 'current_user': request.user}
            return render(request, 'edit-profile.html', context)
        except Exception as e:
            logger.error(e.message)
            raise Http404

    # if method is POST, get form data to update the model
    form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

    if not form.is_valid():
        context = {'form': form, 'id': request.user.id}
        return render(request, 'edit-profile.html', context)

    try:
        form.save()
        current_user = User.objects.get(id=request.user.id)
        current_user.save()
        return redirect(reverse('profile', args=[request.user.id]))
    except Exception as e:
        logger.error(e.message)
        raise Http404


@login_required
def group_chat(request, group_id):
    if Group.objects.filter(id=group_id).exists():
        context = dict()
        group = Group.objects.get(id=group_id)
        context['group'] = group
        messages = Message.objects.filter(group=group)
        context['messages'] = messages
        context['current_user'] = request.user
        return render(request, 'chat.html', context)
        pass
    else:
        raise Http404
    pass


@login_required
def get_avatar(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_profile = Profile.objects.get(user=user)
        content_type = guess_type(user_profile.picture.name)
        return HttpResponse(user_profile.picture, content_type=content_type)
        pass
    except Exception as e:
        logger.error(e.message)
        raise Http404
    pass


@login_required
def relationship(request):
    context = {}
    try:
        context['current_user'] = request.user
        profiles = list()
        for user in request.user.profile.follower.all():
            profiles.append(user.profile)
            # print user.profile.first_name
            # print user.profile.id
            pass
        context['profiles'] = profiles
        return render(request, 'friends.html', context)
    except Exception as e:
        logger.error(e.message)
        # redirect to home page if object doesn't exist
        return redirect('/')
    pass


@login_required
@transaction.atomic
def edit_relationship(request, id):
    try:
        user = User.objects.get(id=id)
        if user not in request.user.profile.follower.all():
            request.user.profile.follower.add(user)
            return profile(request, id)
        else:
            request.user.profile.follower.remove(user)
            return profile(request, id)
    except Exception as e:
        logger.error(e.message)
        raise Http404
    pass


@login_required
def search(request):
    if request.method != 'POST':
        return render(request, 'search.html')
    search_form = SearchForm(request.POST)
    if search_form.is_valid():
        if search_form.cleaned_data['method'] == 'keyword':
            keyword = search_form.cleaned_data['keyword']
            if search_form.cleaned_data['type'] == 'group':
                groups = Group.objects.filter(name__icontains=keyword)
                res = serializers.serialize('json', groups)
                return JsonResponse(res, safe=False)
                pass
            elif search_form.cleaned_data['type'] == 'business':
                businesses = Business.objects.filter(name__icontains=keyword)
                res = serializers.serialize('json', businesses)
                return JsonResponse(res, safe=False)
                pass
            elif search_form.cleaned_data['type'] == 'user':
                users = User.objects.filter(username__icontains=keyword)
                for user in users:
                    user.password = None
                    pass
                res = serializers.serialize('json', users)
                return JsonResponse(res, safe=False)
                pass
            else:
                return HttpResponse(content='unknown search type: ' + search_form.cleaned_data['type'], status=400)
            pass
        elif search_form.cleaned_data['method'] == 'location':
            lat_upper, lat_lower, lon_upper, lon_lower =\
                calculate_bounds(search_form.cleaned_data['lat'],
                                 search_form.cleaned_data['lon'],
                                 search_form.cleaned_data['radius'])
            if search_form.cleaned_data['type'] == 'group':
                groups = Group.objects.filter(lat__lte=lat_upper, lat__gte=lat_lower,
                                              lon__lte=lon_upper, lon__gte=lon_lower)
                res = serializers.serialize('json', groups)
                return JsonResponse(res, safe=False)
                pass
            elif search_form.cleaned_data['type'] == 'business':
                businesses = Business.objects.filter(lat__lte=lat_upper, lat__gte=lat_lower,
                                                     lon__lte=lon_upper, lon__gte=lon_lower)
                res = serializers.serialize('json', businesses)
                return JsonResponse(res, safe=False)
                pass
            else:
                return HttpResponse(content='unknown search type: ' + search_form.cleaned_data['type'], status=400)
            pass
        else:
            return HttpResponse(content='unknown search method: ' + search_form.cleaned_data['method'], status=400)
        pass
    else:
        errors = list()
        for error in search_form.non_field_errors():
            errors.append(error)
            pass
        for field in search_form.visible_fields():
            if field.errors:
                for error in field.errors:
                    errors.append(field.label + ' error: ' + error)
                    pass
                pass
            pass
        return HttpResponse('\n'.join(errors), status=400)
    pass
