from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse

import datetime
from .models import ArgPost
from .models import Argument_Name
from .models import Argument_Fields
from .models import ArgFuture
from .models import Contactinfo
from .models import reportPost
from .models import Categories
from .models import ArgProfile
from .models import Video
from django.contrib.auth.models import User
from .models import Arg_Posts
from django.views.generic import ListView, DetailView,View
from django.views.generic import CreateView
from .models import CQ
from itertools import chain
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ArgRegister, changes, changespro,changesfield
from django.contrib.auth.decorators import login_required



# signup request for users profile
# To gain a better understanding of the use of PK "primary key" and its function
# when it realtes to database
# https://docs.djangoproject.com/en/3.2/topics/db/queries/
class grounded(View):
    def get(self, request, args):
        winning = []
        # winning list
        losing = []
        # losing lists
        unknown = []
        # undecided lists
        saved = {
            "unknown": unknown,
            "winning": winning,
            "args": Arg_Posts.objects.get(pk=args).get_family(),
            "losing": losing,

        }
        n = 1000
        # n for while reply
        while n > 0:
            # executes the loop until the condition is met
            print(n)
            n -= 10
            for i in Arg_Posts.objects.get(pk=args).get_family():
                # for loop over all arguments present in the family
                if not i.id in losing:
                    # if it isn't in losing assign decision as false
                    decision = False
                    for x in i.replies():
                        # loops over the replies
                        if x.id in unknown:
                            # if the replies is in the unknown set assign decision as false
                            decision = False
                        elif x.id in winning:
                            # if it is in winning set assign In as true
                            decision = True
                    if decision != False:
                        # if in does not = false assing argument into losing set
                        losing.append(i.id)
                if not i.id in winning != True and not i.id in losing != True and not i.id in unknown != True:
                    # if argument not present in any of the sets In = True
                    decision = True
                    for x in i.replies():
                        # loops over the replies from the modal
                        if x.id not in losing:
                            # if it isnt in losing
                            decision = False
                            # = false
                    if decision != False:
                        # appends it to the winning set.
                        winning.append(i.id)

        return render(request, "Argupedia/groundedsemantics.html", saved)




def signup(request):
    # inspiration taken from :
    #  https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    # request method for post to send the request to the webpage
    if request.method == 'POST':
        # if statement checking that if the if the register form has been
        # entered with valid information will then save the form.
        if ArgRegister(request.POST).is_valid():
            ArgRegister(request.POST).save()
            messages.success(request, f'Account has been Created!')
            # redirects the user back to the signin page so that they can then
            # login.
            return redirect('signin')
    else:
        # if they do not fill in the form correctly they are then navigated
        # back to the same form page
        ArgRegister()

    return render(request, 'Argupedia/signup.html', {'form': ArgRegister()})
# Adds functionality user must be logged in to view the page.

# login required to view the user's profile otherwise throws an error
@login_required
def Argprofile(request):
    # request method for post to send the request to the webpage
    if request.method == 'POST':
        # change request for the users name, sends a post request by the user
        # to change their username on the profile page
        change = changes(request.POST, instance=request.user)
        # change request for the users profile picture, sends a post request for
        # that specific user profile page, request.files allows user to upload
        # the picture of their choice and, reuqest.user.profile links it back
        # to said users profile.
        changepro = changespro(request.POST, request.FILES, instance=request.user.argprofile)
        # allows user to change their specific subjject field and links it back
        # to said users profile page
        changefield = changesfield(request.POST, instance=request.user.argprofile)

        # checks to see if the changes are valid and if they are then they will
        #save the changes made
        if change.is_valid() and changepro.is_valid() and changefield.is_valid():
            change.save()
            changefield.save()
            changepro.save()
            # updates the user that their changes have been made
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        # if they are not valid then the changes do not occur
        # profile stays the same
    else:
        change = changes(instance=request.user)
        changepro = changespro(instance=request.user.argprofile)
        changefield = changesfield(instance=request.user.argprofile)

    return render(request, 'Argupedia/ArgupediaProfile.html',{'change':change, 'changepro':changepro, 'changefield':changefield})


# Argupedia home function stores objects in debate variable
def Arghome(request):
    # stores all the objects of the posts into the debate variable
    # allowing for it to be looped over
    debate = {
'debate': ArgPost.objects.all()
    }

    # Returns the debate variable which are the posts and links it to the
    # relevant html file.
    return render(request, 'Argupedia/announcements.html',debate)



# Argupedia about page, links to the home.html page
def about(request):
     # links the function to the about page
    return render(request, 'Argupedia/home.html', {'title': 'About'})


