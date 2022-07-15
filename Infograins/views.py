from django.shortcuts import render
from Infograins.models import Blog, Product, Resource, Service, Contact, BlockChain, Franchise, Career, Apply_job, Mtag, Team, Crypto, NFT, ProductSchema, Fork_Title, Fork, Fork_Form, ServicesSchema, Technology
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from Infograins_site.settings import EMAIL_HOST_USER
import requests
from django.conf import settings
from django.http import JsonResponse , HttpResponse
from django.template.loader import render_to_string
from socket import timeout
from django.shortcuts import redirect, render
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django_pandas.io import read_frame
import pandas as pd
import json
from django.views import generic
from countryinfo import CountryInfo

from Infograins_site.util import build_absolute_uri


DEFAULT_STRUCTURED_DATA = {}
if settings.DEFAULT_CONTEXT:
    DEFAULT_STRUCTURED_DATA["@context"] = settings.DEFAULT_CONTEXT
if settings.DEFAULT_TYPE:
    DEFAULT_STRUCTURED_DATA["@type"] = settings.DEFAULT_TYPE


class JsonLdContextMixin(object):
    """
    CBV mixin which sets structured data within the view's context
    """
    structured_data = None

    def __init__(self):
        super(JsonLdContextMixin, self).__init__()

        if not self.structured_data:
            self.structured_data = {}

        if '@graph' in self.structured_data:  # list of nodes
            instance_structured_data = {}
            if settings.DEFAULT_CONTEXT:
                instance_structured_data["@context"] = settings.DEFAULT_CONTEXT
            graph = []
            for item in self.structured_data["@graph"]:  # update items with defaults
                item_structured_data = DEFAULT_STRUCTURED_DATA.copy()
                item_structured_data.update(item)
                graph.append(item_structured_data)
            self.structured_data["@graph"] = graph
        else:
            instance_structured_data = DEFAULT_STRUCTURED_DATA.copy()

        instance_structured_data.update(self.structured_data)
        self.structured_data = instance_structured_data

    def get_structured_data(self):
        if settings.GENERATE_URL and "url" not in self.structured_data and "@graph" not in self.structured_data:
            self.structured_data["url"] = build_absolute_uri(self.request)
        return self.structured_data.copy()

    def get_context_data(self, **kwargs):
        context = super(JsonLdContextMixin, self).get_context_data(**kwargs)
        context[settings.CONTEXT_ATTRIBUTE] = self.get_structured_data()
        return context


class JsonLdView(JsonLdContextMixin, generic.View):
    """
    Render a view with structured data.
    Set `structured_data` with structured data constant fields.
    Override `get_structured_data` for any dynamic fields.
    """


class JsonLdSingleObjectMixin(JsonLdContextMixin):
    """
    CBV mixin which sets structured data for a single object within the context
    """
    def get_structured_data(self):
        super(JsonLdSingleObjectMixin, self).get_structured_data()
        model_structured_data = getattr(self.object, settings.MODEL_ATTRIBUTE)
        self.structured_data.update(model_structured_data)
        return self.structured_data.copy()


class JsonLdDetailView(JsonLdSingleObjectMixin, generic.DetailView):
    """
    Render a "detail" view with structured data taken from object.
    By default implement property `sd` in the model to return structured data in a dict.
    """


class JsonLdMultipleObjectMixin(JsonLdContextMixin):
    """
    CBV mixin which sets structured data for a multiple objects within the context
    """
    def __init__(self):
        if not self.structured_data:
            self.structured_data = {}
        if "@graph" not in self.structured_data:
            self.structured_data["@graph"] = []  # ensure @graph is present
        super(JsonLdMultipleObjectMixin, self).__init__()

    def get_structured_data(self):
        super(JsonLdMultipleObjectMixin, self).get_structured_data()
        for obj in self.object_list:
            obj_structured_data = getattr(obj, settings.MODEL_ATTRIBUTE)
            item_structured_data = DEFAULT_STRUCTURED_DATA.copy()
            item_structured_data.update(obj_structured_data)
            self.structured_data["@graph"].append(item_structured_data)
        return self.structured_data.copy()


