from django.shortcuts import render
from Infograins.models import Blog, Product, Resource, Service, Contact, BlockChain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from Infograins_site.settings import EMAIL_HOST_USER

 
def base(request):
    product_titles = Product.objects.all()
    resource_titles = Resource.objects.all()  
    block_chain_service = BlockChain.objects.all()
    return product_titles, resource_titles, block_chain_service

def company(request):
    product_titles, resource_titles, block_chain_service = base(request)
    Blog_data = Blog.objects.filter().order_by('-blog_date')
    return render(request,'index.html',{'blog' : Blog_data[:3], 'productsnav' : product_titles, 'block_chain_service': block_chain_service, 'resourcesnav' : resource_titles})

def services(request):
    product_titles, resource_titles, block_chain_service = base(request)
    allProds = []
    catprods = Service.objects.values('service_category', 'id')
    cats = {item['service_category'] for item in catprods}
    for cat in cats:
        prod = Service.objects.filter(service_category=cat)
        allProds.append([prod])
    return render(request,'services.html',{'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'servicesitems' : allProds })
    
def products(request):
    product_titles, resource_titles, block_chain_service = base(request)
    allProds = []
    catprods = Product.objects.values('product_category', 'id')
    cats = {item['product_category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_category=cat)
        allProds.append([prod])
    return render(request,'products.html',{'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'productsitems' : allProds })

def resources(request,resource_id):
    Single_resource_data = get_object_or_404(Resource,pk=resource_id)
    recentresources = Resource.objects.all().order_by('-resource_date')
    product_titles, resource_titles, block_chain_service = base(request)
    return render(request,'resources.html',{'resources' : Single_resource_data , 'productsnav' : product_titles, 'recentresources' :recentresources[:3], 'block_chain_service': block_chain_service,'resourcesnav' : resource_titles})
       
def blog(request):
    Blog_data = Blog.objects.all().order_by('-blog_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(Blog_data, 3)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    product_titles, resource_titles, block_chain_service = base(request)
    return render(request,'blog.html', {'users': users , 'productsnav' : product_titles, 'block_chain_service': block_chain_service, 'resourcesnav' : resource_titles})
     
def contact(request):
    responsemsg =''  
    product_titles, resource_titles, block_chain_service = base(request)
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        try:
            contactdb = Contact.objects.create(contact_name=name,contact_email=email,contact_subj=subject,contact_msg=message)
            contactdb.save()  
            send_mail( f'{subject}', f'Hello I am {name},----------> {message}------------->{email}', EMAIL_HOST_USER, [f'vipin.infograins@gmail.com'], fail_silently=False)
            responsemsg ='Successfully sent! We will contact you shortly :)'
            return render(request,'contact.html',{'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'error': responsemsg }) 
        except Exception as e:
            responsemsg = e
            return render(request,'contact.html',{'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'error': responsemsg }) 
    return render(request,'contact.html',{'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'error': responsemsg })
     
def products_single(request,product_id):
    Single_product_data = get_object_or_404(Product,pk=product_id)
    recentproducts = Product.objects.all().order_by('-product_date')[:3]
    product_titles, resource_titles, block_chain_service = base(request)
    return render(request,'products_single.html',{'products' : Single_product_data , 'productsnav' : product_titles, 'block_chain_service': block_chain_service,  'recentproducts' :recentproducts, 'resourcesnav' : resource_titles})
    
def blog_single(request,blog_id):
    Single_blog_data = get_object_or_404(Blog,pk=blog_id)
    Blog_data = Blog.objects.filter().order_by('-blog_date')
    product_titles, resource_titles, block_chain_service = base(request)
    return render(request,'blog-single.html',{'blog' : Single_blog_data, 'recentblogs' : Blog_data[:3], 'productsnav' : product_titles,'block_chain_service': block_chain_service, 'resourcesnav' : resource_titles})

def services_single(request,service_id):
    Single_service_data = get_object_or_404(Service,pk=service_id)
    recentservices = Service.objects.filter().order_by('-service_date')
    product_titles, resource_titles, block_chain_service = base(request)
    return render(request,'services-single.html',{'Single_service_data' : Single_service_data, 'recentservices' : recentservices[:3], 'productsnav' : product_titles, 'block_chain_service': block_chain_service, 'resourcesnav' : resource_titles})

def blockchain(request):
    
    block_chain_service = BlockChain.objects.all()
    single_block_chain_service = get_object_or_404(BlockChain, id = block_chain_service.first().id)
    product_titles, resource_titles, block_chain_service= base(request)
    return render(request, 'blockchain.html', {'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'single_block_chain_service': single_block_chain_service, 'id': block_chain_service.first().id})
    

def single_blockchain(request, s_id=1):
    single_block_chain_service = get_object_or_404(BlockChain, id = s_id)
    block_chain_service = BlockChain.objects.all()
    product_titles, resource_titles, block_chain_service= base(request)
    return render(request, 'blockchain.html', {'productsnav' : product_titles, 'resourcesnav' : resource_titles, 'block_chain_service': block_chain_service, 'single_block_chain_service': single_block_chain_service, 'id': s_id})