def FAQ(request):
    # links the function to the about page
    return render(request, 'Argupedia/FAQ.html', {'title': 'FAQ'})

def Rules(request):
    # links the function to the about page
    return render(request, 'Argupedia/Terms .html', {'title': 'FAQ'})


# Argupedia Contact page, links to the home.html page


# Argupedia Guisance page, links to the home.html page
def guidance(request):
    # link for the guidance page linking it to the html
    guidance_video = {
        # gets the guidance video from the models
        'guidance_video': Video.objects.all()
    }
    # displays the guidance video
    return render(request, 'Argupedia/guidance.html',guidance_video)

# Creates a list view which details how the post will be displayed
class ArgPostListView(ListView):
    # Post list view to re-order the list
    # Links the it do ArgPost model
    model = ArgPost
    # Links to template name
    template_name = 'Argupedia/announcements.html'
    # Links to the variale within the model
    context_object_name = 'debates'
    # Orders the debate post by order of newest
    ordering = ['-arg_date_posted']

# specifies the detail view page of the ArgPost view
class ArgPostDetailView(DetailView):
    # links to the model name to the .modely.py file
    model = ArgPost

# Create view displays a form for creating the object, consists of validation
class ArgPostCreateView(CreateView):
# Defines the title and content information from the models.py file
    model = ArgPost
    # defines the fields to be used
    fields = ['arg_debate_title','arg_content']
    # saves the form information when information is filled in
    def form_valid(self, form):
        # The form trying to submit take the instance and author and link it
        # to the logged in user.
        form.instance.author = self.request.user
        # Saves the form
        return super().form_valid(form)

# def function for future announcment pages
def futureannouncment(request):
    # stores all the future announcment posts made
    # allows for these to be looped over and displayed in the html file.
    announcement = {
'announcement': ArgFuture.objects.all()
    }
    # Returns the information to the and links it to the relevant html file.
    return render(request, 'Argupedia/futureplans.html',announcement)


class ArgFutureListView(ListView):
    # Post list view to re-order the list
    # Links the it do ArgPost model
    model = ArgFuture
    # Links to template name
    template_name = 'Argupedia/futureplans.html'
    # Links to the variale within the model
    context_object_name = 'announcement'
    # Orders the debate post by order of newest
    ordering = ['-arg_future_date']


# Inspiration for detailview page
# https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-display/
# https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin
class ArgFutureDetail(DetailView):
    model = ArgFuture

# Create view displays a form for creating the object, consists of validation
# inspiration for createview
#https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#django.views.generic.edit.CreateView
class ArgFutureCreateView(CreateView):

# Defines the title and content information from the models.py file
    model = ArgFuture
    fields = ['arg_future_plans_title ',' arg_future_plans_detail']
    def form_valid(self, form):
        # The form trying to submit take the instance and author and link it
        # to the logged in user.
        form.instance.author = self.request.user
        # Saves the form
        return super().form_valid(form)

# View for Argument Scheme Names
# inspiration for view
# https://docs.djangoproject.com/en/3.2/ref/class-based-views/base/#django.views.generic.base.View

class Argument_NameView(View):
    # Links the model to the relevant models.py class
    model = Arg_Posts
    # Returns all the Argument Scheme names.

# Stores the Argument Scheme names in the Args variable field and gets the
    # primary key of each scheme
    def get(self, request, pk):
        Args = {
            'Args': Argument_Name.objects.all()
        }
        # Returns the list of Argument scheme names saved in the admin section
        return render(request, "Argupedia/argument_name_list.html", Args)

class Argument_testView(View):
    # Links the model to the relevant models.py class
    model = Arg_Posts
    # Returns all the Argument Scheme names.

# Stores the Argument Scheme names in the Args variable field and gets the
    # primary key of each scheme
    def get(self, request, pk):
        Args = {
            'Args': Argument_Name.objects.all(),
            # stores and saves the objects that can then be called in the HTML file
            'Argsf': Argument_Fields.objects.filter(Argument_name_field=pk),
            # filters by the argument Primary key
            "argsch": pk
        }
        # Returns the list of Argument scheme names saved in the admin section
        return render(request, "Argupedia/test_design.html", Args)


# Inspiration for detailview page
# https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-display/
# https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin
#
# Class for the debate view, for when user constructs the argument debate

