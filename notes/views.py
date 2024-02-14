from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Note
from .forms import NoteForm

# Flaw 1: CSRF token is missing.
# csrf_exempt-decorator disables the CSRF protection for the view.
# Fix: Remove the csrf_exempt decorator to allow Django to use CSRF protection.
@csrf_exempt
@login_required
def home(request):
    notes = Note.objects.filter(user=request.user)
    form = NoteForm()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')

    return render(request, 'notes/home.html', {'notes': notes, 'form': form})


@login_required
def detail(request, pk):
    # Flaw 2: Broken Access Control
    # User can access anyones note by changing the URL.
    # Fix: Change the query to filter the notes by the user.
    # note = get_object_or_404(Note, id=pk, user=request.user)
    note = get_object_or_404(Note, id=pk)
    return render(request, 'notes/detail.html', {'note': note})


@login_required
def delete(request, pk, title):
    # Flaw 5: SQL Injection
    # User input is directly used in the SQL query which can lead to SQL Injection.
    # Fix: Use Django's ORM to delete the note.
    # note = get_object_or_404(Note, id=pk, user=request.user)
    # note.delete()
    # return redirect('home')
    if request.user != Note.objects.get(id=pk).user:
        return redirect('home')
    query = f"DELETE FROM notes_note WHERE id = {pk} AND title = '{title}'"
    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
