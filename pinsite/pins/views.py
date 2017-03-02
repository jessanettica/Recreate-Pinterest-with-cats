from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import render_to_response

from pins.forms import *
from pins.models import *

import json
import datetime


def index(request):
    """Set up and display the Pins."""
    form = CreatePinForm()
    variables = RequestContext(request, {'form': form})
    return render(request, 'pins/main_page.html', variables)


def logout_page(request):
    """Display the logout page."""
    logout(request)
    return HttpResponseRedirect('/pins')


def register_page(request):
    """Display the register page."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password']
                )
            authenticated_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                )
            login(request, authenticated_user)
            return HttpResponseRedirect('/pins/')
    form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)


def myconverter(obj):
    """Return a string representation of non json serializable datetime object."""
    if isinstance(obj, datetime.datetime):
        return obj.__str__()


def json_response(resp):
    """Return an HTTP response."""
    return HttpResponse(json.dumps(resp, default=myconverter), content_type="application/json")


def get_all_pins(request):
    """Return http response with all pins to display on initial page load."""
    try:
        pins = Pin.objects.all()
        dictionaries = [ obj.as_dict() for obj in pins ]
    except:
        return json_response({
            'status': 'fail'
        })
    return json_response({
        'status': 'ok',
        'data': dictionaries
    })


def get_more_pins(request):
    """Return http response with 24 pins for infinite scroll.

    The pins are the first 24 that have not been used since all of the pins were
    displayed. If all the pins have been displayed, then 20 are displayed and the
    is_used_field is updated so that they are not used again untill all the pins
    have been used once more.
    """
    try:
        pins = Pin.objects.filter(is_used=False)[:24]
        if pins.exists():
            dictionaries = [ obj.as_dict() for obj in pins ]
            # queryset cannot be updated with `update()` after being sliced
            for pin in pins:
                pin.is_used = True
                pin.save()
        else:
            # all pins have been used, reset the is_used field
            Pin.objects.all().update(is_used=False)
            pins = Pin.objects.all()[:24]
            dictionaries = [ obj.as_dict() for obj in pins ]
            for pin in pins:
                pin.is_used = True
                pin.save()
    except:
        return json_response({
            'status': 'fail'
        })
    return json_response({
        'status': 'ok',
        'data': dictionaries
    })


def create_new_pin(request):
    """Return http response with new pin data.

    A new Pin is created using data from the form.
    """
    if request.method == 'POST':
        pinner = request.user
        if not pinner.full_name:
            pinner.full_name = request.POST.get('full_name')
            pinner.save()
        board_name = request.POST.get('board_name')

        try:
            board, created = Board.objects.get_or_create(
                name=board_name
            )
        except Exception:
            return json_response({
                'status': 'fail'
            })

        img_url = request.POST.get('img_url')
        description = request.POST.get('description')
        title = request.POST.get('title')

        try:
            pin, created = Pin.objects.get_or_create(
                pinner=pinner,
                title=title,
                buyable_product=False,
                description=description,
                created_at=datetime.datetime.now(),
                img_url=img_url,
                img_height=236,
                like_count=0,
                repin_count=0,
                # new pin will be immediately appended to the pin feed
                is_used=True
            )
        except Exception:
            return json_response({
                'status': 'fail'
            })

        pin.boards.add(board)
        dictionaries = [pin.as_dict()]

    return json_response({
        'status': 'ok',
        'data': dictionaries
    })
