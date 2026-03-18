from django.db import models

# Create your models here.
class Member(models.Model):
    fname=models.CharField(max_length=255)  #python manage.py sqlmigrate Myapp 0001
    lname=models.CharField(max_length=255)  #[BEGIN;Create model member--CREATE TABLE "Myapp_member"
                                            #("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
                                            #"fname" varchar(255) NOT NULL,"lname" varchar(255) NOT NULL);COMMIT;]
    phone=models.IntegerField(null=True)    #python manage.py sqlmigrate Myapp 0002
    join_date=models.DateField(null=True)   #[BEGIN;---- Add field join_date to member--ALTER TABLE "Myapp_member" 
                                            #ADD COLUMN "join_date" date NULL;---- Add field phone to member--
                                            #ALTER TABLE "Myapp_member" ADD COLUMN "phone" integer NULL;COMMIT;
    email=models.EmailField(null=True)     #python manage.py sqlmigrate Myapp 0003
                                            #[BEGIN;---- Add field email to member--ALTER TABLE "Myapp_member" ADD COLUMN "email" varchar(254) NULL;COMMIT;]
    address=models.CharField(max_length=255, null=True)  #python manage.py sqlmigrate Myapp 0004
                                            #[BEGIN;---- Add field address to member--ALTER TABLE "Myapp_member" ADD COLUMN "address" varchar(255) NULL;COMMIT;]
    image=models.ImageField(upload_to='images/',default='RINKU.jpg',blank=True, null=True)  #python manage.py sqlmigrate Myapp 0005
                                            #[BEGIN;---- Add field image to member--ALTER TABLE "Myapp_member" ADD COLUMN "image" varchar(100) NULL;COMMIT;]
    file=models.FileField(upload_to='files/', null=True)  #python manage.py sqlmigrate Myapp 0006
                                            #[BEGIN;---- Add field file to member--ALTER TABLE "Myapp_member" ADD COLUMN "file" varchar(100) NULL;COMMIT;]
    
    
    def __str__(self):
        return f"{self.fname} {self.lname}"