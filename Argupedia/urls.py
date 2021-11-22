from . import views
from .views import ArgPostListView
from .views import ArgPostDetailView
from .views import ArgPostCreateView
from .views import Argument_NameView
from .views import ArgupediaDebateView
from .views import debatehome
from .views import Argdetview
from .views import reply
from .views import replystruct
from .views import upvote
from .views import downvote
from .views import ArgFutureListView
from .views import ArgFutureDetail

from .views import grounded


from django.urls import path



urlpatterns = [
    # path for the latest announcemnt page
    path('Latest/Announcements/', ArgPostListView.as_view(), name='arg-home'),
    # path for the latest future plans page
    path('Future/Plans/', ArgFutureListView.as_view(), name='future-home'),
    # path for the future plans details
    path('Future/<int:pk>', ArgFutureDetail.as_view(), name='future-plans'),
    # path for the future plans details
    path('Future/new/', ArgPostCreateView.as_view(), name='future-create'),
    # path for the reports page
    path('reports/', views.reports, name='reports'),
    # path for the reports page confirmation
    path('reports/user/confirm', views.reportsreturn, name='reportuserconfirm'),
    # path for the rules/Terms and conditions page
    path('rules', views.Rules, name='Rules'),
    # path for the contact info page
    path('Contact/Page/', views.inde, name='contact-info'),
    # path for the report page
    path('report/argument/', views.index, name='reportpost'),
    # path for the contact confirm page
    path('ContactReturn/', views.contactReturn, name='contactReply'),
    # path for the argument detail page
    path('argupedia/detail', debatehome.as_view(), name='argupedia-home'),
    path('', views.about, name='arg-about'),
    # PK=Primary Key of Debate Post we want to view, set to integer as this is
    # what we only expect to see after the Debate posted.
    # path for the guidance page
    path('guidance/', views.guidance, name='guidance'),
    # path for the specific argument
    path('argupedia/debate/<int:pk>/', ArgPostDetailView.as_view(), name='debate-detail'),
    # path for creation debate
    path('debate/new/', ArgPostCreateView.as_view(), name='debate-create'),

    # PK=Primary Key of Debate Post we want to view, set to integer as this is
    # what we only expect to see for when navigating to a specific Argument
    # Scheme template
    # path for the argument scheme
    path("debate/<int:pk>/ArgumentScheme/", Argument_NameView.as_view(),
         name="Arg-scheme"),
    #    path for the construction page
    path("debate/<int:pk>/Construction/", ArgupediaDebateView.as_view(),
         name="debate-construct"),
    # path for the details page
    path("debate/<int:debate>/detail/", Argdetview.as_view(),
         name="debate-view"),
    # path for the reply page
    path("debate/<int:reply>/reply/",
         reply.as_view(), name="Arg-counter"),
    path("debate/<int:pk>/question/<int:cqs_id>/reply/<int:reply>/", replystruct.as_view(), name="reply-view"),
    # path for the like
    path('debate/<int:pk_react>/like', upvote.as_view(), name='voteup'),
    # path for the dislike
    path('debate/<int:pk_react>/nlike', downvote.as_view(), name='votedown'),

    # path for the FAQ
path('FAQ/', views.FAQ, name='FAQ'),
    # path for the grounded semantics
path("debate/<int:args>/grounded/semantics/", grounded.as_view(), name="grounded-sem"),


]