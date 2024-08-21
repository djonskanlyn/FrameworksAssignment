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
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        # Save the model first to ensure we have access to the image
        super().save(*args, **kwargs)

        # Check if an image exists
        if self.image:
            img = Image.open(self.image)  # Open the uploaded image file

            # Resize the image if necessary (e.g., if it's larger than 300x300)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)  # Resize the image while maintaining aspect ratio

                # Save the resized image to a BytesIO object (in memory)
                img_io = BytesIO()
                img_format = img.format if img.format else 'JPEG'  # Get the original format (e.g., JPEG, PNG)
                img.save(img_io, format=img_format)

                # Replace the image field with the resized image
                self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)

        # Call save again to save the resized image
        super().save(*args, **kwargs)