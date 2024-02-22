#this module handles *routes* i.e. urls for webpage. homepage, or any other pages I create(login page will go in auth.py
#Blueprint member allows for organizing the application into smaller re-usable parts
#blueprints need to be registered, see __init__.py

from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Flashcard
from .models import Deck
from . import db
import json
from datetime import datetime



#this file is a blueprint of our application, it has a bunch of *routes* ie url's
views = Blueprint("views", __name__)     #doesn't have to be name of file but seems to be easier. 

fetched_flash = Flashcard()
@views.route('/', methods = ["GET", "POST"])       #this is homepage route(url)
@login_required
def home():
    if request.method == "POST":
        deck_title = request.form.get("deck_title")
        flash_title = request.form.get("flash_title")
        flasha = request.form.get("flasha")
        flashb = request.form.get("flashb")

        
        if len(deck_title) < 1:
            flash("Deck must have a title!", category = "error")
        if len(flash_title) < 1:
            flash("Flashcard must have a title!", category = "error")
        if len(flasha) < 1:
            flash("Side A must be populated!", category = "error")
        if len(flashb) < 1:
            flash("Side B must be populated!", category = "error")
        else:
            new_deck = Deck(title = deck_title, user_id = current_user.id )
            new_flash = Flashcard(title = flash_title, data = flasha, data2 = flashb, deck_title = new_deck.title, user_id = current_user.id) 
            
            if not Deck.query.get(deck_title):  #we don't want to add a new deck if one of that title already exists. 
                db.session.add(new_deck)
            db.session.add(new_flash)
            db.session.commit()

            return redirect("/")                #This is to facilitate(I hope) post-redirect-get design to stop accidental duplicates upon browser refresh

    f_title, f_data, f_data2, f_deck_title = "", "", "", ""        #This is to allow for placeholder text or the fetched flash card text
    if fetched_flash.title:
        f_title = fetched_flash.title
        f_data = fetched_flash.data
        f_data2 = fetched_flash.data2
        f_deck_title = fetched_flash.deck_title

    return render_template("home.html", user = current_user, flash_title = f_title, flasha = f_data, flashb = f_data2, deck_title = f_deck_title)

#
# deletes deck and all flashcards.  Will want to change this as to allow a flash card toe xist in multiple decks. 
#
@views.route("delete-deck", methods = ["POST", "GET"])
def delete_deck():
    deck = json.loads(request.data)
    deckId = deck["deckId"]

    deck = Deck.query.get(deckId)
    if deck:
        if deck.user_id == current_user.id:
            for flashcard in deck.flashcards:
                db.session.delete(flashcard)
            db.session.delete(deck)
            db.session.commit()
    
    return jsonify({})

#
# deletes a single flash card. 
#
@views.route("/delete-flash", methods = ["POST", "GET"])
def delete_note():
    flashcard = json.loads(request.data)
    flashId = flashcard["flashId"]
    flashcard = Flashcard.query.get(flashId)
    #print(note.user.email)                     demonstrates how backref works(see models.py and db.relationship(...))
    if flashcard:
        if flashcard.deck.user_id == current_user.id:
            db.session.delete(flashcard)
            db.session.commit()

        fetched_flash.title = None           #when we delete a note we don't want to reload the current flash card with previous
    return jsonify({})

@views.route("/fetch-deck", methods = ["POST", "GET"])
def fetch_deck():
    showF = json.loads(request.data)
    # showFl = showF["showFlash"]
    print(showF)
    return jsonify({})


@views.route("/fetch-flash", methods = ["POST", "GET"])
def fetch_flash():
    print('hit')
    flashcard = json.loads(request.data)
    flashId = flashcard["flashId"]
    flashcard = Flashcard.query.get(flashId)
    #deck = Deck.query.get(note.user_deck_id)
    # note = json.loads(request.data)
    # noteId = note["noteId"]
    # note = Note.query.get(noteId)
    
    
    # note.title = "itsss"
    # db.session.commit()

    # print(note.title)
    # print(request.data)
    
    # return render_template("home.html", user = current_user, test = "testfetch") 
    
    # print(jsonify(note.data))
    #return render_template("home.html", user = current_user, test = note.data)  
    fetched_flash.title = flashcard.title
    fetched_flash.data = flashcard.data
    fetched_flash.data2 = flashcard.data2
    fetched_flash.deck_title = flashcard.deck_title
    
    return jsonify({})

@views.route('/test', methods=['GET', 'POST'])
def testfn():
    # GET request
    if request.method == 'GET':
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200
