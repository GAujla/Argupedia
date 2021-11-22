from django.contrib import admin
from django.contrib import admin
# import from model
from .models import Argument_Name
# import from model
from .models import Argument_Fields
# import from model
from .models import CQ
# import from model
from .models import ArgPost
# import from model
from .models import Categories
# import from model
from .models import Arg_Posts
# import from model
from .models import ArgProfile
# import from model
from .models import ArgFuture
# import from model
from .models import Contactinfo
# import from model
from .models import reportPost
# import from model
from .models import Video

# displays model
admin.site.register(Argument_Name)
admin.site.register(Argument_Fields)
admin.site.register(CQ)
admin.site.register(ArgPost)
admin.site.register(Contactinfo)
admin.site.register(Arg_Posts)
admin.site.register(ArgProfile)
admin.site.register(ArgFuture)
admin.site.register(reportPost)
admin.site.register(Categories)
admin.site.register(Video)

