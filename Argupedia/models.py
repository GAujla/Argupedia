
from django.core.exceptions import ValidationError

from django.urls import reverse

import datetime



# Create your models here.

from django.db import models

# https://docs.djangoproject.com/en/3.2/topics/db/models/ Details how to create
# data models in models.py for Django
# Construct an Argument Scheme as text field to which Admin can enter
# the argument scheme name
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db import models
from django.contrib.auth.models import User

# Model to model view of the database
# https://docs.djangoproject.com/en/3.2/topics/db/models/

class ArgPost(models.Model):
    # stores the title
    announcement = models.TextField()
    # stores the content information
    arg_content = models.TextField()
    # stores the author, cascade will cascade the deleting effects of the
    # deletion of the author
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    # stores the date and time the post was created
    arg_date_posted = models.DateTimeField(default=datetime.datetime.now)

    # returns the debate title in the admin section of django
    def __str__(self):
        return self.announcement
    class Meta:
        verbose_name_plural = "Announcements"

    # Django knows how to find the location for a specific post
    # Reverse function will return to the URL as a string


class Argument_Name(models.Model):
    # defines argument name in text field
    Argument_Name = models.TextField()
    # defines argument information in text field
    Argument_information = models.TextField(blank=True)
    # defines argument source in text field
    Argument_source = models.TextField(blank=True)
    # Returns the Argument Scheme Name that is visible to the Admin
    def __str__(self):
        return self.Argument_Name
    # Validation error prompt warning the user of the potential error
    def clean(self):
        if self.Argument_Name == None:
            raise ValidationError(_('Argument Name may not have a name assoc'
                                    'iated'))

# Construct Argument Fields as text field to which Admin can enter
# the argument scheme relevant fields.
class Argument_Fields(models.Model):
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.ForeignKey
    # used to fully understand the concept of foreign key in django database
    # Links the two data models together in the database
    Argument_name_field = models.ForeignKey(Argument_Name,on_delete=models.PROTECT)
    # Stores the Argument field name
    Argument_field_name = models.TextField(blank=True)
    # Description of the Argument Premise
    Argument_field = models.TextField(blank=True)
    # Information user enters about the source they are getting this information
    # from
    Argument_source = models.TextField(blank=True)
    # any specific information to help additional administrators later on
    Argument_additional_info= models.TextField(blank=True)


    # Returns the Argument Scheme Field names which the Users will have to
    # fill out
    def __str__(self):
        return self.Argument_field
    # Validation error prompt warning the user of the potential error
    def clean(self):
        if self.Argument_field == None:
            raise ValidationError(_('Argument may not have any fields associ'
                                    'ated with it'))


class  reportPost(models.Model):
    # text field for user reporting
    user_reporting = models.TextField(blank=True)
    # text field for user reported
    user_reported = models.EmailField()
    # text field for user reason
    reason = models.TextField()
    # text field for url link
    urllink = models.TextField(blank=True)
    def __str__(self):
        return self.user_reporting

class CQ(models.Model):
    # Links the Argument Scheme name to Critical Questions allowing for
    # a relationship to be made
    Argument_crit_name = models.ForeignKey(Argument_Name,on_delete=models.CASCADE)
    # specifies the critical questions that are to be entered by the admin
    CQ = models.TextField()
    # specifies the source as to why that critical question is chosen
    Argument_source = models.TextField(blank=True)
    # any additional information regarding the critical question
    Argument_additional_info = models.TextField(blank=True)
    # chosen as if the user selects a specific type of critical question
    # this will then be displayed as the two questions are attacking each other
    # https://docs.djangoproject.com/en/3.2/topics/db/models/
    CHOICES = [('1',True), ('2',False),('3','Other')]
    choice = models.BooleanField()
    # Returns the Critical Question
    def __str__(self):
        return self.CQ
    # # Validation error prompt warning the user of the potential error
    def clean(self):
        if self.Argument_crit_name == None:
            raise ValidationError(_('Argument may not have any Critical Questio'
                                    'ns Associated With it.'))

