from django.contrib import admin

from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html

from exam.models import Answer
# Register your models here.

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'answer', 'status', 'download_link']
    list_filter = ['status']
    actions = ['download_selected_answers']

    def download_selected_answers(self, request, queryset):
        # Create a zip file containing selected answers
        # This assumes 'answer' is a FileField in your model
        import zipfile
        import os
        from io import BytesIO

        # Create a BytesIO object to store the zip file
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for answer in queryset:
                file_path = answer.answer.path  # Assuming 'answer' is the FileField
                file_name = os.path.basename(file_path)
                zip_file.write(file_path, arcname=file_name)

        # Seek to the beginning of the BytesIO buffer
        zip_buffer.seek(0)

        # Create the HttpResponse object with the appropriate headers
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=selected_answers.zip'

        return response

    download_selected_answers.short_description = "Download selected answers"

    def download_link(self, obj):
        # Display a download link in the admin list view
        return format_html('<a href="{}">Download</a>', reverse('admin:download_answer', args=[obj.pk]))

    download_link.short_description = "Download Link"

admin.site.register(Answer)
