from django.db import models

# Create your models here.

class employee(models.Model):
    PIN = models.CharField(max_length=100, unique=True,default='abc')
    full_name = models.CharField(max_length=100,null=False,default='abc')
    Primary_PhoneNum = models.IntegerField(default=0)
    Alternative_Phonenum = models.IntegerField(default=0)
    Email_Id=models.EmailField(max_length=150,default='abc@gmail.com')
    profession=models.CharField(max_length=150,default=0)
    Location=models.CharField(max_length=150,default=0)
    
   

    def save(self, *args, **kwargs):
        if not self.PIN:  
            last_system = employee.objects.order_by('PIN').first()
            if last_system:
                last_code = last_system.PIN[3:]  
                new_code = f'SYS{int(last_code) + 1:03d}'  
            else:
                new_code = 'SYS001'
            self.PIN = new_code

 

        super().save(*args, **kwargs)