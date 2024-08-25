from django.contrib import admin

# from .models import Exam
# Register your models here.

from .models import Exam,Question,Responses,Answer

# admin.site.register(Quest)
admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(Answer)
admin.site.register(Responses)


