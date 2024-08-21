from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):
    #     # Open the uploaded image
    #     img = Image.open(self.image)

    #     # Define the max width and height for resizing
    #     max_size = (300, 300)  # You can change this size to your preference

    #     # Resize the image while maintaining aspect ratio
    #     img.thumbnail(max_size)

    #     # Save the image to an in-memory file
    #     img_io = BytesIO()
    #     img_format = self.image.name.split('.')[-1].upper()  # Get the format from the filename
    #     if img_format in ["JPG", "JPEG"]:
    #         img_format = "JPEG"
    #     img.save(img_io, format=img_format)

    #     # Create a new Django ContentFile and overwrite the original image with the resized one
    #     resized_image = ContentFile(img_io.getvalue(), name=self.image.name)

    #     # Save the resized image to storage (this will automatically upload it to S3)
    #     self.image = resized_image

    #     # Call the original save() method to continue saving the instance
    #     super().save(*args, **kwargs)