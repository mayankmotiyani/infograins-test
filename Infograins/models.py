from ast import Num
from cgitb import text
from email.policy import default
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from phone_field import PhoneField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class Blog(models.Model):
    blog_image = models.ImageField(upload_to='media',default='')
    blog_title = models.CharField(max_length=80,default='')
    blog_para  = RichTextUploadingField(default='')
    blog_date  = models.DateField(auto_now=True)
    blog_slug = models.SlugField(blank = True)
    
    def __str__(self):
        return self.blog_title
    
    def save(self, *args, **kwargs):
        self.blog_slug = slugify(self.blog_title)
        super(Blog, self).save(*args, **kwargs)
       
class Technology(models.Model):
    title = models.CharField(max_length=80,default='' )
    image = models.ImageField(null=True, blank = True, upload_to='media', default = '')
    description = models.TextField((""))
    conten  = RichTextUploadingField(default='')
    slug = models.SlugField(blank=True)
    
    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Technology, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("products_slug", kwargs={"product_id": self.slug})
    
    
    
class Product(models.Model):
    Technology = models.ForeignKey('Technology', on_delete=models.CASCADE, null=True, related_name='product')   
    productname = models.CharField(max_length=80,default='')
    product_image = models.ImageField(blank = True, null= True, upload_to='media', default = '')
    product_logo_image = models.ImageField(blank = True, null= True, upload_to='media', default = '')
    product_paragraph  = RichTextUploadingField(default='')
    product_date  = models.DateField(auto_now=True)
    product_slug = models.SlugField(blank = True)
    product_description = models.TextField((""))
    
    def __str__(self):
        return f' {self.productname}'
    
    def save(self, *args, **kwargs):
        self.product_slug = slugify(self.productname)
        super(Product, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("product_technology", kwargs={"technology_id": self.Technology.slug,"product_id": self.product_slug})
    

    @property
    def sd(self):
        return {
            "@type": 'Product',
            "description": self.product_slug,
            "name": self.product_title,
        }

class Resource(models.Model):
    resource_title = models.CharField(max_length=100,default='')
    resource_para  = RichTextUploadingField(default='')
    resource_img = models.ImageField(blank = True, null= True, upload_to='media', default = '')
    resource_date  = models.DateField(auto_now=True)
    resource_slug = models.SlugField(blank = True)
    def __str__(self):
        return self.resource_title
    
    def save(self, *args, **kwargs):
        self.resource_slug = slugify(self.resource_title)
        super(Resource, self).save(*args, **kwargs)
    
class Service(models.Model):
    service_title = models.CharField(max_length=100,default='')
    service_category = models.CharField(max_length=80,default='')
    service_img = models.ImageField(blank = True, null= True, upload_to='media', default = '')
    service_para  = RichTextUploadingField(default='')
    service_date  = models.DateField(auto_now=True)
    service_slug = models.SlugField(blank = True)

    def save(self, *args, **kwargs):
        self.service_slug = slugify(self.service_title)
        super(Service, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/{self.service_slug}/'

    def __str__(self):
        return f'{self.service_title}, -> {self.service_category} -------- {self.service_slug}'

    

class Contact(models.Model):
    contact_name = models.CharField(max_length=50,default='')
    contact_email  =  models.EmailField(max_length=100,default='')
    contact_subj  = models.CharField(max_length=200,default='')
    contact_msg  = models.TextField(max_length=1000,default='')

    def __str__(self):
        return self.contact_name
    
    

class BlockChain(models.Model):
    service_title = models.CharField(max_length=100,default='')
    service_para  = RichTextUploadingField(default='')
    service_date  = models.DateField(auto_now=True)
    service_slug = models.SlugField(blank = True)
    
    
   

    def save(self, *args, **kwargs):
        self.service_slug = slugify(self.service_title)
        super(BlockChain, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.service_title}'

class Events(models.Model):
    user_name = models.CharField(max_length=50,default='')
    user_email  =  models.EmailField(max_length=100,default='')
    subj  = models.CharField(max_length=200,default='')
    contact_msg  = models.TextField(max_length=1000,default='')

class Franchise(models.Model):
    first_name = models.CharField(max_length=50,default='',null=True,blank=True)
    last_name = models.CharField(max_length=50, default='',null=True,blank=True)
    email = models.EmailField(max_length=100,default='',null=True,blank=True)
    contact =PhoneField(blank=False ,help_text='Contact number', null=True)
    address = models.TextField(null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True,default="")
    city = models.CharField(max_length=50,default='',null=True,blank=True)
    source = models.CharField(max_length=50,default='',null=True,blank=True)
    specify=models.TextField(default='',null=True,blank=True)
    notes = models.TextField(default='',null=True,blank=True)

    def __str__(self):
        return f'First : {self.first_name} -- City : {self.city} -- Lead Comes From : {self.source}'



class Career(models.Model):
    job_title = models.CharField(max_length=100,default='',null=True,blank=True)
    opening = models.IntegerField()
    experience_in_years = models.CharField(max_length=50,null=True,blank=True,default="")
    location = models.CharField(max_length=50,null=True,blank=True,default="")
    join_duration_days = models.IntegerField()
    job_description = models.TextField(null=True,blank=True)
    Available = models.BooleanField(default=False)
    

    def __str__(self):
        return f'Job title : {self.job_title}'
    
    def save(self,*args,**kwargs):
        if self.opening <= 0:
            self.Available = False
        else:
            self.Available = True   
        return super().save(*args,**kwargs)
    
    
    
    
    
class Apply_job(models.Model):
    first_name = models.CharField(max_length=50,default='',null=True,blank=True)
    last_name = models.CharField(max_length=50, default='',null=True,blank=True)
    email = models.EmailField(max_length=100,default='',null=True,blank=True)
    contact =PhoneField(blank=False ,help_text='Contact number', null=True)
    address = models.TextField(null=True,blank=True)
    position_applying_for = models.CharField(max_length=100, default='')
    skills = models.TextField(null=True,blank=True)
    experience = models.CharField(max_length=50,default='',null=True,blank=True)
    Resume = models.FileField(upload_to='pdfs/')
    source = models.CharField(max_length=50,default='',null=True,blank=True)
    specify=models.TextField(default='',null=True,blank=True)

    

    def __str__(self): return f'  {self.first_name}'
    
    
class Mtag(models.Model):
    Block = models.OneToOneField(BlockChain, on_delete=models.CASCADE, related_name='mtags')
    service_tag = models.TextField()
    service_title = models.CharField(max_length=200,blank=True,null=True)
    
    
    def __str__(self) : 
        return f' block : {self.Block}'

    def save(self,*args,**kwargs):
        self.service_title = self.Block.service_slug
        super(Mtag,self).save(*args,**kwargs)
    
    # def update(self,*args,**kwargs):
    #     super(Mtag,self).update(*args, **kwargs)




class Team(models.Model):
    name = models.CharField(max_length=60,default='',null=True,blank=True)
    designation = models.TextField(null=True,blank=True)
    description = models.TextField(default='',null=True,blank=True)
    image = models.ImageField(blank = True, null= True, upload_to='media', default = '')

    def __str__(self) : 
        return  f'{self.name}'


class Crypto(models.Model):
    title = models.CharField(max_length=100, default='')
    Crypto_img = models.ImageField(blank = True, null= True, upload_to='media', default = '')
    para = RichTextUploadingField(default='')
    slug = models.SlugField(blank= True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Crypto, self).save(*args, **kwargs)

 


   
class NFT(models.Model):
    title = models.CharField(max_length=100,default='')   
    img = models.ImageField(blank = True, null= True, upload_to='media', default = '')
    para = RichTextUploadingField(default='')

    slug = models.SlugField(blank = True)
    
    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(NFT, self).save(*args, **kwargs)
    


class ProductSchema(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_schema')
    rating_value = models.FloatField(blank=True,null=True)
    rating_count = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.product.product_title} -ratingValue : {self.rating_value} -ratingValue : {self.rating_count}"

class Fork_Title(models.Model):
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(blank = True)


    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Fork_Title, self).save(*args, **kwargs)



class Fork(models.Model):
    fork_block = models.ForeignKey(Fork_Title, on_delete=models.CASCADE)
    fork_name = models.CharField(max_length=100, default='') 
    fork_img = models.ImageField(blank = True, null= True, upload_to='media', default = '')
    
    def __str__(self):
        return f'{self.fork_name}'


class Fork_Form(models.Model):
    name = models.CharField(max_length = 150,default='')
    email = models.EmailField(max_length=100,default='',null=True,blank=True)
    contact = PhoneField(blank=False ,help_text='Contact number', null=True)
    skype_id = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=20,default='')
    demo_for = models.CharField(max_length=100,default='')
    message = models.TextField(default='',null=True,blank=True)

    
    def __str__(self):
        return f'{self.name }'



class ServicesSchema(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name='service_schema')
    rating_value = models.FloatField(blank=True,null=True)
    rating_count = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.product.service_title} -ratingValue : {self.rating_value} -ratingValue : {self.rating_count}"

class BlockchainSchemas(models.Model):
    blockchain = models.ForeignKey('BlockChain', on_delete=models.CASCADE, related_name='blockchain_schema')
    rating_value = models.FloatField(blank=True,null=True)
    rating_count = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.product.service_title} -ratingValue : {self.rating_value} -ratingValue : {self.rating_count}"