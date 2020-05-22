from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.db.models import Count


@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST' :

        form = NewNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.save()
            return redirect('lmn:note_detail', note_pk=note.pk)

    else :
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html' , { 'form': form , 'show': show })

@login_required
def edit_note(request, note_pk):

    note = get_object_or_404(Note, pk=note_pk)
    
    if request.method == 'POST':

        form = NewNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.info(request, 'Note updated')
        else:
            messages.error(request, form.errors)

        return redirect('lmn:note_detail', note_pk=note.pk)

    else:

        form = NewNoteForm(instance = note)

    return render(request, 'lmn/notes/edit_note.html', { 'form': form, 'note': note })

@login_required
def delete_note(request, note_pk):

    note = get_object_or_404(Note, pk=note_pk)
    note.delete()
    return redirect('lmn:my_user_profile')


def latest_notes(request):
    notes = Note.objects.all().order_by('-posted_date')
    return render(request, 'lmn/notes/note_list.html', { 'notes': notes })


def notes_for_show(request, show_pk):   # pk = show pk

    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
    show = Show.objects.get(pk=show_pk)  
    return render(request, 'lmn/notes/note_list.html', { 'show': show, 'notes': notes } )


def note_detail(request, note_pk, *args, **kwargs):
    note = get_object_or_404(Note, pk=note_pk)
    user = kwargs.get('pk')

    editable = False

    if note.user.pk == request.user.pk:
        editable = True

    return render(request, 'lmn/notes/note_detail.html' , { 'note': note, 'editable': editable })


def shows_most_notes(request):
    # Shows with most notes = most popular show PK in the notes table 
    # Get the IDs of the three most popular shows
    show_id_and_counts = Note.objects    \
        .values('show_id')          \
        .annotate(Count('show'))    \
        .order_by('-show__count')   \
        [:3]      

    # Fetch the associated Show objects 

    def get_show_for_id(id_and_count):
        show = Show.objects.get(pk=id_and_count['show_id'])
        return (show, id_and_count)

    popular_shows_and_counts = list(map(get_show_for_id, show_id_and_counts))
    
    return render(request, 'lmn/notes/shows_most_notes.html', {'popular_shows': popular_shows_and_counts })