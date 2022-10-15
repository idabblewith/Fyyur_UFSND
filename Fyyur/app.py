# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import sys
from datetime import datetime
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Models
# ----------------------------------------------------------------------------#

# Fully Normalised/Logically grouped


class Venue(db.Model):
    __tablename__ = "venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)

    shows = db.relationship("Show", backref="venue", cascade="all", lazy="dynamic")
    location = db.relationship(
        "Vlocation", backref="venue", cascade="all, delete", lazy="dynamic"
    )
    contact = db.relationship(
        "Vcontact", backref="venue", cascade="all, delete", lazy="dynamic"
    )
    seek = db.relationship(
        "Vseek", backref="venue", cascade="all, delete", lazy="dynamic"
    )
    image = db.relationship(
        "Vimage", backref="venue", cascade="all, delete", lazy="dynamic"
    )
    genres = db.relationship(
        "Vgenres", backref="venue", cascade="all, delete", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Venue ID: {self.id} | Venue Name: {self.name}>"


class Artist(db.Model):
    __tablename__ = "artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)

    shows = db.relationship("Show", backref="artist", cascade="all", lazy="dynamic")
    location = db.relationship(
        "Alocation", backref="artist", cascade="all, delete", lazy="dynamic"
    )
    contact = db.relationship(
        "Acontact", backref="artist", cascade="all, delete", lazy="dynamic"
    )
    seek = db.relationship(
        "Aseek", backref="artist", cascade="all, delete", lazy="dynamic"
    )
    image = db.relationship(
        "Aimage", backref="artist", cascade="all, delete", lazy="dynamic"
    )
    genres = db.relationship(
        "Agenres", backref="artist", cascade="all, delete", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Artist ID: {self.id} | Artist Name: {self.name}>"


class Show(db.Model):
    __tablename__ = "show"

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(
        db.Integer, db.ForeignKey("venue.id", ondelete="CASCADE"), nullable=False
    )
    artist_id = db.Column(
        db.Integer, db.ForeignKey("artist.id", ondelete="CASCADE"), nullable=False
    )
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Show ID: {self.id} | Show VID: {self.venue_id} | Show AID: {self.artist_id} | Show Start: {self.start_time}>"


# Henceforth, setting foreign keys referencing original tables as primary keys to avoid repetition of data
# caused by setting a separate 'id' column,and strengthen relationship/integrity (for example when cascade
# deleting original table) as they do not autoincrement, and are simply based on original table.


class Vlocation(db.Model):
    __tablename__ = "vlocation"

    venue_id = db.Column(
        db.Integer,
        db.ForeignKey("venue.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f"<Venue ID: {self.venue_id} | Venue Loc: {self.address}, {self.city}, {self.state}>"


class Alocation(db.Model):
    __tablename__ = "alocation"

    artist_id = db.Column(
        db.Integer,
        db.ForeignKey("artist.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f"<Artist ID: {self.artist_id} | Artist Loc: {self.city}, {self.state}>"


class Vcontact(db.Model):
    __tablename__ = "vcontact"

    venue_id = db.Column(
        db.Integer,
        db.ForeignKey("venue.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    phone = db.Column(db.String(15))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))

    def __repr__(self):
        return f"<Venue ID: {self.venue_id} | CPhone: {self.phone}, CWeb: {self.website}, CFb:{self.facebook_link}>"


class Acontact(db.Model):
    __tablename__ = "acontact"

    artist_id = db.Column(
        db.Integer,
        db.ForeignKey("artist.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    phone = db.Column(db.String(15))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))

    def __repr__(self):
        return f"<Artist ID: {self.artist_id} | CPhone: {self.phone}, Cweb: {self.website}, CFb: {self.facebook_link}>"


class Vseek(db.Model):
    __tablename__ = "vseek"

    venue_id = db.Column(
        db.Integer,
        db.ForeignKey("venue.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    seeking = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(250), default="")

    def __repr__(self):
        return f"<Venue ID: {self.venue_id} | Seek: {self.seeking}, {self.seeking_description}>"


class Aseek(db.Model):
    __tablename__ = "aseek"

    artist_id = db.Column(
        db.Integer,
        db.ForeignKey("artist.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    seeking = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(250), default="")

    def __repr__(self):
        return f"<Artist ID: {self.artist_id} | Seek: {self.seeking}, {self.seeking_description}>"


class Vimage(db.Model):
    __tablename__ = "vimage"

    venue_id = db.Column(
        db.Integer,
        db.ForeignKey("venue.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    image_link = db.Column(db.String, nullable=False, default="")

    def __repr__(self):
        return f"<Venue ID: <{self.venue_id} | Image: {self.image_link}>"


class Aimage(db.Model):
    __tablename__ = "aimage"

    artist_id = db.Column(
        db.Integer,
        db.ForeignKey("artist.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    image_link = db.Column(db.String, nullable=False, default="")

    def __repr__(self):
        return f"<Artist ID: {self.artist_id} | Image: {self.image_link}>"


class Vgenres(db.Model):
    __tablename__ = "vgenres"

    venue_id = db.Column(
        db.Integer,
        db.ForeignKey("venue.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    genres = db.Column(db.ARRAY(db.String), nullable=False)

    def __repr__(self):
        return f"<Venue ID: {self.venue_id} | Genres: {self.genres}>"


class Agenres(db.Model):
    __tablename__ = "agenres"

    artist_id = db.Column(
        db.Integer,
        db.ForeignKey("artist.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    genres = db.Column(db.ARRAY(db.String), nullable=False)

    def __repr__(self):
        return f"<Artist ID: <{self.artist_id} | Genres: {self.genres}>"


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


# ----------------------------------------------------------------------------#
#  VENUE SECTION
# ----------------------------------------------------------------------------#

#  Create Venue (C)
# ----------------------------------------------------------------------------#
@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


# Above: Takes in the VenueForm() to get fields.
# Below: Uses the VenueForm() to send inputted data to various models, creating
# instances of those models (inputting data in each respective table)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    form = VenueForm(request.form)
    error = False
    try:
        venue = Venue(name=form.name.data)
        db.session.add(venue)
        db.session.commit()

        location = Vlocation(
            venue_id=venue.id,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
        )

        contact = Vcontact(
            venue_id=venue.id,
            phone=form.phone.data,
            facebook_link=form.facebook_link.data,
            website=form.website.data,
        )

        genre = Vgenres(
            venue_id=venue.id,
            genres=form.genres.data,
        )

        image = Vimage(
            venue_id=venue.id,
            image_link=form.image_link.data,
        )

        seek = Vseek(
            venue_id=venue.id,
            seeking=form.seeking.data,
            seeking_description=form.seeking_description.data,
        )

        db.session.add_all([location, contact, genre, image, seek])
        db.session.commit()

    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        flash(
            "An error occurred. Venue '"
            + request.form["name"]
            + "' could not be listed."
        )
    if not error:
        flash("Venue '" + request.form["name"] + "' was successfully listed!")

    return render_template("pages/home.html")


#  Read Venue (R)
# ----------------------------------------------------------------------------#
@app.route("/venues")
def venues():
    places = (
        db.session.query(Vlocation.city, Vlocation.state)
        .distinct(Vlocation.city, Vlocation.state)
        .all()
    )
    data = []

    for eachplace in places:
        venue = (
            db.session.query(Venue.name, Venue.id, Vlocation)
            .join(Vlocation, Venue.id == Vlocation.venue_id)
            .filter(Vlocation.city == eachplace[0])
            .filter(Vlocation.state == eachplace[1])
        )

        data.append({"city": eachplace[0], "state": eachplace[1], "venues": venue})

    # Gets every distinct location and lists all venues playing there via jinja2
    # formatting (appended information gets sent to jinja html). All locations
    # in the database must have a venue, so this method works here.

    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    search_term = request.form.get("search_term")
    venues = (
        db.session.query(Venue).filter(Venue.name.ilike("%" + search_term + "%")).all()
    )

    data = []
    for eachvenue in venues:
        data.append(
            {
                "id": eachvenue.id,
                "name": eachvenue.name,
            }
        )

    response = {"count": len(venues), "data": data}

    # Uses the (case-)insensitive like (ilike) operator to query for items like search_term
    # Appends that items id and name to data, sets amount of results and data in response.
    # Sends response and search_term to jinja2.

    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    vloc = Vlocation.query.get(venue_id)
    vgenres = Vgenres.query.get(venue_id)
    vcontact = Vcontact.query.get(venue_id)
    vseek = Vseek.query.get(venue_id)
    vimage = Vimage.query.get(venue_id)
    # Used for 'data'/jinja, below

    past_shows = []
    upcoming_shows = []

    # lowercase 'venue' for 'venue.id' below refers to above variable to filter data for current venue
    get_past_shows = (
        db.session.query(Show, Aimage, Artist)
        .filter(
            Show.venue_id == venue.id,
            Show.artist_id == Aimage.artist_id,
            Show.artist_id == Artist.id,
        )
        .filter(Show.start_time < datetime.now())
    )
    get_upcoming_shows = (
        db.session.query(Show, Aimage, Artist)
        .filter(
            Show.venue_id == venue.id,
            Show.artist_id == Aimage.artist_id,
            Show.artist_id == Artist.id,
        )
        .filter(Show.start_time > datetime.now())
    )

    for eachshow in get_past_shows:
        past_shows.append(
            {
                "artist_id": eachshow.Aimage.artist_id,
                "artist_name": eachshow.Artist.name,
                "artist_image_link": eachshow.Aimage.image_link,
                "start_time": eachshow.Show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    for eachshow in get_upcoming_shows:
        upcoming_shows.append(
            {
                "artist_id": eachshow.Aimage.artist_id,
                "artist_name": eachshow.Artist.name,
                "artist_image_link": eachshow.Aimage.image_link,
                "start_time": eachshow.Show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": vgenres.genres,
        "address": vloc.address,
        "city": vloc.city,
        "state": vloc.state,
        "phone": vcontact.phone,
        "website": vcontact.website,
        "facebook_link": vcontact.facebook_link,
        "seeking_venue": vseek.seeking,
        "seeking_description": vseek.seeking_description,
        "image_link": vimage.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": db.session.query(Show, Aimage, Artist)
        .filter(
            Show.venue_id == venue.id,
            Show.artist_id == Aimage.artist_id,
            Show.artist_id == Artist.id,
        )
        .filter(Show.start_time < datetime.now())
        .count(),
        "upcoming_shows_count": Show.query.filter(Show.venue_id == venue.id)
        .filter(Show.start_time > datetime.now())
        .count(),
    }
    return render_template("pages/show_venue.html", venue=data)


#  Update Venue (U)
# ----------------------------------------------------------------------------#
@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    vlocation = Vlocation.query.get(venue_id)
    vgenres = Vgenres.query.get(venue_id)
    vcontact = Vcontact.query.get(venue_id)
    vseek = Vseek.query.get(venue_id)
    vimage = Vimage.query.get(venue_id)

    form.name.data = venue.name
    form.city.data = vlocation.city
    form.state.data = vlocation.state
    form.address.data = vlocation.address

    form.phone.data = vcontact.phone
    form.facebook_link.data = vcontact.facebook_link
    form.website.data = vcontact.website

    form.image_link.data = vimage.image_link
    form.genres.data = vgenres.genres

    form.seeking.data = vseek.seeking
    form.seeking_description.data = vseek.seeking_description

    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)
    vlocation = Vlocation.query.get(venue_id)
    vgenres = Vgenres.query.get(venue_id)
    vcontact = Vcontact.query.get(venue_id)
    vseek = Vseek.query.get(venue_id)
    vimage = Vimage.query.get(venue_id)

    error = False

    try:
        venue.name = form.name.data
        vlocation.city = form.city.data
        vlocation.state = form.state.data
        vlocation.address = form.address.data
        vcontact.phone = form.phone.data
        vgenres.genres = form.genres.data
        vcontact.facebook_link = form.facebook_link.data
        vcontact.website = form.website.data
        vimage.image_link = form.image_link.data
        vseek.seeking = form.seeking.data
        vseek.seeking_description = form.seeking_description.data
        db.session.commit()

    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        flash("Venue '" + form.name.data + "' was successfully updated.")
    else:
        flash(
            "Failed to update Venue. The name may already be taken or the form was incorrectly filled."
        )

    return redirect(url_for("show_venue", venue_id=venue_id))


#  Delete Venue (D)
# ----------------------------------------------------------------------------#
@app.route("/venues/<venue_id>/delete", methods=["DELETE"])
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    error = False

    try:
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    return render_template("pages/home.html")


# ----------------------------------------------------------------------------#
#  ARTIST SECTION
# ----------------------------------------------------------------------------#

#  Create Artist (C)
# ----------------------------------------------------------------------------#
@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    form = ArtistForm(request.form)
    error = False
    try:
        artist = Artist(name=form.name.data)
        db.session.add(artist)
        db.session.commit()

        location = Alocation(
            artist_id=artist.id, city=form.city.data, state=form.state.data
        )

        contact = Acontact(
            artist_id=artist.id,
            phone=form.phone.data,
            facebook_link=form.facebook_link.data,
            website=form.website.data,
        )

        genre = Agenres(
            artist_id=artist.id,
            genres=form.genres.data,
        )

        image = Aimage(
            artist_id=artist.id,
            image_link=form.image_link.data,
        )

        seek = Aseek(
            artist_id=artist.id,
            seeking=form.seeking.data,
            seeking_description=form.seeking_description.data,
        )

        db.session.add_all([location, contact, genre, image, seek])
        db.session.commit()

    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        flash(
            "An error occurred. Artist name '"
            + request.form["name"]
            + "'  could not be listed."
        )

    if not error:
        flash("Artist '" + request.form["name"] + "' was successfully listed!")

    return render_template("pages/home.html")


#  Read Artist (R)
# ----------------------------------------------------------------------------##
@app.route("/artists")
def artists():
    places = (
        db.session.query(Alocation.city, Alocation.state)
        .distinct(Alocation.city, Alocation.state)
        .all()
    )
    data = []

    for eachplace in places:
        artist = (
            db.session.query(Artist.name, Artist.id, Alocation)
            .join(Alocation, Artist.id == Alocation.artist_id)
            .filter(Alocation.city == eachplace[0])
            .filter(Alocation.state == eachplace[1])
        )

        data.append({"city": eachplace[0], "state": eachplace[1], "artists": artist})

    return render_template("pages/artists.html", areas=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    search_term = request.form.get("search_term")
    print(search_term)
    artists = (
        db.session.query(Artist)
        .filter(Artist.name.ilike("%" + search_term + "%"))
        .all()
    )
    print(artists)

    data = []
    for eachartist in artists:
        data.append(
            {
                "id": eachartist.id,
                "name": eachartist.name,
                "num_upcoming_shows": len(
                    db.session.query(Show)
                    .filter(Show.artist_id == eachartist.id)
                    .filter(Show.start_time > datetime.now())
                    .all()
                ),
            }
        )

    response = {"count": len(artists), "data": data}

    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    aloc = Alocation.query.get(artist_id)
    agenres = Agenres.query.get(artist_id)
    acontact = Acontact.query.get(artist_id)
    aseek = Aseek.query.get(artist_id)
    aimage = Aimage.query.get(artist_id)
    past_shows = []
    upcoming_shows = []

    # lowercase 'artist' for 'artist.id' below refers to above variable to filter data for current artist
    get_past_shows = (
        db.session.query(Show, Vimage, Venue)
        .filter(
            Show.artist_id == artist.id,
            Show.venue_id == Vimage.venue_id,
            Show.venue_id == Venue.id,
        )
        .filter(Show.start_time < datetime.now())
    )
    get_upcoming_shows = (
        db.session.query(Show, Vimage, Venue)
        .filter(
            Show.artist_id == artist.id,
            Show.venue_id == Vimage.venue_id,
            Show.venue_id == Venue.id,
        )
        .filter(Show.start_time > datetime.now())
    )

    for eachshow in get_past_shows:
        past_shows.append(
            {
                "venue_id": eachshow.Vimage.venue_id,
                "venue_name": eachshow.Venue.name,
                "venue_image_link": eachshow.Vimage.image_link,
                "start_time": eachshow.Show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    for eachshow in get_upcoming_shows:
        upcoming_shows.append(
            {
                "venue_id": eachshow.Vimage.venue_id,
                "venue_name": eachshow.Venue.name,
                "venue_image_link": eachshow.Vimage.image_link,
                "start_time": eachshow.Show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": agenres.genres,
        "city": aloc.city,
        "state": aloc.state,
        "phone": acontact.phone,
        "website": acontact.website,
        "facebook_link": acontact.facebook_link,
        "seeking_venue": aseek.seeking,
        "seeking_description": aseek.seeking_description,
        "image_link": aimage.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": db.session.query(Show, Vimage, Venue)
        .filter(
            Show.artist_id == artist.id,
            Show.venue_id == Vimage.venue_id,
            Show.venue_id == Venue.id,
        )
        .filter(Show.start_time < datetime.now())
        .count(),
        "upcoming_shows_count": Show.query.filter(
            Show.artist_id == artist.id, Show.start_time > datetime.now()
        ).count(),
    }

    return render_template("pages/show_artist.html", artist=data)


# Update Artist (U)
# ----------------------------------------------------------------------------#
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    alocation = Alocation.query.get(artist_id)
    agenres = Agenres.query.get(artist_id)
    acontact = Acontact.query.get(artist_id)
    aseek = Aseek.query.get(artist_id)
    aimage = Aimage.query.get(artist_id)

    form.name.data = artist.name
    form.city.data = alocation.city
    form.state.data = alocation.state

    form.phone.data = acontact.phone
    form.facebook_link.data = acontact.facebook_link
    form.website.data = acontact.website

    form.image_link.data = aimage.image_link
    form.genres.data = agenres.genres

    form.seeking.data = aseek.seeking
    form.seeking_description.data = aseek.seeking_description

    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)
    alocation = Alocation.query.get(artist_id)
    agenres = Agenres.query.get(artist_id)
    acontact = Acontact.query.get(artist_id)
    aseek = Aseek.query.get(artist_id)
    aimage = Aimage.query.get(artist_id)

    error = False

    try:
        artist.name = form.name.data
        alocation.city = form.city.data
        alocation.state = form.state.data
        acontact.phone = form.phone.data
        agenres.genres = form.genres.data
        acontact.facebook_link = form.facebook_link.data
        acontact.website = form.website.data
        aimage.image_link = form.image_link.data
        aseek.seeking = form.seeking.data
        aseek.seeking_description = form.seeking_description.data
        db.session.commit()

    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        flash("Artist '" + form.name.data + "' was successfully updated.")
    else:
        flash(
            "Failed to update Artist. The name may already be taken or the form was incorrectly filled."
        )

    return redirect(url_for("show_artist", artist_id=artist_id))


#  Delete Artist (D)
# ----------------------------------------------------------------------------#
@app.route("/artists/<artist_id>/delete", methods=["DELETE"])
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    error = False

    try:
        db.session.delete(artist)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    return render_template("pages/home.html")


# ----------------------------------------------------------------------------#
#  SHOW SECTION
# ----------------------------------------------------------------------------#

#  Create Show (C)
# ----------------------------------------------------------------------------#
@app.route("/shows/create")
def create_shows():
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    form = ShowForm(request.form)
    error = False
    try:
        show = Show(
            venue_id=form.venue_id.data,
            artist_id=form.artist_id.data,
            start_time=form.start_time.data,
        )
        db.session.add(show)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        flash("Show was successfully listed!")
    else:
        flash("Error, show was not listed!")

    return render_template("pages/home.html")


#  Read Show (R)
# ----------------------------------------------------------------------------#
@app.route("/shows")
def shows():
    now = datetime.now()
    venues_playing = (
        db.session.query(Venue)
        .distinct(Venue.name)
        .filter(Venue.id == Show.venue_id, Show.start_time >= now)
        .all()
    )
    data = []

    for eachvenue in venues_playing:
        shows = (
            db.session.query(Show, Artist, Venue, Aimage.image_link)
            .filter(Show.start_time >= now, Show.venue_id == eachvenue.id)
            .filter(
                Artist.id == Show.artist_id,
                Artist.id == Aimage.artist_id,
                Show.artist_id == Aimage.artist_id,
                Show.venue_id == Venue.id,
            )
            .order_by(Show.start_time.desc())
            .all()
        )
        count = len(shows)
        if count == 0:
            continue
        data.append({"venue": eachvenue, "shows": shows, "count": count})

    return render_template("pages/shows.html", data=data)


#  Update Show (U)
# ----------------------------------------------------------------------------#
# UNIMPLEMENTED / NOT #TODO OR ON RUBRIC

#  Delete Show (D)
# ----------------------------------------------------------------------------#
# UNIMPLEMENTED / NOT #TODO OR ON RUBRIC

# ----------------------------------------------------------------------------#
#  ERROR
# ----------------------------------------------------------------------------#
@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#
# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
