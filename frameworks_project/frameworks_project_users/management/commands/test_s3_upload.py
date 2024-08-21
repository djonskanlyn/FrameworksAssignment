
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = "Test file upload to AWS S3"

    def handle(self, *args, **kwargs):
        # Create some content for the file
        file_content = ContentFile(b"This is a test file for S3 upload.")
        
        # Define a file name
        test_file_name = 'test_upload/test_file.txt'

        # Try to save the file to the default storage (which should be S3)
        try:
            file_path = default_storage.save(test_file_name, file_content)
            self.stdout.write(self.style.SUCCESS(f"File successfully uploaded to S3: {file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error uploading file to S3: {e}"))