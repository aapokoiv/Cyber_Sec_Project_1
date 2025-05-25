from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account


@login_required
def transferView(request):
	
	if request.method == 'GET':		# To fix replace all GET instances in this block and in index.html line 26 with POST and uncomment the csrf token on line 27 in the index.html
		to = User.objects.get(username=request.GET.get('to'))
		amount = int(request.GET.get('amount'))

		request.user.account.balance -= amount
		to.account.balance += amount

		request.user.account.save()
		to.account.save()
	
	return redirect('/')

@login_required
def viewAccount(request, username):
	#if request.user.username != username:
	#	return HttpResponse("Unauthorized")
	user = User.objects.get(username=username)
	return HttpResponse(f"Balance of {username}: {user.account.balance}")

@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})
