from django.contrib import admin

# Register your models here.
from .models import OJ,CodeSubmission,topic,problemset
admin.site.register(OJ)
admin.site.register(topic)
admin.site.register(problemset)
admin.site.register(CodeSubmission)
