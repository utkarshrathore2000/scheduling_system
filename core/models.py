from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def get_by_natural_key(self, username):
        case_insensitive_username_field = f"{self.model.USERNAME_FIELD}__exact"
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, email=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(email=self.normalize_email(email), )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email=email, password=password, )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_staffuser(email=email, password=password, )
        user.email = email
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.user_type = 'admin'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=255,  null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=255,  null=True, blank=True)
    last_name = models.CharField(max_length=255,  null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_register = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(_('password'), max_length=128, null=True)
    user_number = models.CharField(max_length=255, null=True, blank=True)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
    address = models.CharField(max_length=500, null=True, blank=True)


    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"user:- {self.pk}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