class ArgupediaDebateView(View):
    # Relates back to the model.py relevant class
    model = Argument_Name
    # Gains the relevant fields that will be used to define the views
    fields = ['Argument_Name', 'Argument_Fields']

    # defining function to get fields associated with the Argument scheme and
    # filters via the scheme id and primary key


    def get(self, request, pk):
        # stores the relvant fields that will eb needed to construct the debate
        # filters the field names by the relevant argument scheme primary key
        Args = {
            # filters by the objects primary key
            'Args': Argument_Fields.objects.all().filter(Argument_name_field=pk),"argsch": pk,
            # gets all the categories for the objects
            "cat": Categories.objects.all()

        }

        # links it back to the relevant html page so the system knows where to
        # links the html file
        return render(request, "Argupedia/argupedia_debate_detail.html", Args)


    def post(self,request, pk, *args,**kwargs):
            if request.method == "POST":
                posts = Arg_Posts
                id = Argument_Name.objects.get(pk=pk)
                # inspriation on linking back the filed names and reponse to the
                # specific post the user had created
                # https://docs.djangoproject.com/en/3.2/topics/db/queries/

                # creates an empty list for the argument field name and the information
                # for it to be stored into
                author = request.user
                # filed name list
                field_name = []
                # field information list
                field_info = []

                field_delete = []
                # gets the title from the debate
                title = request.POST['debate']
               # displays the category
                cat = Categories.objects.get(pk=request.POST.get('cat'))
                # loops over the scheme fields and assigns it a primary key so that
                # the system assigns the specific field a primary key id to it and then
                # will know how to filer it by
                #
                # Inspiration on using filter method by the primary key to link the
                # specific filed names and reponses to the one that the user had
                # created.
                # https://www.programiz.com/python-programming/methods/built-in/filter
                # inspiration on applying the filter methodology and why the get method
                # didnt work.
                # https://stackoverflow.com/questions/22063748/django-get-returned-more-than-one-topic
                for userent in  Argument_Fields.objects.all().filter(Argument_name_field=pk):
                    # for loop checks
                    if userent not in Argument_Fields.objects.all().filter(Argument_name_field=pk):
                        # appends it into the list
                        field_delete.insert(4, userent.Argument_field_name)
                    else:
                        # else appends in the field name list
                        field_name.insert(4, userent.Argument_field_name)

                    # inserts the field name to the string defined

                # again loops over the specific argument fields for the post made which
                # is associated by the pk
                for userent in Argument_Fields.objects.all().filter(Argument_name_field=pk):
                    # inserts it into the list above both given the same insert order
                    # number 4 so when the list concatonnates it will format them
                    if userent not in Argument_Fields.objects.all().filter(Argument_name_field=pk):
                        field_delete.insert(4, userent.Argument_field_name)
                    else:
                     # together
                        field_info.insert(4,request.POST.get(userent.Argument_field_name))
                # stores the list in a variable for ease of reading
                argument = field_name
                # stores the list in a variable for ease of reading
                userentry = field_info
                # inspiration on how to conncatonate the two strings
                # https://stackoverflow.com/questions/28271850/itertools-zip-two-list-into-each-other
                presentable = list(chain(*zip(argument, userentry)))
                # formating the string which joins them together and seperates them
                # with \n which splits by row for every new entered
                information = "\n" " \n".join(presentable)
                # stores and saves the information into post variable
                posts(argupedia_user=author, information = information, argupedia_topic=title, Categories=cat,Argument_name_post=Argument_Name.objects.get(pk=pk)).save()


                # redirects the user back to the home page once they have entered their
                # argument.
                return redirect('argupedia-home')
            # denotes the information into the relevant HTML page
            return render(request, 'Argupedia/argupedia_debate_detail.html')

def inde(request):
    # contact page method
    # if the POST request is successful
    if request.method =="POST":
        # stores contact in method
        contact=Contactinfo()
        # gets the name and sends it to the model said variable name
        name = request.POST.get('name')
        # gets the email and sends it to the model said variable name
        email = request.POST.get('email')
        # gets the subject and sends it to the model said variable name
        subject = request.POST.get('subject')
        # stores the name in name variable
        contact.name = name
        # stores the contact email in email variable
        contact.email = email
        # stores contact subject in subject variable
        contact.subject = subject
        # save the contact.
        contact.save()
        # redirects user to the contact confirmation page.
        return redirect("contactReply")

# matches it to the contact page.
    return render(request,'Argupedia/contact.html')

