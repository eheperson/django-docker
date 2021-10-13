from django.db import models

# Create your models here.

"""
class Person(models.Model):
    first_name = models.CharField(max_length=30) 
    last_name = models.CharField(max_length=30)

The above Person model would create a database table like this:

CREATE TABLE myapp_person (
    "id" serial NOT NULL PRIMARY KEY, 
    "first_name" varchar(30) NOT NULL, 
    "last_name" varchar(30) NOT NULL
);



Using models :
    Once you have defined your models, you need to tell Django you’re going to use those models. 
    Do this by editing your settings file and changing the INSTALLED_APPS setting to add the name 
    of the module that contains your models.py.

    For example, if the models for your application live in the module myapp.models 
    (the package structure that is createdforanapplicationbythemanage.py startappscript),INSTALLED_APPSshouldread,inpart:

Field types :

Each field in your model should be an instance of the appropriate Field class. 

Django uses the field class types to determine a few things:
    The column type, which tells the database what kind of data to store (e.g. INTEGER, VARCHAR, TEXT).
    The default HTML widget to use when rendering a form field (e.g. <input type="text">, <select>). 
    The minimal validation requirements, used in Django’s admin and in automatically-generated forms.


Field options :

Each field takes a certain set of field-specific arguments (documented in the model field reference). 
For example, CharField (and its subclasses) require a max_length argument which specifies the size of 
the VARCHAR database field used to store the data.


- null :  If it is True, Django will store empty values as NULL in the database. Default is False.
- blank : If it is True, the field is allowed to be blank. Default is False.

    Note that this is different than null. 
    null is purely database-related, whereas blank is validation-related. 
    If a field has blank=True, form validation will allow entry of an empty value. 
    If a field has blank=False, the field will be required.

- choices : It is a sequence of 2-tuples to use as choices for this field.      
            If this is given, the default form widget will be a select box instead 
            of the standard text field and will limit choices to the choices given.

    A choices list looks like this:

        YEAR_IN_SCHOOL_CHOICES = [ 
            ('FR', 'Freshman'), 
            ('SO', 'Sophomore'), 
            ('JR', 'Junior'), 
            ('SR', 'Senior'), 
            ('GR', 'Graduate'),
        ]

        Note : The first element in each tuple is the value that will be stored in the database. 
               The second element is displayed by the field’s form widget.
        Note : Given a model instance, the display value for a field with choices can be accessed using the
               get_FOO_display() method. For example:
               .get_year_in_school_choices_display()

- default :  The default value for the field. This can be a value or a callable object. 
             If callable it will be called every time a new object is created.

- help_text : Extra “help” text to be displayed with the form widget. 
              It’s useful for documentation even if your field isn’t used on a form.

- primary_key : If True,this field is the primary key for the model.

                This is an auto-incrementing primary key.

                If you don’t specify primary_key=True for any fields in your model, 
                Django will automatically add an IntegerField to hold the primary key, 
                so you don’t need to set primary_key=True on any of your fields unless you 
                want to override the default primary-key behavior.

                Note :  The primary key field is read-only. 
                        If you change the value of the primary key on an existing object and then save it, 
                        a new object will be created alongside the old one.

- unique : If True, this field must be unique throughout the table.

- verbose_name :  Each field type, except for ForeignKey, ManyToManyField and OneToOneField, 
                  takes an optional first positional argument – a verbose name. 
                  
                  If the verbose name isn’t given, 
                  Django will automatically create it using the field’s attribute name, 
                  converting underscores to spaces.

                  Inthisexample,theverbosenameis"person's first name":
                    first_name = models.CharField("person's first name", max_length=30)

                  Inthisexample,theverbosenameis"first name": 
                    first_name = models.CharField(max_length=30)

                  Note : ForeignKey, ManyToManyField and OneToOneField require the first argument to be a model class, 
                         so use the verbose_name keyword argument:
                            sites = models.ManyToManyField(Site, verbose_name="list of sites")
"""




class Musician(models.Model):
    """
    'first_name', 'last_name' and 'instrument' are fields of the model. 
    Each field is specified as a class attribute, 
    and each attribute maps to a database column.
    """
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()

    MUSIC_TYPES = (
        ('0', 'Rock'),
        ('1', 'Blues'),
        ('2', 'Jazz'),
        ('3', 'Metal'),
        ('4', 'Classic'),
        ('5', 'Pop'),
        ('6', 'Electro'),
    )
    music_type = models.CharField(max_length=1, choices=MUSIC_TYPES)