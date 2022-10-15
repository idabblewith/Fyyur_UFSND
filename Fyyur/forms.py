from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
)
from wtforms.validators import DataRequired, Length, AnyOf, URL


class ShowForm(FlaskForm):
    class Meta:
        pass

    artist_id = StringField(
        "artist_id"  # name of this field, also used as our label in html
    )
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.now()
    )


class VenueForm(FlaskForm):
    class Meta:
        pass

    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        # rearranged order
        "state",
        validators=[DataRequired()],
        choices=[
            ("AL"),
            ("AK"),
            ("AZ"),
            ("AR"),
            ("CA"),
            ("CO"),
            ("CT"),
            ("DE"),
            ("DC"),
            ("FL"),
            ("GA"),
            ("HI"),
            ("ID"),
            ("IL"),
            ("IN"),
            ("IA"),
            ("KS"),
            ("KY"),
            ("LA"),
            ("MA"),
            ("MD"),
            ("ME"),
            ("MI"),
            ("MN"),
            ("MO"),
            ("MS"),
            ("MT"),
            ("NC"),
            ("ND"),
            ("NE"),
            ("NH"),
            ("NJ"),
            ("NM"),
            ("NY"),
            ("NV"),
            ("OH"),
            ("OK"),
            ("OR"),
            ("PA"),
            ("RI"),
            ("SC"),
            ("SD"),
            ("TN"),
            ("TX"),
            ("UT"),
            ("VT"),
            ("VA"),
            ("WA"),
            ("WV"),
            ("WI"),
            ("WY"),
        ],
    )
    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired()])
    image_link = StringField(
        "image_link",
        default="https://assets3.thrillist.com/v1/image/3107044/1584x1056/crop;webp=auto;jpeg_quality=60;progressive.jpg",
    )
    # How to get the link to not show and only set if field is null
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired()],
        choices=[
            ("Alternative", "Alternative"),
            ("Blues", "Blues"),
            ("Classical", "Classical"),
            ("Country", "Country"),
            ("Electronic", "Electronic"),
            ("Folk", "Folk"),
            ("Funk", "Funk"),
            ("Hip-Hop", "Hip-Hop"),
            ("Heavy Metal", "Heavy Metal"),
            ("Instrumental", "Instrumental"),
            ("Jazz", "Jazz"),
            ("Musical Theatre", "Musical Theatre"),
            ("Pop", "Pop"),
            ("Punk", "Punk"),
            ("R&B", "R&B"),
            ("Reggae", "Reggae"),
            ("Rock n Roll", "Rock n Roll"),
            ("Soul", "Soul"),
            ("Other", "Other"),
        ],
    )
    facebook_link = StringField("facebook_link", validators=[URL()])
    website = StringField("website", validators=[URL()])
    seeking = BooleanField(
        "seeking",
    )
    seeking_description = StringField(
        "seeking_description",
    )


class ArtistForm(FlaskForm):
    class Meta:
        pass

    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        # rearranged order
        "state",
        validators=[DataRequired()],
        choices=[
            ("AL"),
            ("AK"),
            ("AZ"),
            ("AR"),
            ("CA"),
            ("CO"),
            ("CT"),
            ("DE"),
            ("DC"),
            ("FL"),
            ("GA"),
            ("HI"),
            ("ID"),
            ("IL"),
            ("IN"),
            ("IA"),
            ("KS"),
            ("KY"),
            ("LA"),
            ("MA"),
            ("MD"),
            ("ME"),
            ("MI"),
            ("MN"),
            ("MO"),
            ("MS"),
            ("MT"),
            ("NC"),
            ("ND"),
            ("NE"),
            ("NH"),
            ("NJ"),
            ("NM"),
            ("NY"),
            ("NV"),
            ("OH"),
            ("OK"),
            ("OR"),
            ("PA"),
            ("RI"),
            ("SC"),
            ("SD"),
            ("TN"),
            ("TX"),
            ("UT"),
            ("VT"),
            ("VA"),
            ("WA"),
            ("WV"),
            ("WI"),
            ("WY"),
        ],
    )
    phone = StringField(
        "phone",
    )
    image_link = StringField(
        "image_link",
        default="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.ezygtyzqIHfqkklq4Sw5TwHaE6%26pid%3DApi&f=1",
    )
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired()],
        choices=[
            ("Alternative", "Alternative"),
            ("Blues", "Blues"),
            ("Classical", "Classical"),
            ("Country", "Country"),
            ("Electronic", "Electronic"),
            ("Folk", "Folk"),
            ("Funk", "Funk"),
            ("Hip-Hop", "Hip-Hop"),
            ("Heavy Metal", "Heavy Metal"),
            ("Instrumental", "Instrumental"),
            ("Jazz", "Jazz"),
            ("Musical Theatre", "Musical Theatre"),
            ("Pop", "Pop"),
            ("Punk", "Punk"),
            ("R&B", "R&B"),
            ("Reggae", "Reggae"),
            ("Rock n Roll", "Rock n Roll"),
            ("Soul", "Soul"),
            ("Other", "Other"),
        ],
    )
    facebook_link = StringField("facebook_link", validators=[URL()])
    website = StringField("website", validators=[URL()])
    seeking = BooleanField(
        "seeking",
    )
    seeking_description = StringField(
        "seeking_description",
    )