def index(request):
    # if the POST request is successful
    if request.method=="POST":
        # report method
        report = reportPost()
        #  gets user reporting and sends it to the model with said name
        user_reporting = request.POST.get('user_reporting')
        # gets user reported and sends it to the model with said name
        user_reported = request.POST.get('user_reported')
        # gets the url link and sends it to the model with said name
        urllink = request.POST.get('urllink')
        # gets reason and sends it to the model with said name
        reason = request.POST.get('reason')
        # links the user reporting to the variable name
        report.user_reporting = user_reporting
        # links the user reported to the variable name
        report.user_reported = user_reported
        # links the reason to the variable name
        report.reason = reason
        # links the url to the variable name
        report.urllink = urllink
        # saves the report
        report.save()
        # redirects the user to the report confirm page
        return redirect('reportuserconfirm')
    # links the code to said html page
    return render(request,'Argupedia/reportPost.html')

def reportsreturn(request):
    # links the function to the about page
    return render(request, 'Argupedia/reportpostconfirm.html')


# Stores and displayes there arguments in the Arghome page
class debatehome(View):
    def get(self, request):
        # Stores the arguments in the debate cases variable
        # orders the debates by arg_date that they had ordered it by.
        debate_cases = {
            # orders the argument by date of the newest
            'debate_cases': Arg_Posts.objects.all().order_by('-arg_date')
        }
        order = ['arg_date']

        # Returns it in the designated HTML file
        return render(request, "Argupedia/View_debates.html", debate_cases)
def reports(request):

    # counts how many users there are
    users_count = User.objects.count()
    # counts how many arguments and replies have been made
    post_count = Arg_Posts.objects.count()
    # gets the users, count their interactions, displays how many times they have posted and orders by count
    pop_user = Arg_Posts.objects.values("argupedia_user_id").annotate(count=Count('argupedia_user_id')).order_by("-count")
    # gets the topic, count how many times its been used  displays how many times its been used and orders by count
    pop_topic = Arg_Posts.objects.values("Categories").annotate(count=Count('Categories')).order_by("-count")
    # shows users who have joined today.
    today = datetime.date.today()
    qs = ArgProfile.objects.filter(time__gt=today)



    return render(
        # saves the variables to be displayed to the user.
        request, 'Argupedia/reports.html', {'user_count': users_count , 'post_count': post_count , 'pop_user':pop_user, 'qs':qs,'pop_topic':pop_topic}
    )


def contactReturn(request):
    # links the function to the about page
    return render(request, 'Argupedia/contactReturn.html')

# Displays the Argument detail class which gets the title and relevant
# information entered within the file
class Argdetview(View):
    # https://django-mptt.readthedocs.io/en/latest/models.html
    # variable participant stores all replies to original post.
    # variable argtopic gathers the topic description of the debate later to be called in HTML
    # file.
    # variable  stores the Argument id to identify each debate and
    # which post replies to which
    def get(self, request, debate):
        participant = {
            # gets the family of all argument debate
            'participant': Arg_Posts.objects.get(pk=debate).get_family(),
            # gets the ancestors of all argument entries and doesnt include self
            'participan': Arg_Posts.objects.get(pk=debate).get_ancestors(ascending=True, include_self=False),
            # gets the debate of all argument topics
            'argtopic': Arg_Posts.objects.get(pk=debate).argupedia_topic,
            # gets the category associated with the debate
            'argfield': Arg_Posts.objects.get(pk=debate).Categories,
            # stores the debate as grounded
            "grounded": debate,
        }
        # Returns all the information under the variable participant into the Arg_detail
        # HTML file
        return render(request, "Argupedia/Arg_detail.html", participant)


class reply(View):
 # Class for beginning countering process of the debate
 # reply
 #view stores the various functions from models.py into the variable
    def get(self,request,reply):
        # stores the information needed to reply the Argument in the variable

        # argsche displays all the argupedia debate names for the user to use
        argument_schemes = {
            'argsch': Argument_Name.objects.all(),
            # stores the scheme name
            "weakp": CQ.objects.filter(Argument_crit_name=Arg_Posts.objects.get(
                pk=reply).Argument_name_post.id),
            # https://docs.python.org/3/library/functions.html#filter

            # it gets the critical question by looking at the argument name associated with each scheme
            'userput': Arg_Posts.objects.get(pk=reply),

            # critical questions filter allowing for the critical question that
            # the user used to be displayed
            # https://stackoverflow.com/questions/22063748/django-get-returned-more-than-one-topic
            # filter used as get returns mutliple results when we only need the one used.

        }
        # returns to the Argreply.html file
        return render(request, "Argupedia/Argreply.html", argument_schemes)


