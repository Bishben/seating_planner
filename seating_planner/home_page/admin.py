from django.contrib import admin
from .models import Branch, Subject, Event, Exam, ExamRoom, Room
from django import forms
from django.urls import path
from django.http import JsonResponse

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
        js = ('admin/js/exam_subject_filter.js',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # If editing an existing exam, allow the selected subject
        if obj and obj.branch:
            form.base_fields['subject'].queryset = obj.branch.subjects.all()
        else:
            form.base_fields['subject'].queryset = Subject.objects.none()

        return form

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("get_subjects_by_branch/", self.admin_site.admin_view(self.get_subjects), name="get_subjects_by_branch"),
        ]
        return custom_urls + urls  # Add custom URLs before default ones

    def get_subjects(self, request):
        """ Return subjects related to the selected branch as JSON """
        branch_id = request.GET.get("branch_id")

        if branch_id:
            subjects = Subject.objects.filter(branches__id=branch_id).values("id", "code")
        else:
            subjects = Subject.objects.none()

        return JsonResponse({"subjects": list(subjects)})

## Models
admin.site.register(Branch, BranchAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Event)
admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamRoom)
admin.site.register(Room)

