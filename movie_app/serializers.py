from rest_framework import serializers
from .models import Movie, Director, Review
from rest_framework.exceptions import ValidationError

class DirectorSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = Director
        fields = ' id name count'.split()

    def get_count(self, director):
        movies = director.movies.all()
        return movies.count()


# class DirectorDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Director
#         fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text star'.split()


# class ReviewDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    avg_rating = serializers.SerializerMethodField()
    # director = serializers.SerializerMethodField
    class Meta:
        model = Movie
        fields = 'title duration director_name reviews avg_rating'.split()
        # depth = 1

    def get_avg_rating(self, movie):
        reviewss = movie.reviews.all()
        if reviewss:
            sum_reviews = sum(i.star for i in reviewss)
            average_review = round(sum_reviews / len(reviewss), 1)
            return average_review
        else:
            return 0


    # def get_directories(self, movie):
    #     list_=[]
    #     for directory in movie.directories.all():
    #         list_.append(directory.name)
    #         return list_

# class MovieDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = '__all__'



class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    description = serializers.CharField()
    duration = serializers.FloatField(min_value=2)
    director_id = serializers.IntegerField(min_value=1)

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director not found')
        return director_id

class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)



class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    star = serializers.IntegerField(min_value=1, max_value=5)
    movie_id = serializers.IntegerField(min_value=1)

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except Director.DoesNotExist:
            raise ValidationError('Movie not found')
        return movie_id