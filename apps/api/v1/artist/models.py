from django.db import models
from django_countries.fields import CountryField
from treebeard.mp_tree import MP_Node


GENDER_CHOICES = (
    ('he/him', 'he/him'),
    ('she/her', 'she/her'),
    ('he/him', 'he/him'),
    ('they/them', 'they/them'),
    ('custom', 'custom'),
    ('they/them', 'they/them'),
)

class Artist(MP_Node):
    uuid = models.CharField( 
        db_index=True,
        max_length=25,
        unique=True
    )
    name = models.CharField(
        db_index=True,
        max_length=20, 
        unique=True, 
        blank=False, 
        null=False,
        help_text='Enter stage name'
    )
    first_name = models.CharField(
        max_length=25, 
        unique=True, 
        blank=False, 
        null=False,
        help_text='Enter first name'
    )
    last_name = models.CharField(
        max_length=45, 
        unique=True, 
        blank=False, 
        null=False,
        help_text='Enter last name'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES, 
        help_text='Select your gender from the list'
    )
    country = CountryField(
        db_index=True,
        max_length=20,
        blank=False,
        null=False,
        help_text='Enter country'
    )
    dob = models.DateField(
        max_length=8,
        help_text='Enter date of brith'
    )
    avatar = models.ImageField(
        db_index=True,
        upload_to='media/artist/avatar/',
        blank=True,
        null=True,
        help_text='Upload your desired profile avatar'
    )
    baner = models.ImageField(
        db_index=True,
        upload_to='media/artist/baner/',
        blank=True,
        null=True,
        help_text='Upload your desired profile baner'
    )
    email = models.EmailField(
        unique=True,
        help_text='Enter email'
    )
    # password = models.CharField(
    #     max_length=150,
    #     null=False, 
    #     blank=False
    # )
    followers = models.IntegerField(db_index=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'artist'
        verbose_name = 'Artist'
        verbose_name_plural = "Artists"