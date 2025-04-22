from django.db import models
import uuid
from django.utils import timezone



CATEGORY_CHOICES = (
    ('student', 'Student'),
    ('professional', 'Professional'),
)


CATEGORY_CHOICES_MEALS = (('veg', 'Veg'),
                          ('non-veg', 'Non-veg'))


CATEGORY_CHOICES_ABOUT_US = (('email','Email'),
                             ('website','Website'),
                             ('social media','Social media'),
                             ('collage','Collage'),
                             ('other','Other')
                             )



class Payment(models.Model):

    full_name = models.CharField(max_length=200)

    success =  models.BooleanField(default=False)

    email = models.EmailField()

    contact = models.CharField(max_length=10,blank=False)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
        
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    transcation_id = models.CharField(max_length=200,
                                      blank=True)
    
    bank_transaction_id = models.CharField(max_length=100, blank=True, null=True)

    
    organisation_name = models.CharField(max_length=200,blank=True)

    job_title = models.CharField(max_length=200,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    meals = models.CharField(max_length=20,choices=CATEGORY_CHOICES_MEALS)

    whatsapp_number = models.CharField(max_length=10,blank=True)

    additional_comments = models.CharField(blank=True,default=" ",max_length=500)

    about_us = models.CharField(max_length=30,choices=CATEGORY_CHOICES_ABOUT_US)





    def save(self, *args, **kwargs):
        if self.category == 'student':
            self.amount = 1
        elif self.category == 'professional':
            self.amount = 2
        super().save(*args, **kwargs)



