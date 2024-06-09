from django.views.generic import ListView
from ..models import ForumUser


class UsersListView(ListView):
    model = ForumUser
    template_name = "users.html"
    context_object_name = "my_users"
    paginate_by = 4

    def get_queryset(self):
        return ForumUser.objects.all()
