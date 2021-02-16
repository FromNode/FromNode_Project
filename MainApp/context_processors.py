from ProjectApp.models import Projects

def project_list(request):
    if request.user.is_authenticated:
        User = request.user
        unliked_proj = User.Joined_Unliked_Projects.all()
        liked_proj = User.Joined_Liked_Projects.all()
        all_proj = unliked_proj | liked_proj
        profile_img_url = User.Profile.profile_image.url
        username = User.Profile.nickname
        return {'proj_obj_all':all_proj,
                'profile_img_url':profile_img_url,
                'username':username}
    # else:
    #     return {'proj_obj_all':'none',
    #             'profile_img_url':''}