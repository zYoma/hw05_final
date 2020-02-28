from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("group/<str:slug>/", views.GroupPosts.as_view(), name="group_posts"),
    path("new/", views.NewPost.as_view(), name="new_post"),
    path("follow/", views.FollowIndex.as_view(), name="follow_index"),
    path("<username>/", views.Profile.as_view(), name="profile"),
    path("<username>/<int:post_id>/", views.PostView.as_view(), name="post"),
    path("<username>/<int:post_id>/edit/", views.PostEdit.as_view(), name="post_edit"),
    path("404/", views.page_not_found),
    path("500/", views.server_error),
    path("<username>/<int:post_id>/comment", views.AddComment.as_view(), name="add_comment"),
    path("<username>/follow", views.ProfileFollow.as_view(), name="profile_follow"), 
    path("<username>/unfollow", views.ProfileUnfollow.as_view(), name="profile_unfollow"),
]