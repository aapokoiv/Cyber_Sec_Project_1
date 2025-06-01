from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import transaction
from .models import Account
from django.conf import settings
import base64
import re
import sqlite3

xor_key = settings.SECRET_KEY.encode()[:32]

@login_required
def transferView(request):

	# To fix replace all GET instances in this block and in index.html line 26 with POST 
	# Also uncomment the csrf token on line 27 in the index.html
	if request.method == 'GET':		
		to = User.objects.get(username=request.GET.get('to'))
		amount = int(request.GET.get('amount'))

		request.user.account.balance -= amount
		to.account.balance += amount

		request.user.account.save()
		to.account.save()
	
	return redirect('/')

@login_required
def viewAccount(request, username):
	# Uncomment these lines
	# if request.user.username != username:
	# 	return HttpResponse("Unauthorized")

	user = User.objects.get(username=username)
	card = user.account.card
	
	if not re.match("^[0-9 ]+$", card) and card != "None":
		card = decrypt(card, xor_key)
	return HttpResponse(f"Balance of {username}: {user.account.balance}\nCard: {card}")
	

@login_required
def addCard(request):
	if request.method == 'POST':
		number = request.POST.get('number')

		# Comment out this line
		request.user.account.card = number

		# And uncomment this part
		# encrypted_number = encrypt(number, xor_key)
		# request.user.account.card = encrypted_number

		request.user.account.save()
	return redirect("/")

def encrypt(text, key):
	return base64.urlsafe_b64encode(
		bytes([b ^ key[i % len(key)] for i, b in enumerate(text.encode())])
	).decode()

def decrypt(text, key):
	data = base64.urlsafe_b64decode(text.encode())
	return ''.join(chr(b ^ key[i % len(key)]) for i, b in enumerate(data))


@login_required
def userSearchView(request):
	username = request.GET.get('username')
	actual_user = request.user.username
	conn = sqlite3.connect('src/db.sqlite3')
	cursor = conn.cursor()

	# Comment out this part
	query = f"""
        SELECT auth_user.username, pages_account.balance
        FROM auth_user
        JOIN pages_account ON auth_user.id = pages_account.user_id
        WHERE auth_user.username LIKE '%{username}%'
		"""
	cursor.execute(query)
	
	# And uncomment this part
	# query = f"""
        # SELECT auth_user.username, pages_account.balance
        # FROM auth_user
        # JOIN pages_account ON auth_user.id = pages_account.user_id
        # WHERE auth_user.username LIKE ?
		# """
	# name = f"%{username}%"
	# cursor.execute(query, (name,))
	
	
	rows = cursor.fetchall()
	conn.close()
	if len(rows) < 1:
		return HttpResponse("User not found")

	if actual_user not in dict(rows):
		return HttpResponse(f"Name: {rows[0][0]}")

	results = [{'username': row[0], 'balance': row[1]} for row in rows]
	return HttpResponse(results)

@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})
