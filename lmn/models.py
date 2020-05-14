from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
import datetime

# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

#Require email, first name and last name
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False


''' A music artist '''
class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True) # Change artist to unique

    def __str__(self):
        return "Artist: " + self.name


''' A venue, that hosts shows. '''
class Venue(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=20, blank=False)  # What about international?

    def __str__(self):
        return 'Venue name: {} in {}, {}'.format(self.name, self.city, self.state)


''' A show - one artist playing at one venue at a particular date. '''
class Show(models.Model):
    show_date = models.DateTimeField(blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Show with artist {} at {} on {}'.format(self.artist, self.venue, self.show_date)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(show=self)
        return len(ratings)

''' One user's opinion of one show. '''
class Note(models.Model):
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(blank=False, auto_now=True)

    def publish(self):
        posted_date = datetime.datetime.today()
        self.save()

    def __str__(self):
        return 'Note for user ID {} for show ID {} with title {} text {} posted on {}'.format(self.user, self.show, self.title, self.text, self.posted_date)

''' A users profile. '''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # Fields for more profile information here
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    fav_band = models.TextField(max_length=50, blank=True, null=True)
    insta_username = models.TextField(max_length=30, blank=True, null=True)
    youtube_username = models.TextField(max_length=30, blank=True, null=True)
    twitch_username = models.TextField(max_length=30, blank=True, null=True)
    snap_username = models.TextField(max_length=20, blank=True, null=True)
    

    def __str__(self):
        return '{} Profile'.format(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_img.path)

        # Modify profile picture size to thumbnail size
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_img.path)

''' Ratings for shows '''
class Rating(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),
    MaxValueValidator(5)])

    ''' Allows only one show rating for one specific user '''    
    class Meta:
        unique_together = (('user', 'show'),)
        index_together = (('user', 'show'),)

    def __str__(self):
        return '{} Rating'.format(self.stars)

  
