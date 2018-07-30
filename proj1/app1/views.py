from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.db.models import Q
from app1 import models
from datetime import datetime,date
from reportlab.pdfgen import canvas
from django.http import HttpResponse
@csrf_exempt
def default(request):
		if 'username' in request.session:
			if request.session['User_type'] == "Librarian":
				return redirect('/librarian_dash')
			else:
				return redirect('/student_dash')
		else:
			return redirect('/home')
@csrf_exempt
def register(request):
	if request.method=='POST':
		Name = request.POST['Name']
		Username = request.POST['Username']
		Password = request.POST['Password']
		Contact = request.POST['Contact']
		User_type = request.POST['Type']
		context = {}
		if models.User.objects.filter(username=Username).exists():
			message = "Username already exists"
			context['message'] = message
			response = render(request,"register.html",context)
		else:
			obj = models.User(
				name = Name,
				username = Username,
				password = Password,
				contact = Contact,
				user_type = User_type,
			)
			obj.save()
			response = HttpResponseRedirect('/login')
	else:
		response = render(request,'register.html',{})
	return response
@csrf_exempt
def login(request):
	if 'username' in request.session:
		if request.session['User_type'] == "Librarian":
			return redirect('/librarian_dash')
		else:
			return redirect('/student_dash')
	else:
		if request.method == "POST":
			Username = request.POST['Username']
			Password = request.POST['Password']
			context = {}
			if models.User.objects.filter(username = Username,password = Password):
				obj_user = models.User.objects.get(username = Username,password = Password)
				request.session['username'] = Username
				request.session['User_type'] = obj_user.user_type
				if obj_user.user_type == "Librarian":
					response = HttpResponseRedirect('/librarian_dash')
				else:
					response = HttpResponseRedirect('/student_dash')
			else:
				context['message'] = "Invalid Credentials"
				response = render(request,"login.html",context)
		else:
			response = render(request,'login.html',{})
		return response
@csrf_exempt
def sort_date(temp):
	return temp.return_date
def stud_dash(request):
	if 'User_type' in request.session:
		if request.session['User_type'] == "Student":
			context = {}
			obj_user = models.User.objects.get(username = request.session['username'])
			context['username'] = obj_user.username
			context['name'] = obj_user.name
			context['contact'] = obj_user.contact
			context['user_type'] = obj_user.user_type
			context['message'] = "I'm a Student"
			context['message1'] = "Student"
			context['books'] = list(models.books.objects.all())
			context['rbooks'] = list(models.requested.objects.filter(requestedBy = request.session['username']))
			context['rbooks'].sort(key = sort_date)
			response = render(request,'mes.html',context)
			return response
	else:
		return redirect('/login')
@csrf_exempt
def lib_dash(request):
	if 'User_type' in request.session:
		if request.session['User_type']=="Librarian":
			context = {}
			obj_user = models.User.objects.get(username = request.session['username'])
			context['username'] = obj_user.username
			context['name'] = obj_user.name
			context['contact'] = obj_user.contact
			context['user_type'] = obj_user.user_type
			context['message1'] = "Librarian"
			context['message'] = "I'm a Librarian"
			context['books'] = list(models.books.objects.filter(no_of_copies__gt = 0))
			context['rbooks'] = list(models.requested.objects.all())
			context['rbooks'].sort(key = sort_date)
			context['retbooks'] = list(models.requested.objects.filter(return_date = date.today(),status = 'To be Returned'))
			for i in context['retbooks']:
				print(i.return_date)
			response = render(request,'mes.html',context)
			return response
	else:
		return redirect('/login')
@csrf_exempt
def logout(request):
	if 'username' in request.session:
		del request.session['username']
		del request.session['User_type']
	return redirect('/login')
@csrf_exempt
def book_details(request):
	temp_id = request.GET['book_id']
	obj_user = models.books.objects.get(id = temp_id)
	context = {}
	context['summary'] = obj_user.summary
	context['name'] = obj_user.name
	context['author'] = obj_user.author
	context['no_of_copies'] = obj_user.no_of_copies
	context['subject'] = obj_user.subject
	context['rating'] = obj_user.star_rating
	response = render(request,'summary.html',context)
	return response
