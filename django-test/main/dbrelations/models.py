from django.db import models

# Many-to-one relationships
    # For example, if a Car model has a Manufacturer-
    # that is, a Manufacturer makes multiple cars but each Car only has one Manufacturer
# To define a many-to-one relationship, use django.db.models.ForeignKey. 
# ForeignKey requires a positional argument: the class to which the model is related.
class Reporter(models.Model):
    first_name = models.CharField(max_length=30) 
    last_name = models.CharField(max_length=30) 
    email = models.EmailField()
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
#
class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self): 
        return self.headline
    
    class Meta:
        ordering = ['headline']


# One to one relationship
    # For example, if you were building a database of “places”, you would build pretty standard stuff 
    # such as address, phone number, etc. in the database. 
    # Then, if you wanted to build a database of restaurants on top of the places, instead of repeating 
    # yourself and replicating those fields in the Restaurant model, 
    # you could make Restaurant have a OneToOneField to Place 
    # (because a restaurant “is a” place; in fact, to handle this you’d typically use 
    # inheritance, which involves an implicit one-to-one relation).

# OneToOneField requires a positional argument: the class to which the model is related.
# To define a one-to-one relationship, use OneToOneField. 
# In this example, a Place optionally can be a Restaurant:
class Place(models.Model):
    name = models.CharField(max_length=50) 
    address = models.CharField(max_length=80)

    def __str__(self):
        return "%s the place" % self.name

class Restaurant(models.Model): 
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True,)
    serves_hot_dogs = models.BooleanField(default=False) 
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name

class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE) 
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)

# Many-to-many relations
    # For example, if a Pizza has multiple Topping objects 
    # – that is, a Topping can be on multiple pizzas and each Pizza has multiple toppings
# To define a many-to-many relationship, use ManyToManyField.
# In this example, an Article can be published in multiple Publication objects, 
# and a Publication has multiple Article objects:
# ManyToManyField requires a positional argument: the class to which the model is related.
class Publication(models.Model):
    title = models.CharField(max_length=30)
    page_no = models.CharField(max_length=30)

    class Meta:
        ordering = ['title', 'page_no'] 
        
    def __str__(self):
        return self.title

class Article(models.Model):
    headline = models.CharField(max_length=100) 
    # publications = models.ManyToManyField(Publication)
    # models.ManyToManyField is raised an error, but why? every thing same wit django docs
    publications = models.ForeignKey(Publication, on_delete=models.CASCADE)

    class Meta:
        ordering = ['headline']
    def __str__(self): 
        return self.headline

class Person(models.Model):
    name = models.CharField(max_length=128) 
    
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self): 
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE) 
    group = models.ForeignKey(Group, on_delete=models.CASCADE) 
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)