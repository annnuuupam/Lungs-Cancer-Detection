from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(primary_key=True,max_length=30)
    password=models.CharField(max_length=10,null=False)
    name=models.CharField(max_length=30,null=False)
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
    fathers_name=models.CharField(max_length=30,default='')
    mothers_name=models.CharField(max_length=30,default='')
    phone=models.CharField(max_length=10,default='')
    email=models.CharField(max_length=30,default='')
    address=models.CharField(max_length=50,default='')
    def __str__(self):
        return self.fathers_name
    
    
class Test_history(models.Model):
    test_id=models.BigAutoField(auto_created=True,primary_key=True)
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=25,default='')
    total=models.IntegerField()
    correct=models.IntegerField()
    wrong=models.IntegerField()
    percentage=models.IntegerField()

class Test_paper_subject1(models.Model):
    q_id=models.IntegerField(primary_key=True)
    ques=models.CharField(max_length=100)
    a=models.CharField(max_length=50)
    b=models.CharField(max_length=50)
    c=models.CharField(max_length=50)
    d=models.CharField(max_length=50)
    ans=models.CharField(max_length=2)
    def __str__(self):
        return self.ques
    
class Test_paper_subject2(models.Model):
    q_id=models.IntegerField(primary_key=True)
    ques=models.CharField(max_length=100)
    a=models.CharField(max_length=50)
    b=models.CharField(max_length=50)
    c=models.CharField(max_length=50)
    d=models.CharField(max_length=50)
    ans=models.CharField(max_length=2)
    def __str__(self):
        return self.ques
    
class Test_paper_subject3(models.Model):
    q_id=models.IntegerField(primary_key=True)
    ques=models.CharField(max_length=100)
    a=models.CharField(max_length=50)
    b=models.CharField(max_length=50)
    c=models.CharField(max_length=50)
    d=models.CharField(max_length=50)
    ans=models.CharField(max_length=2)
    def __str__(self):
        return self.ques
    
class Payment(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    order_id = models.CharField(max_length=100, unique=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    