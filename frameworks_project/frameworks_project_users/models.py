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
        # Save the model only at the end to prevent multiple save calls
        # Resize the image before the first save call
        if self.image:
            # Open the image from storage (in-memory if using S3)
            img = Image.open(self.image)

            # Resize the image if it's larger than the desired size
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)

                # Save the resized image in-memory using BytesIO
                img_io = BytesIO()
                img_format = img.format if img.format else 'JPEG'  # Preserve the original format
                img.save(img_io, format=img_format)

                # Use the same file name and avoid re-appending "profile_pics/"
                self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)

        # Call save only once after the image is processed
        super().save(*args, **kwargs)