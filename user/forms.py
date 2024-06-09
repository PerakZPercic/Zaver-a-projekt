from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ForumInvite, ForumUser
from django import forms


class ForumUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    invite_code = forms.CharField(max_length=64)

    def get_username(self):
        try:
            return self.cleaned_data.get("username")
        except:
            return ""

    def get_email(self):
        try:
            return self.cleaned_data.get("email")
        except:
            return ""

    def get_password1(self):
        try:
            return self.cleaned_data.get("password1")
        except:
            return ""

    def get_password2(self):
        try:
            return self.cleaned_data.get("password2")
        except:
            return ""

    def get_invite_code(self):
        try:
            return self.cleaned_data.get("invite_code")
        except:
            return ""

    def is_valid(self):
        super_valid = super().is_valid()
        if not super_valid:
            return False, 0

        # check if the provided email is already in use
        emails = ForumUser.objects.filter(email=self.get_email())
        if len(emails) >= 1:
            return False, 1

        # check if the provided invite is valid
        try:
            invite: ForumInvite = ForumInvite.objects.get(invitation_code=self.get_invite_code())
            invited_by_uid = invite.created_by

            creator: ForumUser = invite.get_creator()
            if creator is not None:
                creator.used_invites += 1
                creator.save()

            invite.delete()  # delete the invite record as we don't want multiple users, to use the same invite
        except:
            return False, 2

        return True, invited_by_uid

    def save(self, commit=True):
        pass

    class Meta(UserCreationForm.Meta):
        model = ForumUser
        fields = ("username",)


class ForumUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ForumUser
        fields = ("username",)


class ForumUserLoginForm(forms.Form):
    username = forms.CharField(max_length=32, min_length=3)
    password = forms.CharField(max_length=254, min_length=8)

    def get_username(self):
        try:
            return self.cleaned_data.get("username")
        except:
            return ""

    def get_password(self):
        try:
            return self.cleaned_data.get("password")
        except:
            return ""

    def is_valid(self):
        super().is_valid()

        try:
            user = ForumUser.objects.get(username=self.get_username())
        except:
            return False

        return True
