from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import threading, queue
import concurrent.futures

import storyitem


from batoto import Batoto

app = Flask(__name__)
#Cleartext pw as this server is not for production
app.secret_key = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    comicsInLibrary = db.Column(db.Text)

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.comicsInLibrary = None

@app.route("/")
def index():
    return redirect(url_for("login"))
    #return render_template("index.html")

@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        #If we get a request with both name and password fields filled
        if request.form["nm"] is not "" and request.form["pw"] is not "":
            session.permanent = True
            user = request.form["nm"]
            password = request.form["pw"]
            
            #Query db by name
            foundUser = users.query.filter_by(name=user).first()

            if foundUser is not None:
                #Log in if password matches user's name
                if foundUser.password == password:
                    #Add user details to session
                    session["user"] = user
                    session["password"] = password

                    return redirect(url_for("library"))

                #Return to login screen if password does not match
                elif foundUser.name == user:
                    flash(f"User with name: {user} already exists! Check your password")

                    return render_template("login.html")

                #Add a password to the user if it somehow doesn't have one
                else:
                    usr = users(user, password)
                    db.session.add(usr)
                    db.session.commit()
                    #print(f"Created a user with name: {user} and password: {password}")

                    #Add user details to session
                    session["user"] = user
                    session["password"] = password

                    return redirect(url_for("library"))
            else:
                #Create a user with the given name and password
                usr = users(user, password)
                db.session.add(usr)
                db.session.commit()
                #print(f"Created a user with name: {user} and password: {password}")

                #Add user details to session
                session["user"] = user
                session["password"] = password
                
                return redirect(url_for("library"))

        #Stay on the login page if name and password fields aren't filled    
        else:
            return render_template("login.html")

    else:
        #If the user's details are already in the browser session
        #go straight to the library
        if "user" in session:
            return redirect(url_for("library"))

        return render_template("login.html")

@app.route("/logout/")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")

    #Clear session details so the user can sign in again
    session.pop("user", None)
    session.pop("password", None)
    
    return redirect(url_for("login"))

@app.route("/profile/")
def profile():
    return render_template("profile.html")

@app.route("/library/")
def library():
    if "user" in session:
        #Query database by user name
        user = session["user"]
        dbUser = users.query.filter_by(name=user).first()

        #If we're given a url, add it to the user's details in the database
        if request.args.get("storyURL"):
            storyURL = str(request.args.get("storyURL"))

            #Add the url to the user's details if it doesn't already exist
            if dbUser.comicsInLibrary is not None:
                if storyURL in dbUser.comicsInLibrary:
                    pass
                else:
                    #Convert the library string to a nested list we can modify
                    comicsInLibrary = storyitem.StringToNestedList(dbUser.comicsInLibrary)
                    comic = [storyURL, 0, 0]
                    comicsInLibrary.append(comic)
                    comicsInLibrary = storyitem.NestedListToString(comicsInLibrary)

                    dbUser.comicsInLibrary = comicsInLibrary
                    db.session.commit()
            else:
                #The user doesn't have an entry for comicsInLibrary so we create it
                comic = [[storyURL, 0, 0]]
                comicsInLibrary = storyitem.NestedListToString(comic)

                dbUser.comicsInLibrary = comicsInLibrary
                db.session.commit()

        #Was used for testing, unnecessary now
        """comicsInLibrary = storyitem.StringToNestedList(dbUser.comicsInLibrary)
        if comicsInLibrary is not None:
            for comic in comicsInLibrary:
                #flash(f"{comic[0]}, {comic[1]}, {comic[2]}")
                pass"""
                
        #Display all the comics in library from the user's entry in the database
        storyItemList = []
        comicsInLibrary = storyitem.StringToNestedList(dbUser.comicsInLibrary)

        if comicsInLibrary is not None:
            #Multithread the scraping of comics
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(getattr(storyitem.ReturnSourceClass(comicsInLibrary[i][0]), 'GetStoryDetails'), comicsInLibrary[i][0])                  
                    for i in range(0,len(comicsInLibrary))]
                for f in futures:
                    storyItemList.append(f.result())

    else:
        flash("Log in or make an account before accessing your library!")
        return redirect(url_for("login"))
        
    return render_template("library.html", storyItemList=storyItemList)


"""def ReturnDetails(url):
    details = getattr(storyitem.ReturnSourceClass(url), 'GetStoryDetails')
    return details(url)"""


@app.route("/search/")
def search():
    #Change this so we search using the sources listed in the user's settings
    query = request.args.get("q")
    names, links, imageLinks = Batoto.Search(query)

    storyItemList = []

    #Multithread the searching of comic details
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(getattr(storyitem.ReturnSourceClass(links[i]), 'GetStoryDetails'), links[i])                  
            for i in range(0,len(links)-1)]
        for f in futures:
            storyItemList.append(f.result())

    return render_template("search.html", searchResult=query, names=names, links=links, imageLinks=imageLinks, storyItemList=storyItemList)


