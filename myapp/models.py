from django.db import models

# Create your models here.
class User(models.Model):
    usertype = models.CharField(max_length=100, default="customer")
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    pswd = models.CharField(max_length=100)

    def __str__ (self):
        return self.fname+" - "+self.lname+" - "+self.usertype
    
class Watchs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    watchtype = models.CharField(max_length=100)
    w_image = models.ImageField(blank=True, null=True, upload_to='images/')
    w_brand = models.CharField(max_length=100)
    w_model = models.CharField(max_length=100)
    w_price = models.IntegerField()
    w_features = models.TextField(max_length=250)
    
    def __str__(self):
        return self.watchtype+" - "+self.w_brand+" - "+self.user.fname+" - "+self.user.lname
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watch = models.ForeignKey(Watchs, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.fname