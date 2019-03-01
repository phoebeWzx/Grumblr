from django.contrib import auth
from django.contrib.auth import logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.http import Http404, HttpResponse
from grumblr.forms import *
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
import time

# Set current timestamp
current_milli_time = lambda: int(round(time.time() * 1000))


def register(request):
	context = {}
	if request.method == 'GET':
		form = RegistrationForm()
		context['form'] = form
		return render(request, 'grumblr/RegistrationPage.html',context)

	form = RegistrationForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'grumblr/RegistrationPage.html',context)

	username = form.cleaned_data['username']
	password = form.cleaned_data['password1']
	firstname = form.cleaned_data['firstname']
	lastname = form.cleaned_data['lastname']
	age = form.cleaned_data['age']
	bio = form.cleaned_data['bio']
	email = form.cleaned_data['email']

	new_user = User.objects.create_user(username = username, password = password,
					    first_name = firstname, last_name = lastname, email=email)
	new_user.profile.age = age
	new_user.profile.bio = bio

	new_user.is_active = False
	new_user.save()

	token = default_token_generator.make_token(new_user)
	email_body = """
	Welcome to Grumblr! Please click the link below to verify
	your email address and complete the registration of your account:
	http://%s%s
	"""% (request.get_host(), reverse('confirm', args=(new_user.username, token)))

	send_mail(subject="Verify your email address", message=email_body, from_email="zhuoxuew@andrew.cmu.edu",
		  recipient_list=[new_user.email], fail_silently=False)

	context['email'] = email
	return render(request, 'grumblr/email_confirm.html', context)


def register_confirm(request, username, token):
	try:
		cur_user = User.objects.get(username=username)
	except:
		raise Http404

	if not default_token_generator.check_token(cur_user, token):
		raise Http404

	cur_user.is_active = True
	cur_user.save()

	auth.login(request, cur_user)
	return redirect(reverse('home'))


def reset_password(request):
	context = {}
	if request.method == "GET":
		form = ResetPasswordForm()
		context['form'] = form
		return render(request, 'grumblr/ResetPage.html', context)

	form = ResetPasswordForm(request.POST)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'grumblr/ResetPage.html', context)

	try:
		cur_user = User.objects.get(email=form.cleaned_data['email'])
	except:
		Http404

	token = default_token_generator.make_token(cur_user)
	email_body = """
	Please click the link below to verify your email address
	and complete the password resetting of your account:
	http://%s%s
	""" % (request.get_host(), reverse('reset-confirm', args=(cur_user.username, token)))

	send_mail(subject="Verify your email address", message=email_body, from_email="zhuoxuew@andrew.cmu.edu",
		  recipient_list=[cur_user.email], fail_silently=False)
	return render(request, 'grumblr/email_confirm.html', context)


def reset_confirm(request, username, token):
	context = {}
	try:
		cur_user = User.objects.get(username=username)
	except:
		raise Http404

	if not default_token_generator.check_token(cur_user, token):
		raise Http404

	context['user'] = cur_user
	return redirect(reverse('password-confirm', args={username}))


def password_confirm(request, username):
	context = {}
	if request.method == 'GET':
		form = ResetForm()
		context['form'] = form
		return render(request, 'grumblr/Password_confirm.html', context)

	form = ResetForm(request.POST)
	context['form'] = form

	# Validate the form
	if not form.is_valid():
		return render(request, 'grumblr/Password_confirm.html', context)

	# Change the password of the user
	try:
		cur_user = User.objects.get(username=username)
		cur_user.set_password(form.cleaned_data['new_password'])
		cur_user.save()
	except:
		Http404
	# Log out
	logout(request)
	return redirect(reverse('home'))


@login_required
def global_stream(request):
	context = {}
	orderbyList = ['-date', '-time']
	all_posts = Post.objects.all().order_by(*orderbyList)
	post_form = PostForm()
	context['post_form'] = post_form
	context['posts'] = all_posts
	context['username'] = request.user
	context['timestamp'] = current_milli_time
	return render(request, 'grumblr/GlobalStream.html', context)

@login_required
def add_post(request):
	context = {}
	form = PostForm(request.POST)
	# Validate the form
	if not form.is_valid():
		orderbyList = ['-date', '-time']
		all_posts = Post.objects.all().order_by(*orderbyList)
		context['post_form'] = form
		context['posts'] = all_posts
		context['username'] = request.user
		context['timestamp'] = current_milli_time
		return render(request, 'grumblr/GlobalStream.html', context)

	post = form.cleaned_data['post']
	new_post = Post(person=request.user,text=post)
	new_post.save()
	orderbyList = ['-date', '-time']
	all_posts = Post.objects.all().order_by(*orderbyList)
	context['posts'] = all_posts
	context['timestamp'] = current_milli_time
	return render(request, 'posts.json', context, content_type='application/json')