class JsonLdListView(JsonLdMultipleObjectMixin, generic.ListView):
    """
    Render a "list" view with structured data taken from object list.
    By default implement property `sd` in the model to return structured data in a dict.
    """


# from django_json_ld.views import JsonLdDetailView
# class ProductDetailView(JsonLdDetailView):
#     model=Product

 
def base(request):
    product_titles = Product.objects.all()
    resource_titles = Resource.objects.all()  
    block_chain_service = BlockChain.objects.all()
    allProds = Product.objects.all()
    
    catprods = Service.objects.values('service_category', 'id')
    cats = {item['service_category'] for item in catprods}
    
    # for cat in cats:
    #     prod = Service.objects.filter(service_category=cat)
    #     allProds.append([prod])
    return product_titles, resource_titles, block_chain_service, allProds

def company(request):
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    Blog_data = Blog.objects.filter().order_by('-blog_date')
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    return render(request,'index.html',{'nft':nft,'crypto':crypto,'blog' : Blog_data[:3], 'productsnav' : product_titles, 'block_chain_service': block_chain_service, 'resourcesnav' : resource_titles, 'allProds' : allProds})

def services(request):
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    allProds = []
    catprods = Service.objects.values('service_category', 'id')
    cats = {item['service_category'] for item in catprods}
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    for cat in cats:
        prod = Service.objects.filter(service_category=cat)
        allProds.append([prod])
    return render(request,'services.html',{'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'servicesitems' : allProds , 'allProds' : allProds})
    
def products(request):
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    allProds = Product.objects.all()
    # catprods = Product.objects.values('product_category', 'id')
    # cats = {item['product_category'] for item in catprods}
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    product_module = Technology.objects.all()
    # for cat in cats:
    #     prod = Product.objects.filter(product_category=cat)
    #     allProds.append([prod])
    
    
    
    return render(request,'product_technology.html',{'module':product_module,'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'productsitems' : allProds , 'allProds' : allProds})

def resources(request):
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    recentresources = Resource.objects.all().order_by('-resource_date')
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    return render(request,'resource.html',{'nft':nft,'crypto':crypto,'resources' : recentresources , 'productsnav' : product_titles, 'recentresources' :recentresources[:3], 'block_chain_service': block_chain_service,'resourcesnav' : resource_titles, 'allProds' : allProds})

def single_resources(request,resource_id):
    Single_resource_data = get_object_or_404(Resource, resource_slug__icontains =resource_id)
    recentresources = Resource.objects.all().order_by('-resource_date')
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()

    return render(request,'resources.html',{'nft':nft,'crypto':crypto,'resources' : Single_resource_data , 'productsnav' : product_titles, 'recentresources' :recentresources[:3], 'block_chain_service': block_chain_service,'resourcesnav' : resource_titles, 'allProds' : allProds})
       
def blog(request):
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    Blog_data = Blog.objects.all().order_by('-blog_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(Blog_data, 3)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    return render(request,'blog.html', {'nft':nft,'crypto':crypto,'users': users , 'productsnav' : product_titles, 'block_chain_service': block_chain_service, 'resourcesnav' : resource_titles, 'allProds' : allProds})
     
def contact(request):
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    responsemsg =''  
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']


        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        print(recaptcha_response, 'sdfsadfsdf')
        print(settings.GOOGLE_RECAPTCHA_SECRET_KEY, 'sdjfayisgfiyaisdgfiasdfiasdhfui')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''
        print(result['success'], 'hfhsudhfuisidfasgdf')
        if result['success']:
            try:
                contactdb = Contact.objects.create(contact_name=name,contact_email=email,contact_subj=subject,contact_msg=message)
                contactdb.save()  
                send_mail( f'{subject}', f'Hello I am {name},----------> {message}------------->{email}', 'kapilyadav@infograins.com', ['vipin@infograins.com'], fail_silently=False)
                responsemsg ='Successfully sent! We will contact you shortly :)'
                return render(request,'contact.html',{'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'error': responsemsg , 'services_list' : services}) 
            except Exception as e:
                responsemsg = e
                return render(request,'contact.html',{'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'error': responsemsg , 'services_list' : services}) 
        return render(request,'contact.html',{'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'error': 'Something went wrong', 'services_list' : services})
    return render(request,'contact.html',{'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'allProds' : allProds})

def products_single(request,product_id):
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    Single_product_data = get_object_or_404(Technology, slug = product_id)
    get_technology_product = Product.objects.filter(Technology_id=Single_product_data.id)
    recentproducts = Product.objects.all().order_by('-product_date')[:3]
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    try:
        getProductSchema = ProductSchema.objects.get(product_id=Single_product_data.id)
    except Exception as exception:
        getProductSchema = ""
    return render(request,'products.html',{'nft':nft,'crypto':crypto,'products' : Single_product_data , 'productsnav' : product_titles, 'block_chain_service':block_chain_service,  'recentproducts' :recentproducts, 'resourcesnav' : resource_titles, 'allProds' : allProds,"getProductSchema":getProductSchema,"get_technology_product":get_technology_product})
    
def products_technologies(request,technology_id,product_id):
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    allProds = Product.objects.all()
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()  
      
    return render(request,'products_single.html',{'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'productsitems' : allProds , 'allProds' : allProds})






def blog_single(request,blog_id):
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    Single_blog_data = get_object_or_404(Blog, blog_slug__icontains = blog_id)
    Blog_data = Blog.objects.filter().order_by('-blog_date')
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    return render(request,'blog-single.html',{'nft':nft,'crypto':crypto,'blog' : Single_blog_data, 'recentblogs' : Blog_data[:3], 'productsnav' : product_titles,'block_chain_service': block_chain_service, 'resourcesnav' : resource_titles, 'allProds' : allProds})

def services_single(request,service_id):
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    Single_service_data = get_object_or_404(Service, service_slug__icontains = service_id)
    recentservices = Service.objects.filter().order_by('-service_date')
    product_titles, resource_titles, block_chain_service, services = base(request)

    try:
        getServiceSchema = ServicesSchema.objects.get(service_id=Single_service_data.id)
    except Exception as exception:
        getServiceSchema = ""
    return render(request,'services-single.html',{"getServiceSchema":getServiceSchema,'nft':nft,'crypto':crypto,'Single_service_data' : Single_service_data, 'recentservices' : recentservices[:3], 'productsnav' : product_titles, 'block_chain_service': block_chain_service, 'resourcesnav' : resource_titles, 'services_list' : services})




def blockchain(request):
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    single_block_chain_service = get_object_or_404(BlockChain, service_title__icontains = "BlockChain Services")
    try:
        get_meta_tag = single_block_chain_service.mtags.service_tag
    except Exception as exception:
        get_meta_tag = ""
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    block_chain_service = BlockChain.objects.exclude(service_title='BlockChain Services')
    blockchain_header = BlockChain.objects.all()[:7]
    return render(request, 'blockchain.html', {'blockchain_header':blockchain_header,'nft':nft,'crypto':crypto,'stag':get_meta_tag, 'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'single_block_chain_service': single_block_chain_service, 'id': block_chain_service.first().id, 'allProds' : allProds})
    

def single_blockchain(request, s_id=BlockChain.objects.first().service_slug):
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    try:
        single_block_chain_service = get_object_or_404(BlockChain, service_slug__icontains = s_id)
        
        # block_chain_title = single_block_chain_service.service_title
    except Exception as e:
        single_block_chain_service = BlockChain.objects.filter(service_slug__icontains = s_id)[0]
        
        # block_chain_title = single_block_chain_service.service_title
    try:
        get_meta_tag = single_block_chain_service.mtags.service_tag
        get_meta_title = single_block_chain_service.mtags.service_title
    except Exception as exception:
        get_meta_tag = ""
        get_meta_title = ""
    # block_chain_service = BlockChain.objects.all()

    try:
        getblockchainSchema = ServicesSchema.objects.get(blockchain_id=single_block_chain_service.id)
    except Exception as exception:
        getblockchainSchema = ""
    
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    block_chain_service = BlockChain.objects.exclude(service_title='BlockChain Services')

    return render(request, 'blockchain.html', {"getblockchainSchema":getblockchainSchema ,'nft':nft,'crypto':crypto,'stag':get_meta_tag,'stitle':get_meta_title,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'single_block_chain_service': single_block_chain_service, 'id': s_id, 'allProds' : allProds})

def workflow(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    block_chain_service = BlockChain.objects.all()
    product_titles, resource_titles, block_chain_service, allProds = base(request)
    return render(request, 'work_process.html', {'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'allProds' : allProds})

def sitemapss(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    block_chain_service = BlockChain.objects.all()
    product_titles, resource_titles, block_chain_service, services = base(request)
    return render(request, 'site-map.html', {'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})



def team(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    team = Team.objects.all()
    block_chain_service = BlockChain.objects.all()
    product_titles, resource_titles, block_chain_service, services = base(request)
    return render(request, 'team1.html', {'nft':nft,'crypto':crypto,'team':team,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})

def privacy_policy(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    block_chain_service = BlockChain.objects.all()
    product_titles, resource_titles, block_chain_service, services = base(request)
    return render(request, 'policy.html', {'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})

def training(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    block_chain_service = BlockChain.objects.all()
    product_titles, resource_titles, block_chain_service, services = base(request)
    return render(request, 'training.html', {'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})


def testimonial(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    block_chain_service = BlockChain.objects.all()
    product_titles, resource_titles, block_chain_service, services = base(request)
    return render(request, 'testimonial.html', {'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})

def aboutus(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    block_chain_service = BlockChain.objects.all()
    product_titles, resource_titles, block_chain_service, services = base(request)
    return render(request, 'aboutus.html', {'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})
    
      
def career(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    block_chain_service = BlockChain.objects.all()
    product_titles, resource_titles, block_chain_service, services = base(request)
    career=Career.objects.filter(Available=True)
    return render(request, 'career.html', {'nft':nft,'crypto':crypto,'Career' : career,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})

def help(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    block_chain_service = BlockChain.objects.all()
    product_titles, resource_titles, block_chain_service, services = base(request)
    return render(request, 'how_can_we_help.html', {'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})

def join_event(request):
    return render(request, 'setDate.html')

def add_event(request):
    return render(request, 'event-form.html')


def franchise_form(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    if request.method == "POST":
            
            first_name = request.POST.get('firstname',"")
            last_name = request.POST.get('lastname',"")
            email = request.POST.get("email","")
            contact = request.POST.get("contact","")
            address = request.POST.get("address","")
            state = request.POST.get("state","")
            city = request.POST.get("city","")
            source = request.POST.get("lead_source","")
            specify1=request.POST.get("specify","")
            notes = request.POST.get("notes","")
            if first_name != '':
                franchise = Franchise(first_name = first_name,last_name=last_name,email=email,contact=contact,address=address,state=state,city=city,source=source,specify=specify1,notes=notes)
                franchise.save()
                mailtemplate=render_to_string('emailmsg.html', {'i': franchise})
                send_mail('Franchise Request', mailtemplate , 'kapilyadav@infograins.com' ,['franchise@infograins.com'],fail_silently=False)

    product_titles, resource_titles, block_chain_service, services = base(request)
    
    return render(request,'franchisepage.html', {'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})



def Applyjob(request):
    nft = NFT.objects.all()
    crypto = Crypto.objects.all()
    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        position = request.POST['position']
        skill = request.POST['skills']
        experience = request.POST['experience']
        source = request.POST['source']
        specify1=request.POST['specify']
        resume = request.FILES['resume']
        print(resume)

        
        job = Apply_job(first_name = first_name,last_name=last_name,email=email,contact=contact,address=address,position_applying_for=position,skills=skill,experience=experience,source=source,specify=specify1,Resume=resume)
        job.save()
        mailmsg=render_to_string('jobmail.html', {'i': job})
       
        fromaddr = "kapilyadav@infograins.com"
        toaddr = "hr@infograins.com"
        
        msg = MIMEMultipart()
        
        msg['From'] = fromaddr
   
        msg['To'] = toaddr
        
        msg['Subject'] = "Job application"
        body = mailmsg

        msg.attach(MIMEText(body, 'plain'))
        
        filename = resume
        attachment = open(job.Resume.path,'rb')
       
       
        p = MIMEBase('application', 'octet-stream')
        
        p.set_payload((attachment).read())

        encoders.encode_base64(p)
        
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        msg.attach(p)
        
        s = smtplib.SMTP('mail.infograins.com', 587)
        
        s.starttls()
        
        s.login(fromaddr, "Yadav@1357")
        
        text = msg.as_string()
        
        s.sendmail(fromaddr, toaddr, text)
        
        
        s.quit()
        
        if job:
            return redirect ('/company/')
       
       
    product_titles, resource_titles, block_chain_service, services = base(request)
    
    return render(request,'applyjob.html',  {'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})
            


def events(request):
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    product_titles, resource_titles, block_chain_service, services = base(request)
    
    return render(request, 'events.html' ,{'nft':nft,'crypto':crypto,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})
    

    
def Nft(request,slug):
    nft = NFT.objects.all()
    nft1 = NFT.objects.filter(slug=slug)
    nft2 = NFT.objects.get(slug=slug)
    crypto = Crypto.objects.all()
    
    product_titles, resource_titles, block_chain_service, services = base(request)
    return render(request, 'nft.html' ,{'crypto':crypto,'nft2':nft2,'nft':nft,'nft1':nft1, 'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})
    
    
def crypto(request,slug):
    crypto = Crypto.objects.all()
    crypto1 = Crypto.objects.filter(slug=slug)
    crypto2 = Crypto.objects.get(slug=slug)
    nft = NFT.objects.all()
    
    product_titles, resource_titles, block_chain_service, services = base(request)
    return render(request, 'crypto.html' ,{'nft':nft,'crypto':crypto,'crypto1':crypto1,'crypto2':crypto2 ,'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services})
    
    



def Fork_data(request, slug):
    product_titles, resource_titles, block_chain_service, services = base(request)
    crypto = Crypto.objects.all()
    nft = NFT.objects.all()
    fork_title = Fork_Title.objects.filter(slug=slug)
    fork = Fork.objects.filter(fork_block__slug = slug)
    get_list_of_fork = Fork_Title.objects.all().order_by("id")
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        skypeid = request.POST['skype_id']
        contact = request.POST['phone']
        country = request.POST['country']
        
        code = CountryInfo(country)
        country_code = code.calling_codes()[0]
        

        # country_code = request.POST(data)   
        demo = request.POST.getlist('getfork[]')
        demofor = ",".join(demo)
       

        message = request.POST['msg']
        
        

        form = Fork_Form(name = name, email = email, contact = contact, country = country, skype_id = skypeid, message = message, demo_for= demofor, country_code = country_code)
        if name != '' :
            form.save()
            mail=render_to_string('forkmail.html', {'i': form})
            send_mail('Fork demo Request', mail , 'kapilyadav@infograins.com' ,['vipin@infograins.com'],fail_silently=False)
           






    
    
    return render(request, 'forks.html', {'nft':nft, 'crypto':crypto, 'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'services_list' : services, 'fork_title':fork_title, 'fork':fork, "get_list_of_fork":get_list_of_fork})
    