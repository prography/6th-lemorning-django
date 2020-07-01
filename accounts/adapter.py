from allauth.account.adapter import DefaultAccountAdapter
from .models import Account


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user_id = user.id
        sex = data.get('sex')
        profile = data.get('profile')
        nickname = data.get('nickname')
        birth = data.get('birth')
        account = Account.objects.create(user_id=user_id,
                                         sex=sex, profile=profile, nickname=nickname,
                                         birth=birth).save()
        user.save()
        return user
