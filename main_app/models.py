from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime,timedelta




class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class Session(models.Model):
    name = models.CharField(max_length=20)
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return self.name

class SessionTerm(models.Model):

    CHOICE = [
        ('First Term', 'First Term'),
        ('Second Term', 'Second Term'),
        ('Third Term', 'Third Term')
    ]
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    term = models.CharField(max_length=15, unique=True, choices=CHOICE)

    TERM_CHOICES = [("Term 1", "Term 1"), ("Term 2", "Term 2"), ("Term 3", "Term 3")]
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, choices=TERM_CHOICES)


    def __str__(self):
        return self.term

class CustomUser(AbstractUser):
    USER_TYPE = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    GENDER = [("M", "Male"), ("F", "Female")]
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return  self.first_name + " " + self.last_name


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


#Create a class for the branches (school)
class Branch(models.Model):
    branch_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    address= models.CharField(max_length=100)

    def __str__(self):
        return self.name
  

#Newly added models are here=================
class ClassCategory(models.Model):
    name = models.CharField(max_length=100)
    target_scores = models.ManyToManyField(SessionTerm, through='CategoryTargetScore')

    def __str__(self):
        return self.name


class CategoryTargetScore(models.Model):
    class_category = models.ForeignKey(ClassCategory, on_delete=models.CASCADE)
    term = models.ForeignKey(SessionTerm, on_delete=models.CASCADE)
    target_score = models.DecimalField(max_digits=5, decimal_places=2)


    def __str__(self):
        return f'{self.class_category} - {self.term} - {self.target_score}'

class Classes(models.Model):
    class_id = models.AutoField(primary_key=True )
    category = models.ForeignKey(ClassCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('branch','name')

    def __str__(self):
        return f'{self.name} {self.branch}'


class Staff(models.Model):
    class_name = models.ForeignKey(Classes, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Assign Class')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.first_name + " " +  self.admin.last_name
    
class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    created_at = models.DateField(auto_now=True)
    exam_date = models.DateField()
    name = models.CharField(max_length=50, unique=True)
    target_marks = models.ForeignKey(CategoryTargetScore, on_delete=models.DO_NOTHING)
    # teacher = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    term = models.ForeignKey(SessionTerm, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.term} {self.name}-Session: {self.session}'    

class Stream(models.Model):
    stream_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name='class')
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.class_id} {self.name}'

class Subject(models.Model):
    name = models.CharField(max_length=120)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher} {self.subject} {self.stream}'

class ExamMeanResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    exam =models.ForeignKey(Exam, on_delete=models.DO_NOTHING, null=True, verbose_name='Exam Name')
    subject = models.ForeignKey(TeacherSubject, on_delete=models.DO_NOTHING)
    score = models.IntegerField()
    created = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('exam', 'subject')

    def __str__(self):
        return f'{self.exam} - {self.subject} - {self.score}'

#performance tables 
class TeacherPerformance(models.Model):
    teacher_subject = models.ForeignKey(TeacherSubject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    term = models.ForeignKey(SessionTerm, on_delete=models.CASCADE)
    year = models.ForeignKey(Session, on_delete=models.CASCADE)
    mean_marks = models.ForeignKey(ExamMeanResult, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher_subject}, {self.exam} {self.mean_marks}'


class ClassPerformance(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    term = models.ForeignKey(SessionTerm, on_delete=models.CASCADE)
    year = models.ForeignKey(Session, on_delete=models.CASCADE)
    mean_marks = models.DecimalField(max_digits=5, decimal_places=2)


class StreamPerformance(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    term = models.ForeignKey(SessionTerm, on_delete=models.CASCADE)
    year = models.ForeignKey(Session, on_delete=models.CASCADE)
    mean_marks = models.DecimalField(max_digits=5, decimal_places=2)


class SchoolPerformance(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    term = models.ForeignKey(SessionTerm, on_delete=models.CASCADE)
    year = models.ForeignKey(Session, on_delete=models.CASCADE)
    mean_marks = models.DecimalField(max_digits=5, decimal_places=2)

#End of newly added models =============/////==========

class FeedbackStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()

# todos