@csrf_exempt
def add_books(request):
	if request.session['User_type']=="Student":
		return HttpResponseRedirect('/home')
	if request.method=='POST':
		if request.POST['Name']!="":
			Name = request.POST['Name']
			Author = request.POST['Author']
			no_of_copies = request.POST['no_of_copies']
			subject = request.POST['subject']
			summary = request.POST['summary']
			context = {}
			if models.books.objects.filter(name=Name,author = Author,subject = subject).exists():
				obj_user = models.books.objects.get(name = Name,author = Author,subject = subject)
				tot_book = int(obj_user.no_of_copies)
				tot_book = tot_book + int(no_of_copies)
				models.books.objects.get(name = Name,author = Author,subject = subject).delete()
				obj_user.no_of_copies = str(tot_book)
				obj = models.books(
				name = obj_user.name,
				author = obj_user.author,
				no_of_copies = obj_user.no_of_copies,
				subject = obj_user.subject,
				summary = obj_user.summary,
				)
				obj.save()
			else:
				obj = models.books(
				name = Name,
				author = Author,
				no_of_copies = no_of_copies,
				subject = subject,
				summary = summary,
				)
				obj.save()
			response = HttpResponseRedirect('/librarian_dash')
		else:
			context = {}
			context['message'] = "Invalid entry"
			response = render(request,"add_books.html",context)
	else:
		response = render(request,'add_books.html',{})
	return response
@csrf_exempt
def profile(request):
	user = request.GET['username']
	context = {}
	obj_user = models.User.objects.get(username = user)
	context['username'] = obj_user.username
	context['name'] = obj_user.name
	context['contact'] = obj_user.contact
	context['user_type'] = obj_user.user_type
	response = render(request,'profile.html',context)
	return response
@csrf_exempt
def home(request):
	if 'username' in request.session:
		if request.session['User_type'] == "Librarian":
			return redirect('/librarian_dash')
		else:
			return redirect('/student_dash')
	if request.method=='GET':
		response = render(request,'home.html',{})
		return response
def search(request):
	if request.POST['searchText']!="":
		Name = request.POST['searchText']
		context = {}
		if models.books.objects.filter(Q(name__contains='Name')).exists():
			context['book'] = list(models.books.objects.filter(Q(name__contains='Name')))
		else:
			context['error'] = "Enter a valid search"
		response = render(request,'search.html',context)
		return response
@csrf_exempt
def request_books(request):
	if request.GET['Name']!="":
		Name = request.GET['Name']
		if models.books.objects.filter(name = Name).exists():
			obj_books = models.books.objects.get(name = Name)
			if int(obj_books.no_of_copies) < 1:
				context = {}
				context['message'] = "Invalid Entry"
				return render(request,'request_books.html',context)
			if models.requested.objects.filter(Q(requestedBy = request.session['username']),Q(status = 'Booked') | Q(status = 'To be Returned')).exists():
				context = {}
				context['message'] = "Invalid Entry"
				return render(request,'request_books.html',context)
			models.books.objects.get(name = Name).delete()
			obj_books.no_of_copies = str(int(obj_books.no_of_copies) - 1)
			obj_new_book = models.books(
			name = obj_books.name,
			author = obj_books.author,
			no_of_copies = str(obj_books.no_of_copies),
			summary = obj_books.summary,
			subject = obj_books.subject,
			star_rating = obj_books.star_rating,
			)
			obj_new_book.save()
			obj = models.requested(
			name = Name,
			requestedBy = request.session['username'],
			status = "Booked",
			)
			obj.save()
			return HttpResponseRedirect('/student_dash')
		else:
			context = {}
			context['message'] = "Invalid Entry"
			return render(request,'request_books.html',context)
	else:
		context = {}
		context['message'] = "Invalid Entry"
		return render(request,'request_books.html',context)
@csrf_exempt
def currentBookings(request):
	obj_request = models.requested.objects.get(id = request.GET['request_id'])
	if(obj_request.status == "Booked"):
		obj_request.status = "To be Returned"
		obj_request.save(update_fields = ['status'])
	else:
		obj_request.status = "Returned"
		obj_books = models.books.objects.get(name = obj_request.name)
		obj_books.no_of_copies = str(int(obj_books.no_of_copies) + 1)
		obj_books.save(update_fields = ['no_of_copies'])
		obj_request.save(update_fields = ['status'])
	return HttpResponseRedirect('/home')
def pdf_generator(request):
	obj_request = models.requested.objects.get(id = request.GET['request_id'])
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
	d0 = datetime.today().date() - obj_request.return_date
	if(d0.days > 0):
		fine = str(int(d0.days)*10)
	else:
		fine = str(0)
	str1 = str(obj_request.requestedBy) + " have returned book named " + str(obj_request.name) + " on " + str(date.today()) + " with fine of "+ fine + " Rupees"
	p = canvas.Canvas(response)
	p.drawString(100, 800, str1) #PDF generator
	p.showPage()
	p.save()
	return response
