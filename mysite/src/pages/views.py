from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import transaction
from .models import Account, Card
import sqlite3


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
	# if request.user.username != username:
	#	 return HttpResponse("Unauthorized")
	user = User.objects.get(username=username)
	return HttpResponse(f"Balance of {username}: {user.account.balance}")

@login_required
def addCard(request):
	if request.method == 'POST':
		number = request.POST.get('number')
		user = request.user
		Card.objects.create(user=user, number=number)


@login_required
def userSearchView(request):
	username = request.GET.get('username')
	actual_user = request.user.username
	conn = sqlite3.connect('src/db.sqlite3')
	cursor = conn.cursor()
	query = f"""
        SELECT auth_user.username, pages_account.balance
        FROM auth_user
        JOIN pages_account ON auth_user.id = pages_account.user_id
        WHERE auth_user.username LIKE '%{username}%'
		"""
	cursor.execute(query)
	rows = cursor.fetchall()
	conn.close()

	if actual_user not in dict(rows):
		return HttpResponse(f"Name: {rows[0][0]}")

	results = [{'username': row[0], 'balance': row[1]} for row in rows]
	return HttpResponse(results)

@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})
