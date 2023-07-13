from django.db import models
class User(models.Model):
    '''用户表映射类,包括用户ID、昵称和密码属性
    '''
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)
    

class Userdetail(models.Model):
    '''用户详情表表映射类，包括属性
    '''
    birth_date = models.DateField(null=True)
    email= models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    profile = models.TextField()
    User=models.OneToOneField('User', on_delete=models.CASCADE)
