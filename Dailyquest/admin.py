from django.contrib import admin

# Register your models here.


from .models import Quest,Question,Responses,Answer

admin.site.register(Quest)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Responses)


