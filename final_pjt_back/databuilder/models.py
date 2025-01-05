from django.db import models

# Create your models here.
class Card(models.Model):
    card_company = models.TextField()
    card_type = models.CharField(max_length=50)
    card_name = models.CharField(max_length=50)
    card_url = models.URLField(blank=True, null=True)
    card_img = models.TextField(blank=True, null=True)
    card_benefits_category = models.TextField()
    card_benefits = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.card_name
    
    

    
    
