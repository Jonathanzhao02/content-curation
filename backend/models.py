
import datetime
import logging
from hashlib import sha256

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import get_valid_filename
from django.contrib.auth.models import User

from backend.validators import validate_unique_filename
from backend.enums import STATUS


logger = logging.getLogger(__name__)


class MetadataType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Metadata(models.Model):
    # TODO: Make sure there are no metadata with the same type and the
    # same name when creating a new one
    name = models.CharField(max_length=500)
    type = models.ForeignKey(MetadataType, on_delete=models.CASCADE)

    def metadataType(self):
        return {
            "id": self.type.id,
            "name": self.type.name
        }

    def __str__(self):
        return f'[{self.type}]{self.name}'


class Content(models.Model):
    def set_file_name(self, file_name):
        # get file size if this content was saved individually
        if (self.content_file):
            self.hash = sha256(self.content_file.read()).hexdigest()
            self.filesize = self.content_file.size
            self.file_name = get_valid_filename(file_name)
        return file_name

    content_file = models.FileField(
        "File",
        upload_to=set_file_name,
        max_length=500,
        validators=[
            validate_unique_filename
        ])
    filesize = models.FloatField(null=True, editable=True)
    file_name = models.CharField(max_length=500, null=True)
    title = models.CharField(max_length=300)
    description = models.TextField(null=True)
    hash = models.CharField(max_length=128, null=True)
    # modified_on = models.DateTimeField(default=datetime.now)
    metadata = models.ManyToManyField(Metadata, blank=True)
    copyright_notes = models.TextField(null=True)
    rights_statement = models.TextField(null=True)
    additional_notes = models.TextField(null=True)
    published_date = models.DateField(default=None, null=True)
    # reviewed_on = models.DateField(null=True)
    active = models.BooleanField(default=1)
    # duplicatable = models.BooleanField(default=0)
    # Cataloger/Curator from loggedIn
    created_by = models.ForeignKey(
       User, default=None, null=True, on_delete=models.SET_DEFAULT,
    )
    created_on = models.DateField(default=datetime.date.today, null=True)
    # further modified by curators/metadataaides/library specialist(s)to edit the filename and metadata record
    modified_by = models.TextField(null=True)
    modified_on = models.DateField(default=datetime.date.today, null=True)
    # Sara Team -> Reviews it
    reviewed_by = models.TextField(null=True)
    reviewed_on = models.DateField(default=datetime.date.today, null=True)
    # CopyRight Permission for curator's content
    copyright_approved = models.BooleanField(default=1)
    copyright_by = models.TextField(null=True)
    copyright_on = models.DateField(default=datetime.date.today, null=True)
    copyright_site = models.TextField(null=True)
    original_source = models.TextField(null=True)
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default='Review',
    )

    def created_by_name(self):
        return self.created_by.username if self.created_by else ""

    def published_year(self):
        return None if self.published_date == None else str(
            self.published_date.year)

    def metadata_info(self):
        return [{
            "id": metadata.id,
            "name": metadata.name,
            "type_name": metadata.type.name,
            "type": metadata.type.id
        } for metadata in self.metadata.all()]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def num_content(self):
        return Content.objects.filter(created_by=self.user.id).count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
