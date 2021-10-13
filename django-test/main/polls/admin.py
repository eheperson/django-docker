from django.contrib import admin

# Register your models here.

from .models import Question,Choice

#
# One small problem with 'class ChoiceInline(admin.StackedInline): '
# It takes a lot of screen space to display all the fields for entering related Choice objects. 
# For that reason, Django offers a tabular way of displaying inline related objects; 
# you just need to change the 'ChoiceInline' declaration to read:  'class ChoiceInline(admin.TabularInline)'
# 
class ChoiceInline(admin.TabularInline): 
    """
    This tells Django: “Choice objects are edited on the Question admin page. 
    By default, provide enough fields for 3 choices.”

    It works like this: There are three slots for related Choices – as specified by extra – and each time you come back
    to the “Change” page for an already-created object, you get another three extra slots.
    """
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin): 
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline] # Do not forget add 
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
#    
admin.site.register(Question, QuestionAdmin)
#
#
# admin.site.register(Question)
# admin.site.register(Choice)
#
# admin.site.register(Author, AuthorAdmin)
# You’ll follow this pattern – create a model admin class, 
# then pass it as the second argument to admin.site.register(),
# any time you need to change the admin options for a model.