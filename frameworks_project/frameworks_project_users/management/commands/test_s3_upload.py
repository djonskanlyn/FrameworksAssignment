
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



# import boto3

# s3 = boto3.client('s3',aws_access_key_id=os.getenv('FP_AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('FP_AWS_SECRET_ACCESS_KEY'),region_name='eu-north-1')

# try:
#     s3.put_object(Bucket='frameworks-assignment-media-bucket', Key='test_upload/test_file.txt', Body=b'This is a test file.')
#     print("File successfully uploaded.")
# except Exception as e:
#     print(f"Error: {e}")