@app.route("/comicinfo/")
def comicinfo():
    #Show more info about the selected comic
    storyURL = str(request.args.get("returnItem"))
    detailsItem = getattr(storyitem.ReturnSourceClass(storyURL), 'GetStoryDetails')
    detailsItem = detailsItem(storyURL)

    return render_template("comicinfo.html", storyItem=detailsItem)


@app.route("/read/")
def read():
    storyURL = str(request.args.get("storyURL"))
    #source = storyitem.ReturnSourceCl(storyURL)
    chapterNumber = request.args.get("chapter")
    
    if "user" in session:
        #If the user is logged in, check if the comic is in their Library
        #If so, update the most recently read chapter number so it is synced with the cloud
        user = session["user"]
        dbUser = users.query.filter_by(name=user).first()

        if dbUser.comicsInLibrary is not None:
            if storyURL in dbUser.comicsInLibrary:
                comicsInLibrary = storyitem.StringToNestedList(dbUser.comicsInLibrary)
                for comic in comicsInLibrary:
                    if comic[0] == storyURL:
                        if str(chapterNumber) == "redirectfromlibrary":
                            chapterNumber = int(comic[1])
                        elif int(chapterNumber) > int(comic[1]):
                            comic[1] = chapterNumber

                dbUser.comicsInLibrary = storyitem.NestedListToString(comicsInLibrary)
                db.session.commit()

    #Get the details of each comic
    storyItem = getattr(storyitem.ReturnSourceClass(storyURL), 'GetStoryDetails')
    storyItem = storyItem(storyURL)
    
    #Get the images of the chapter
    chapterImageLinks = getattr(storyitem.ReturnSourceClass(storyItem.chapterListLinks[int(chapterNumber)]), 'GetChapterImages')
    chapterImageLinks = chapterImageLinks(storyItem.chapterListLinks[int(chapterNumber)])
    
    #Batoto.GetChapterImages(storyItem.chapterListLinks[int(chapterNumber)])
    #placeholder image list uncomment line above ^^
    #chapterImageLinks = ['https://xcdn-223.bato.to/00004/images/fd/0e/fd0e81add4fc0e42d47b517e7db1badd7192f348_230577_870_1259.jpg?acc=EIl07tYBl8GA5aRn8XtJCQ&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/0b/35/0b353bd4dc582b6bebb9966f1b3f4c46f7b2960f_254007_870_1261.jpg?acc=JcaCWO-yira4d6Da1QibFQ&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/db/6e/db6e56dd87745783c0d2d9757bdff82c3cd8d974_256507_870_1254.jpg?acc=uMNceXIhvu-hPRB94gWsfQ&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/3c/12/3c12a235291a512fb9b0408c7d85dfb76b726cf4_253697_870_1247.jpg?acc=5qUkQZGmnBw9o_buGqi_3A&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/be/1c/be1c9453207e37a0a0cfecaf0ed8cd1b47530c05_308695_870_1257.jpg?acc=WOXLrat4tmaeA3xxihAZRw&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/97/9b/979b49c604ce4a10f655db187c75be75194dbfc1_243873_870_1256.jpg?acc=PSexUpsdhAFsDPgSTA__AQ&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/50/d1/50d1055b43e79de3f269dffc03a5507b9b0e17da_246134_870_1258.jpg?acc=dEVjZX587rYTRlV7M4zTFg&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/0a/47/0a4775fb44ccea41fd1287f8799ad372f49b82d9_242485_870_1248.jpg?acc=pV-Q5wuFx5V95cmGvlTggg&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/b7/20/b7207c1516116cd5c35944388b8a70f7edca9c5d_217697_870_1285.jpg?acc=re9jySbgoRJIPqTpA36MIA&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/87/a9/87a93919b8f08671b764ad314b3ce9737cbf1956_264001_870_1256.jpg?acc=j2iGkcfvuE7FvEmGYD-p-A&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/b3/c9/b3c963320e29dd5d3bb947bf1f7672dcb616ff8e_267345_870_1305.jpg?acc=cy80DbHj7p_SX6YTxhMJcg&exp=1633054429', 'https://xcdn-223.bato.to/00004/images/ed/b6/edb6202143e188766c500fb9730aaa68e19e1e89_245856_870_1266.jpg?acc=ToCH95U3aFPQRwcVeZMJvw&exp=1633054429']
    #print(chapterImageLinks)

    return render_template("read.html", storyItem=storyItem, chapterImageLinks=chapterImageLinks, chapterNumber=int(chapterNumber))

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
        
    else:
        return redirect(url_for("login"))

@app.route("/viewusers/")
def viewusers():
    return render_template("viewusers.html", values=users.query.all())


@app.route("/offline.html")
def offline():
    return app.send_static_file("offline.html")

@app.route("/service-worker.js")
def sw():
     return app.send_static_file("service-worker.js")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5002)