__author__ = "Jeremy Nelson"
import datetime
from flask_wtf import Form
from wtforms import SelectField, StringField, TextAreaField
from wtforms import validators

DIGITAL_ORIGIN = [('born digital'),
                  ('reformatted digital'),
                  ('digitized microfilm'),
                  ('digitized other analog')]


GENRE = [('choose', 'Choose...'),
         ("abstract or summary", "Abstract or Summary"),
         ("art original", "Art Original"),
         ("art reproduction", "Art Reproduction"),
         ("article", "Article"),
         ("atlas", "Atlas"),
         ("autobiography ", "Autobiography "),
         ("bibliography", "Bibliography"),
         ("biography", "Biography"),
         ("book ", "Book "),
         ("calendar", "Calendar"),
         ("catalog", "Catalog"),
         ("chart", "Chart"),
         ("comic or graphic novel ", "Comic or Graphic Novel "),
         ("comic strip", "Comic Strip"),
         ("conference publication", "Conference Publication"),
         ("database", "Database"),
         ("dictionary", "Dictionary"),
         ("diorama", "Diorama"),
         ("directory", "Directory"),
         ("discography", "Discography"),
         ("drama", "Drama"),
         ("encyclopedia", "Encyclopedia"),
         ("essay", "Essay"),
         ("festschrift", "Festschrift"),
         ("fiction", "Fiction"),
         ("filmography", "Filmography"),
         ("filmstrip", "Filmstrip"),
         ("finding aid ", "Finding Aid "),
         ("flash card", "Flash Card"),
         ("folktale ", "Folktale "),
         ("font", "Font"),
         ("game", "Game"),
         ("government publication ", "Government Publication "),
         ("graphic", "Graphic"),
         ("globe", "Globe"),
         ("handbook", "Handbook"),
         ("history ", "History "),
         ("hymnal", "Hymnal"),
         ("humor, satire", "Humor, Satire"),
         ("index", "Index"),
         ("instruction ", "Instruction "),
         ("interview ", "Interview "),
         ("issue", "Issue"),
         ("journal", "Journal"),
         ("kit", "Kit"),
         ("language instruction", "Language Instruction"),
         ("law report or digest", "Law Report or Digest"),
         ("legal article", "Legal Article"),
         ("legal case and case notes", "Legal Case and Case Notes"),
         ("legislation", "Legislation"),
         ("letter ", "Letter "),
         ("loose-leaf ", "Loose-Leaf "),
         ("map", "Map"),
         ("memoir ", "Memoir "),
         ("microscope slide", "Microscope Slide"),
         ("model", "Model"),
         ("motion picture", "Motion Picture"),
         ("multivolume monograph", "Multivolume Monograph"),
         ("newspaper", "Newspaper"),
         ("novel ", "Novel "),
         ("numeric data", "Numeric Data"),
         ("offprint", "Offprint"),
         ("online system or service", "Online System or Service"),
         ("patent", "Patent"),
         ("periodical", "Periodical"),
         ("picture", "Picture"),
         ("poetry ", "Poetry "),
         ("programmed text", "Programmed Text"),
         ("realia", "Realia"),
         ("rehearsal ", "Rehearsal "),
         ("remote sensing image", "Remote Sensing Image"),
         ("reporting ", "Reporting "),
         ("review", "Review"),
         ("script", "Script"),
         ("series", "Series"),
         ("short story", "Short Story"),
         ("slide", "Slide"),
         ("sound ", "Sound "),
         ("speech", "Speech"),
         ("standard or specification", "Standard or Specification"),
         ("statistics", "Statistics"),
         ("survey of literature", "Survey of Literature"),
         ("technical drawing", "Technical Drawing"),
         ("technical report", "Technical Report"),
         ("thesis", "Thesis"),
         ("toy", "Toy"),
         ("transparency", "Transparency"),
         ("treaty", "Treaty"),
         ("videorecording ", "Videorecording "),
         ("web site", "Web Site"),
         ("yearbook", "Yearbook")]
         

CONTENT_MODELS = [('sp_basic_image', 'Basic Image Content Model'),
                  ('sp_pdf', 'PDF Content Model'),
                  ('compoundCModel', 'Compound Object Content Model'),
                  ('sp-audioCModel', 'Audio Content Model'),
                  ('sp_videoCModel', 'Video Content Model')]

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
    content_models = SelectField('Islandora Content Model',
                                  choices=CONTENT_MODELS,
                                  default='compoundCModel')
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
        choices=GENRE)
    number_objects = StringField('Number of stub records', default=1)
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
