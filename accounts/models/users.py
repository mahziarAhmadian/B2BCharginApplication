import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


# Create your models here.


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the uniqe identifiers for authentication instead od username.
    """

    def create_user(self, phone_number, password, **extra_fields):
        """
        create and save a user with the gven phone number and password and extra data .
        """
        if not phone_number:
            raise ValueError(_("The phone number  must be set"))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.is_common_user = True
        user.save()
        return user

    def create_seller(self, phone_number, password, **extra_fields):
        """
        create and save a seller with the gven phone number and password and extra data .
        """
        if not phone_number:
            raise ValueError(_("The phone number must be set"))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.is_seller = True
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        create and save a super user with the gven phone number and password and extra data .
        """
        if not phone_number:
            raise ValueError(_("The phone number must be set"))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User MMOdel for our app
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    phone_number = models.CharField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_common_user = models.BooleanField(default=False)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    created_date = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.phone_number