class replystruct(View):
    model = Argument_Name
    # Gains the relevant fields
    fields = ['Argument_Name', 'Argument_Field_Name']
    def get(self, request, reply, pk, cqs_id):
        argument_schemes = {
            # stores the relevant fields needed to construct the reply
            # filter method used as its the only one that can retrieve the information
            # from the back-end effectively
            # filters by the argument name and field
            "details": Argument_Fields.objects.filter(Argument_name_field=pk),
            # filters by the critical questions associated with the argument scheme
            "weakp": CQ.objects.filter(Argument_crit_name= Arg_Posts.objects.get(pk=reply).Argument_name_post.id),
            # stores the primary key
            "sch": pk,
            # gets the critical question id
            "cqs_id": cqs_id,
            # gets the reply objects
            "userput": Arg_Posts.objects.get(pk=reply)
        }
        return render(request, "Argupedia/Argreplypost.html", argument_schemes)

    def post(self, request, pk, reply, cqs_id):
        critq = []
        # field name list
        field_name = []
        # field info list
        field_info = []
        # critical question objects
        crits = CQ.objects.get(pk=request.POST.get('attackc'))

        # for loops over the objects and filter by the pk
        for fields in Argument_Fields.objects.filter(Argument_name_field=pk):
            # appends the field name into the list
            field_name.append(fields.Argument_field_name)
            # filters over the argument name by the pk
        for fields in Argument_Fields.objects.filter(Argument_name_field=pk):
            # appends the field argument name
            field_info.append(request.POST.get(fields.Argument_field_name))
        # stores it in an easier variable name
        argument = field_name
        # stores it in an easier variable name
        userentry = field_info

        # combines the items together in the list
        presentable = list(chain(*zip(argument, userentry)))
        # presents it in a presentable format
        presentation = "\n" " \n".join(presentable)
        # saves it all in the Args Post
        Arg_Posts(argupedia_user=request.user, cqs=crits, information=presentation, Argument_name_post=Argument_Name.objects.get(pk=pk),  parent=Arg_Posts.objects.get(pk=reply)).save()
        # redirects the user.
        return redirect('argupedia-home')








# class for upvoting/liking a post
class upvote(View):
    # defines the reaction under pk_react and saves the like
    def post(self, request, pk_react, *args, **kwargs):

        # stores the met method in variable reaction
        reaction = Arg_Posts.objects.get(pk=pk_react)

        # Defines the variable upvote as false before forloop, we dont start
        # with already votes on the argument
        downvote = False

        # loops over all votes regarding the debate post in question
        for downvotes in reaction.votedown.all():
            # if the upvote is done by a registered user
            if downvotes == request.user:
                # set the upvote to true, stoes that vote for the user
                downvote = True


        if downvote:
            reaction.votedown.remove(request.user)


                # if statement for action taking place other than an upvote
                # meaning a downvote
        upvote = False

        for upvotes in reaction.voteup.all():
            if upvotes == request.user:
                upvote=True

        if not upvote:
            # put in place to ensure that the user cannot keep incrementing the
            # the number of likes votes
            # if the user clicks the upvote button then the request will be made
            # if the vote is not in the upvote then it will upvote the argument
            reaction.voteup.add(request.user)
        if upvote:
            reaction.voteup.remove(request.user)

        # the upvote uses a http request so when the user clicks the button it
        # will navigate them to the same page
        return HttpResponseRedirect(request.POST.get('next','/'))

# class for downvoting/disliking a post
class downvote( View):
    # defines the reaction under pk_react and saves the like and saves it
    def post(self, request, pk_react, *args, **kwargs):
        # stores the objects.get with the primary key identity under variable
        # opinion
        opinion = Arg_Posts.objects.get(pk=pk_react)
        # identifies the variable outside the forloop and identifies as False
        upvote = False

        # loops over all votes regarding the debate post in question
        for upvotes in opinion.voteup.all():
            # if the upvote is done by a registered user
            if upvotes == request.user:
                # set the upvote to true, stoes that vote for the user
                upvote = True


        if upvote:
            opinion.voteup.remove(request.user)

            # if statement for action taking place other than an upvote
            # meaning a downvote
        downvote = False

        for downvotes in opinion.votedown.all():
            if downvotes == request.user:
                downvote = True

        if not downvote:
            # put in place to ensure that the user cannot keep incrementing the
            # the number of likes votes
            # if the user clicks the upvote button then the request will be made
            # if the vote is not in the upvote then it will upvote the argument
            opinion.votedown.add(request.user)
        if downvote:
                # if the user downvotes then it will remove it
            opinion .votedown.remove(request.user)

        # the upvote uses a http request so when the user clicks the button it
        # will navigate them to the same page
        return HttpResponseRedirect(request.POST.get('next', '/'))





