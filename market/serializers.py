from core.serializers import CurrentUserSerialiser
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from rest_framework import serializers

from .models import CarModel, Favorites, Post, PostImage

class ThumbnailSerializer(serializers.ImageField):
    def __init__(self, alias, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_only = True
        self.alias = alias

    def to_representation(self, value):
        if not value:
            return None

        url = thumbnail_url(value, self.alias)
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url

class PostImage_serializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_image_url')
    image = ThumbnailSerializer(alias='feed_thumbnail')
    class Meta:
        model = PostImage
        fields = ['url','image'] 
    
    def get_image_url(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(obj.image.url)

class CarModel_serializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id','make','model'] 

class Post_serializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    carmodel_id = serializers.IntegerField(write_only=True,required=False)
    carmodel = CarModel_serializer(read_only=True)
    postimage = serializers.ListField(child=serializers.ImageField(),write_only=True)
    images = PostImage_serializer(source="postimage_set",many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    class Meta:
        model = Post
        fields = ['id','title','type', 'description', 'price','displacement','mileage','color','body_type','location','registration_date','fuel_type','transmission', 'owner_phone','carmodel_id','carmodel','user_id','postimage','images','created_at'] 
    
    def create(self,validated_data):
        images = validated_data.pop('postimage')
        user_id = self.context['user_id']
        post = Post.objects.create(user_id=user_id, **validated_data)
        post.save()

        #PostImage.objects.create(post=post, image=images)
        PostImage.objects.bulk_create([PostImage(post=post,image=i) for i in images])

        return post 
    
    
class PostDetail_serializer(serializers.ModelSerializer):
    carmodel_id = serializers.IntegerField()
    user = CurrentUserSerialiser()
    class Meta:
        model = Post
        fields = ['id','title','type', 'description', 'price','displacement','color','body_type','location','registration_date','fuel_type','transmission', 'owner_phone','carmodel_id','user'] 



class Favorite_serializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    post = Post_serializer(read_only=True)
    class Meta:
        model = Favorites
        fields = ['id','user_id', 'post'] 

class Add_Favorite_serializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()
    class Meta:
        model = Favorites
        fields = ['id', 'post_id'] 

    def create(self, validated_data):
        user_id = self.context['user_id']
        (post,created) = Favorites.objects.get_or_create(user_id=user_id, **self.validated_data)
        #post.save()
        return post


