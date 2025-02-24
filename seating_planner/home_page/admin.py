from django.contrib import admin
from .models import Branch, Subject, Event, Exam, ExamRoom, Room
from django import forms

# Register your models here.

## Branch Modification: Displays Chosen Subjects
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "strength", "display_subjects")  
    readonly_fields = ("display_subjects",)  # Makes it visible but not editable

    def display_subjects(self, obj):
        return ", ".join([sub.code for sub in obj.subjects.all()])
    display_subjects.short_description = "Subjects"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("subjects")

## Subject Modification: Makes Choices Field Horizontal
class SubjectAdmin(admin.ModelAdmin):
    filter_horizontal = ("branches",)  # Horizontal selection UI

## Exam Modification: Adds help_text for strength, 


class ExamAdminForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['strength'].help_text = "If left empty, it will default to the total strength of the selected branch."

        # Initially, disable subject selection
        self.fields['subject'].queryset = Subject.objects.none()

class ExamAdmin(admin.ModelAdmin):
    form = ExamAdminForm

    class Media:
        js = ('admin/js/exam_subject_filter.js',)  # Load our custom JavaScript

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['subject'].queryset = Subject.objects.none()
        return form

## Models
admin.site.register(Branch, BranchAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Event)
admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamRoom)
admin.site.register(Room)