@login_required
def add_comment(request, post_id):
	context={}
	form = CommentForm(request.POST)
	if not form.is_valid():
		orderbyList = ['-date', '-time']
		all_posts = Post.objects.all().order_by(*orderbyList)
		cur_user = request.user
		context['posts'] = all_posts
		context['username'] = cur_user
		return render(request, 'grumblr/GlobalStream.html', context)

	try:
		post = Post.objects.get(id = post_id)
	except ObjectDoesNotExist:
		return HttpResponse("The post did not exist")

	comment = form.cleaned_data['comment']
	new_comment = Comment(person=request.user, text=comment, post=post)
	new_comment.save()
	context['comment'] = new_comment
	return render(request, 'comment.json', context, content_type='application/json')


@login_required
def get_post(request):
	context = {}
	try:
		timestamp = float(request.GET['timestamp'])
	except:
		timestamp = 0.0
	posts = Post.get_changes(timestamp)
	context['posts'] = posts
	context['timestamp'] = current_milli_time()
	return render(request, 'posts.json', context, content_type='application/json')


@login_required
def get_comment(request, post_id):
	context = {}
	orderbyList = ['-date', '-time']
	post = Post.objects.get(id=post_id)
	comments=[]
	try:
		comments = Comment.objects.filter(post=post).order_by(*orderbyList)
	except:
		Http404
	context['comments'] = comments
	return render(request, 'comments.json', context, content_type='application/json')


@login_required
def profile(request, username):
	context = {}
	form = CommentForm()
	context['comment_form'] = form
	try:
		orderbyList = ['-date', '-time']
		cur_user = User.objects.get(username=username)
		user_posts = Post.objects.filter(person=cur_user).order_by(*orderbyList)
		context['posts'] = user_posts
		context['user'] = cur_user
		if check_follower(request, username):
			context['follow'] = True
		return render(request, 'grumblr/ProfilePage.html', context)
	except:
		return render(request, 'grumblr/ProfilePage.html', {'user': []})


@login_required()
def check_follower(request, username):
	try:
		cur_user = User.objects.get(username=request.user)
		followees = cur_user.profile.followees.all()
		followee = User.objects.get(username=username)

		if followee in followees:
			return True
		else:
			return False
	except:
		return False

@login_required
def update_profile(request, username):
	context = {}
	if request.method == 'GET':

		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
		context['user_form'] = user_form
		context['profile_form'] = profile_form

		return render(request, 'grumblr/EditProfile.html', context)

	user_form = UserForm(request.POST, instance=request.user)
	profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

	if not user_form.is_valid() or not profile_form.is_valid():
		context['user_form'] = user_form
		context['profile_form'] = profile_form
		return render(request, 'grumblr/EditProfile.html', context)

	user_form.save()
	profile_form.save()
	return redirect(reverse('profile', args={username}))


@login_required
def change_password(request, username):
	context = {}
	if request.method == 'GET':
		form = ChangePasswordForm()
		context['form'] = form
		return render(request, 'grumblr/Change_Password.html', context)

	form = ChangePasswordForm(request.POST)
	context['form'] = form

	# Validate the form
	if not form.is_valid():
		return render(request, 'grumblr/Change_Password.html', context)

	# Validate the old password
	oldpassword = form.cleaned_data['oldpassword']
	user = authenticate(username=username, password=oldpassword)
	if user is None:
		error = "Please input correct old password"
		context['error'] = error
		return render(request, 'grumblr/Change_Password.html', context)

	# Change the password of the user
	cur_user = request.user
	cur_user.set_password(form.cleaned_data['new_password'])
	cur_user.save()

	# Log out
	logout(request)
	return redirect(reverse('home'))

@login_required()
def follow(request, username):
	context = {}
	try:
		orderbyList = ['-date', '-time']
		follow_user = User.objects.get(username=username)
		context['posts'] = Post.objects.filter(person=follow_user).order_by(*orderbyList)
		context['user'] = follow_user
		cur_user = User.objects.get(username=request.user)
		cur_user.profile.followees.add(follow_user)
		cur_user.save()
		context['follow'] = True;
	except:
		Http404
	return render(request, 'grumblr/ProfilePage.html', context)

@login_required()
def unfollow(request, username):
	context = {}
	try:
		orderbyList = ['-date', '-time']
		follow_user = User.objects.get(username=username)
		context['posts'] = Post.objects.filter(person=follow_user).order_by(*orderbyList)
		context['user'] = follow_user
		cur_user = User.objects.get(username=request.user)
		cur_user.profile.followees.remove(follow_user)
		cur_user.save()
	except:
		Http404
	return render(request, 'grumblr/ProfilePage.html', context)

@login_required()
def follow_stream(request):
	context = {}
	try:
		orderbyList = ['-date', '-time']
		cur_user = User.objects.get(username=request.user)
		followees = cur_user.profile.followees.all()
		posts = Post.objects.filter(person__in=followees).order_by(*orderbyList)
		context['posts'] = posts
		context['user'] = cur_user
	except Exception as e:
		Http404
	return render(request, 'grumblr/Follower_Stream.html', context)

