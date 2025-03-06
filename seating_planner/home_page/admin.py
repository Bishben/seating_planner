from django.contrib import admin
from .models import Branch, Subject, Event, Exam, ExamRoom, Room
from django import forms
from django.urls import path
from django.http import JsonResponse
from django_select2.forms import Select2Widget

# Register your models here.

## Branch Modification
class BranchAdmin(admin.ModelAdmin):
    """
    Customizes the Django Admin for the Branch model:
    - Displays the name, year, strength, and associated subjects in this order.
    - Subjects are shown in a comma-separated format (read-only field).
    - Uses prefetch_related for optimized database queries.
    """
    readonly_fields = ("display_subjects",)

    def display_subjects(self, obj):
        """
        Returns a comma-separated list of subjects associated with the branch.
        """
        return ", ".join([sub.code for sub in obj.subjects.all()])
    display_subjects.short_description = "Subjects"
    

    def get_queryset(self, request):
        """
        Optimizes query performance by prefetching related subjects.
        """
        return super().get_queryset(request).prefetch_related("subjects")

## Subject Modification: Makes Choices Field Horizontal
class SubjectAdmin(admin.ModelAdmin):
    """
    Customizes the Django Admin for the Subject model:
    - Displays the ManyToMany field (branches) as a horizontal multi-select.
    """
    filter_horizontal = ("branches",)  # Horizontal selection UI

## Exam Modification: Adds help_text for strength, 
class ExamAdminForm(forms.ModelForm):
    """
    Custom form for ExamAdmin to:
    - Add a help_text for the 'strength' field.
    - Filter the 'subject' field based on the selected branch.
    """
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adds a help text to the strength field
        self.fields['strength'].help_text = "Leave empty(0) to default to the actual strength of the selected branch."

        # Filter subjects based on branch after creation (ie When Editing)
        if self.instance and self.instance.pk:
            self.fields['subject'].queryset = Subject.objects.filter(branches=self.instance.branch) 

class ExamAdmin(admin.ModelAdmin):
    """
    Customizes the Django Admin for the Exam model:
    - Uses the custom ExamAdminForm for subject filtering.
    - Includes an AJAX endpoint to dynamically filter subjects when a branch is selected.
    - Links a JavaScript file for real-time filtering.
    """
    form = ExamAdminForm

    def get_urls(self):
        """
        Extends the default Django Admin URLs with a custom endpoint:
        - `/admin/app_name/exam/get_subjects/` for AJAX filtering of subjects.
        """
        urls = super().get_urls()
        custom_urls = [
            path('get_subjects/', self.admin_site.admin_view(self.get_subjects), name="get_subjects"),
        ]
        return custom_urls + urls

    def get_subjects(self, request):
        """
        Handles AJAX request to fetch subjects based on the selected branch.
        Returns a JSON response with subject ID and code.
        """
        branch_id = request.GET.get('branch_id')
        subjects = Subject.objects.filter(branches__id=branch_id).values('id', 'code') if branch_id else []
        return JsonResponse(list(subjects), safe=False)

    class Media:
        """
        Includes JavaScript for dynamic subject filtering based on branch selection.
        """
        js = ('admin/js/subject_filter.js',) 

## ExamRoom Modification: Makes Choices Field Horizontal
class ExamRoomAdminForm(forms.ModelForm):
    class Meta:
        model = ExamRoom
        fields = "__all__"
        exclude = ['matrix',] 
    
    exam_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Media:
        js = ('admin/js/roll_selector.js',)

class ExamRoomAdmin(admin.ModelAdmin):
    form = ExamRoomAdminForm

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get_exams/', self.admin_site.admin_view(self.get_exams), name='get_exams'),
            path('get_exam_room/', self.admin_site.admin_view(self.get_exam_room), name='get_exam_room'),
        ]
        return custom_urls + urls
    
    def get_exam_room(self, request):
        """
        Returns a JSON response containing exam rooms filtered by event.
        """
        event_id = request.GET.get("event_id")
        room_num = request.GET.get("room")
        if event_id:
            exams = ExamRoom.objects.filter(event_id=event_id, number=room_num).values("id", "exam_data")
            return JsonResponse(list(exams), safe=False)
        return JsonResponse([], safe=False)


    def get_exams(self, request):
        """
        Returns a JSON response containing exams filtered by event.
        """
        event_id = request.GET.get("event_id")
        if event_id:
            exams = Exam.objects.filter(event_id=event_id).values("id", "branch__name", "branch__year", "subject__code")
            return JsonResponse(list(exams), safe=False)
        return JsonResponse([], safe=False)

    
## Model Registrations
admin.site.register(Branch, BranchAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Event)
admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamRoom, ExamRoomAdmin)
admin.site.register(Room)