class Video(models.Model):
    description=models.TextField()
    video= models.FileField(upload_to="video/%y")
    def __str__(self):
        return self.description

class ArgFuture(models.Model):
    # stores the title
    arg_future_plans_title = models.TextField()
    # stores the content information
    arg_future_plans_detail = models.TextField()
    # stores the author, cascade will cascade the deleting effects of the
    # deletion of the author
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # stores the date and time the post was created
    arg_future_date = models.DateTimeField(default=datetime.datetime.now)
    # returns the future plans title to be visible in the admin section
    def __str__(self):
        return self.arg_future_plans_title
    # validation check to ensure the field has been entered
    def clean(self):
        if self.arg_future_plans_title == None:
            raise ValidationError(_('Argument may not have any Critical Questio'
                                    'ns Associated With it.'))

    # Django knows how to find the location for a specific post
    # Reverse function will return to the URL as a string
    def get_absolute_url(self):
        return reverse('future-plans', kwargs={'pk': self.pk})

    # Class for defining the relevant information to be detailed dealing with
    # the Argument post entries
class Categories(models.Model):
    cat = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cat}"

class Arg_Posts(MPTTModel):
    # Stores user name and has on.CASCADE attributes
    argupedia_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # The name of a field which relates the model back to itself such that each
    # instance can be a child of another instance.

    # Stores the date and time the debate was created
    arg_date = models.DateTimeField(default=datetime.datetime.now)
    # Stores and links the Argument Scheme Name used
    Argument_name_post = models.ForeignKey(Argument_Name, on_delete=models.CASCADE)
    # Stores the information user has entered to create their argument.
    information = models.TextField()

    # Stores the debate title that the argument was used
    argupedia_topic = models.TextField(blank=True)
    # links it to the Argument scheme name class
    cqs = models.ForeignKey(CQ, null=True,
                                           on_delete=models.CASCADE,
                                          related_name="cqs")
    # Vote up class
    voteup = models.ManyToManyField(User, blank=True, related_name='voteup')
    # vote down class
    votedown= models.ManyToManyField(User, blank=True, related_name='votedown')
    Categories = models.ForeignKey(Categories, null=True,on_delete=models.CASCADE)
    # https://django-mptt.readthedocs.io/en/latest/models.html#treeforeignkey-treeonetoonefield-treemanytomanyfieldp
    parent = TreeForeignKey("self", null=True, blank=True,
                            on_delete=models.CASCADE, related_name="children")



    def replies(self):
        # stores relies in list
        repatt = []
        # for loops over the children
        for i, item in enumerate(self.get_children()):
            # checks if it isnt in the leaf node
            if repatt != self.is_leaf_node():
                # appends the item
                repatt.append(item)
        else:
            print("appended")
            #checks parent does exist
        if self.parent is not None:
            print("there is a reply")
            # checks for ciritcal questions
            if self.cqs.choice != True and self.cqs.choice != None :
                print("appended")
                # checks if there is a critical question
            elif self.cqs.choice != False and self.cqs.choice != None:
                repatt.append(self.parent)
# returns
        return repatt







    # Returns the content of the debate information in the Admin page
    def __str__(self):
        return f'"{self.information}"'

    def clean(self):
        if self.argupedia_user == None:
            raise ValidationError('Argument may not have any Critical Questio'
                                    'ns Associated With it.')

    # Django knows how to find the location for a specific post
    # Reverse function will return to the URL as a string
class  Contactinfo(models.Model):
    # text field for name
    name = models.TextField(blank=True)
    # text field for email
    email = models.EmailField()
    # text field for subject
    subject = models.TextField()
    def __str__(self):
        return self.name





#creation for the user profile
class ArgProfile(models.Model):
    # defines their specalist area
    specalist = models.CharField(max_length=40)
    # defines the user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # defines the picture used
    pict = models.ImageField(default='default.png', upload_to='arguserpic')
    # time displaying the model.
    time = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f'{self.user.username}'
# saves all the information done.
    def save(self, *args, **kwargs):
        super().save()


