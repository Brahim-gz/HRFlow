from django.db import models


class JobOffer(models.Model):
    job = models.CharField(max_length=150)
    description = models.TextField()
    selectionCriteria = models.TextField()
    datePub = models.DateField()
    city = models.CharField(max_length=150)
    class JobOfferCategory(models.TextChoices):
        ON_SITE = 'S', 'on-site'
        HYBRID = 'H', 'hybrid'
        REMOTE = 'R', 'remote'
    category = models.CharField(max_length=1, choices=JobOfferCategory.choices)
    class JobOfferType(models.TextChoices):
        CDI = 'CDI', 'cdi'
        CDD = 'CDD', 'cdd'
        INTERNSHIP = 'INT', 'internship'
    type = models.CharField(max_length=3, choices=JobOfferType.choices)

class User(models.Model):
    firstName = models.CharField(max_length=150)
    familyName = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=150)
    applications = models.ManyToManyField(JobOffer, through='Application')

class Dept(models.Model):
    dname = models.CharField(max_length=150)

class Message(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    date = models.DateField()
    checked = models.BooleanField(default=False)
    destination = models.ForeignKey(User, on_delete=models.CASCADE)

class Application(models.Model):
    date = models.DateField()
    address = models.CharField(max_length=150)
    birthdate = models.DateField()
    skills = models.TextField()
    tel = models.CharField(max_length=150)
    class ApplicationStatus(models.TextChoices):
        REJECTED = 'REJ', 'rejected'
        ACCEPTED = 'ACC', 'accepted'
        RECEIVED = 'REC', 'received'
        APPLIED = 'APP', 'applied'
        TechnicalTest = 'T.T', 'technical test'
        INTERVIEW = 'INT', 'interview'
    status = models.CharField(max_length=3, choices=ApplicationStatus.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jobOffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)

class Document(models.Model):
    class DocumentType(models.TextChoices):
        RESUME = 'R', 'resume'
        COVERLETTER = 'L', 'cover letter'
        OTHER = 'O', 'other'
    type = models.CharField(max_length=1, choices=DocumentType.choices)
    doc = models.FileField(upload_to='documents/%Y/%m/%d/')
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

class Trainning(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    startDate = models.DateField()
    duration = models.IntegerField()
    dept = models.ForeignKey(Dept, on_delete=models.RESTRICT)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=150)
    job = models.CharField(max_length=150)
    isHR = models.BooleanField(default=False)
    hireDate = models.DateField()
    absences = models.IntegerField(default=0)
    availableLeave = models.IntegerField(default=30)
    dept = models.ForeignKey(Dept, on_delete=models.RESTRICT)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    trainningParticipations = models.ManyToManyField(Trainning, related_name='participations')

class Leave(models.Model):
    class LeaveType(models.TextChoices):
        SICKNESS = 'S', 'sickness'
        RTT = 'R', 'rtt'
        PAYED = 'P', 'payed'
    type = models.CharField(max_length=1, choices=LeaveType.choices)
    startDate = models.DateField()
    endDate = models.DateField()
    justification = models.TextField()
    accepted = models.BooleanField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

class DocumentDemande(models.Model):
    class DocumentType(models.TextChoices):
        EMPLOYMENTCONTRACT = 'EC', 'employment contract'
        WORKCERTIFICATE = 'WC', 'work certificate'
        PAYSLIP = 'PS', 'payslip'
    type = models.CharField(max_length=2, choices=DocumentType.choices)
    justification = models.TextField()
    class SendingMode(models.TextChoices):
        EMAIL = 'E', 'email'
        SMS = 'S', 'sms'
        MESSAGE = 'M', 'message'
        PRINT = 'P', 'print'
    mode = models.CharField(max_length=1, choices=SendingMode.choices)
    sent = models.BooleanField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)