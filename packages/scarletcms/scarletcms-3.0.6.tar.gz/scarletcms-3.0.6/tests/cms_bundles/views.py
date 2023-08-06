from scarlet.cms import views


class PostsListView(views.ListView):
    paginate_by = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
