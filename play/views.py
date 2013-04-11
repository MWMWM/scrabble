#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools, urllib, re
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from helper.models import Word, User
from scrabble.views import RenderWithInf

def Main(request):
    return RenderWithInf('play/main.html', request)


