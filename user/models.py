from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.db import models
import uuid


class ForumInvite(models.Model):
    invitation_code = models.CharField(max_length=64, default=uuid.uuid4)
    created_by = models.IntegerField(default=0)

    def get_creator(self):
        try:
            return ForumUser.objects.get(id=self.created_by)
        except:
            return None

    def get_creator_name(self):
        user: ForumUser = self.get_creator()
        if user is None:
            return "*Unknown*"

        return user.username

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if force_update or update_fields:
            super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
            return

        try:
            inv = ForumInvite.objects.get(invitation_code=self.invitation_code)
        except:
            user: ForumUser = self.get_creator()
            if user is not None:
                user.created_invites += 1
                user.save()

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        user: ForumUser = None
        try:
            user = ForumUser.objects.get(id=self.created_by)
        except:
            pass

        parts = str(self.invitation_code).split("-")
        parts[0] = "*" * len(parts[0])

        inv_code: str = ""
        if len(parts) == 5:
            parts[2] = "*" * len(parts[2])

        for i in range(len(parts)):
            if i >= (len(parts) - 1):
                inv_code += f"{parts[i]}"
            else:
                inv_code += f"{parts[i]}-"

        return f"{inv_code} by {user is None and '*Unknown*' or user.username}"


class ForumUserManager(BaseUserManager):
    def create_user(self, username, email, password, invited_by, **extra_fields):
        if not username:
            raise ValueError("Username must be set")

        email = self.normalize_email(email)
        user: AbstractBaseUser = self.model(username=username, email=email, invited_by=invited_by, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, email, password, 0, **extra_fields)


class ForumUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(default="default@ema.il")
    hasVerifiedEmail = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # invite stuff
    invite_created_by_user = models.ForeignKey(ForumInvite, on_delete=models.SET_NULL, default=None, null=True)
    invited_by = models.IntegerField(default=0)
    created_invites = models.IntegerField(default=0)
    used_invites = models.IntegerField(default=0)

    # default stuff
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Ban stuff
    is_banned = models.BooleanField(default=False)
    banned_until = models.DateTimeField(default=timezone.now)
    ban_message = models.CharField(max_length=500, default="")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = ForumUserManager()

    def __str__(self):
        return self is None and "" or f"{self.username} ({self.id}), banned: {self.is_banned}"
