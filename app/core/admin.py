from django.contrib import admin


from core.models import Category
from core.models import Profile
from core.models import Sample
from core.models import DefaultCategory
from core.models import Transaction


admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Sample)
admin.site.register(DefaultCategory)
