from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    
    phone = models.CharField(
        null=True, blank=True,
        max_length= 100
    )
    
    @property
    def username(self):
        return self.user.username

    @property
    def last_name(self):
        return self.user.first_name

    @property
    def first_name(self):
        return self.user.last_name
    
    @property
    def email(self):
        return self.user.email
    
    class Meta:
        abstract = True
    
class Event(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    
    class Meta:
        abstract = True    
    
    
class Client(Persona):
    user = models.OneToOneField(
        User, 
        related_name="client",
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.username
    
    

class Place(Persona):
    user = models.OneToOneField(
        User, 
        related_name="place",
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=150,
        null=False, blank=False
    )
    address = models.CharField(
        max_length=500,
        null=False, blank=False
    )
    about = models.TextField(
    )
    
    def __str__(self):
        return self.name
    # TODO : GET STARS
    
class Unit(models.Model):
    place = models.ForeignKey(
        Place, related_name="units",
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=150
    )
    about = models.TextField(
    )
    pax = models.PositiveSmallIntegerField(
        blank=True, null=True
    )
    value = models.PositiveIntegerField(
        blank=True, null=True
    )
    
    def __str__(self):
        return f'{self.place} {self.title}'
    
class Reservation(Event):
        
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    
    check_in = models.DateField()
    check_out = models.DateField()
    
    total = models.PositiveIntegerField(
        null=True, blank=True
    )
    
    is_paid = models.BooleanField(
        default=False,
    )
    # TODO: 
    #       get is_paid in base of sum of related Pay instances
    #       get total in base of value of Unit and amount of days between chekc in and chekcout      
    #       make dates validation
    
    def __str__(self):
        return f'{self.client} {self.unit.place} {self.unit.title} {self.check_in}' 
    
class Pay(Event):
    METHOD_CHOICES = [
        ('CASH', 'CASH'),
        ('MP', 'MP'),
        ('BT', 'BT'),
        ('OTHER', 'OTHER'),
    ]
    method= models.CharField(
        choices=METHOD_CHOICES,
        max_length=50,
        blank=True,null=True

        )
    amount = models.PositiveIntegerField()
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.SET_NULL,
        blank=True,null=True
    )
    
    def __str__(self):
        return f'{self.reservation} ${self.amount} paid'

class Review(Event):
    STARS_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    stars= models.CharField(
        choices=STARS_CHOICES,
        max_length=2,
        )
    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        blank=True,null=True,
        related_name="reviews"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        blank=True,null=True,
        related_name="reviews"
    )
        
    
    def __str__(self):
        return f'{self.place} {self.stars}'
    
    class Meta:
        unique_together = ['client', 'place']