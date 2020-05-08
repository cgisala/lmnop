from django.shortcuts import render, redirect

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

''' View for generic profile page '''
def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)

    editable = False

    if user_pk == request.user.pk:
        editable = True

    usernotes = Note.objects.filter(user=user.pk).order_by('-posted_date')
    return render(request, 'lmn/users/user_profile.html', { 'user_profile': user , 'notes': usernotes , 'editable': editable })

''' View for Modifying logged in user's profile info '''
@login_required
def my_user_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, 
                                        request.FILES, 
                                        instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your profile was successfully updated!')
            return redirect('/user/profile/' + str(request.user.id))
        else:
            messages.error(request, f'Please correct the error below.')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'lmn/users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('lmn:homepage')

        else :
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', { 'form': form , 'message': message } )

    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', { 'form': form } )
