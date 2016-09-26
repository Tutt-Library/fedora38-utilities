__author__ = "Jeremy Nelson"
import datetime
from flask_wtf import Form
from wtforms import SelectField, StringField, TextAreaField
from wtforms import validators

DIGITAL_ORIGIN = [(1, 'born digital'),
                  (2, 'reformatted digital'),
                  (3, 'digitized microfilm'),
                  (4, 'digitized other analog')]


GENRE = [('choose', 'Choose...')]

INSTITUTION_NAME = 'Colorado College'

MARC_FREQUENCY = [('choose', 'Choose...'),
                  ('Semiweekly', 'Semiweekly - 2 times a week'),
                  ('Three times a week', 'Three times a week'),
                  ('Weekly', 'Weekly'),
                  ('Biweekly', 'Biweekly - every 2 weeks'),
                  ('Three times a month', 'Three times a month'),
                  ('Semimonthly', 'Semimonthly - 2 times a month'),
                  ('Monthly', 'Monthly'),
                  ('Bimonthly', 'Bimonthly - every 2 months'),
                  ('Quarterly', 'Quarterly'),
                  ('Three times a year', 'Three times a year'),
                  ('Semiannual', 'Semiannual - 2 times a year'),
                  ('Annual', 'Annual'),
                  ('Biennial', 'Biennial - every 2 years'),
                  ('Triennial', 'Triennial - every 3 years'),
                  ('Completely irregular', 'Completely irregular')]

OBJECT_TEMPLATES = [(0, 'Choose model'),
                    (1, 'Meeting Minutes'),
                    (2, 'Newsletter'),
                    (3, 'Podcast'),
                    (4, 'Video'),
                    (5, 'Master (All fields)')]

RIGHTS_STATEMENT = "Copyright restrictions apply. Contact Colorado College for permission to publish."
PLACE = 'Colorado Springs (Colo.)'
PUBLISHER = "Colorado College"
PUBLICATION_PLACE = 'Colorado Springs, Colorado'

class AddFedoraObjectFromTemplate(Form):
    admin_note = TextAreaField('Administrative Notes',
                               validators=[validators.length(max=1500)])
    alt_title = StringField('Alternative Title')
    collection_pid = StringField("PID of Parent Collection",
        validators=[validators.required(), validators.length(max=20)])
    contributors = StringField("Contributors")
    corporate_contributors = StringField("Corporate Contributors")
    corporate_creators = StringField("Corporate Creators")
    creators = StringField("Creators")
    date_created = StringField('Date Created')
    digital_origin = SelectField('Digital Origin',
        choices=DIGITAL_ORIGIN)
    description = TextAreaField('Description',
                                validators=[validators.optional(), 
                                            validators.length(max=1500)])
    extent = TextAreaField('Extent',
                            validators=[validators.optional(), 
                                       validators.length(max=1500)])
    form = StringField('Form')
    frequency_free_form = StringField('Other')
    frequency = SelectField('Frequency',
        choices=MARC_FREQUENCY)
    genre = SelectField('Genre',
        choices=[])
    genre_free_form = StringField('Other')
    number_objects = StringField('Number of stub records', default=1)
    object_template = SelectField('Content Model Template',
                                  choices=OBJECT_TEMPLATES)
    organizations = StringField("Organizations",
                                validators=[validators.optional(), 
                                            validators.length(max=255)],
                                default=INSTITUTION_NAME)
    rights_holder = TextAreaField('Rights Statement',
                                   default=RIGHTS_STATEMENT)
    subject_dates = StringField('Subject -- Dates')
    subject_people = StringField('Subject -- People')
    subject_places = StringField('Subject -- Places',
                                 default=PLACE)
    subject_topics = StringField('Subject -- Topic')
    title = StringField('Title',
            validators=[validators.length(max=120), validators.optional()])
    type_of_resource = StringField('Type of Resource')
