from django.contrib import admin,messages
from .models import ConfigModel
from .forms import ConfigBasic,ConfigForm1
from django.shortcuts import render, redirect
from django.urls import path
from fm.models import ImageTool
def get_logo_image(logo):
    return ImageTool.resize(logo or "placeholder.png", 100, 100)

def get_config(key, default=""):
    return ConfigModel.objects.filter(cname=key).values_list("cvalue", flat=True).first() or default

def set_config(key, value):
    ConfigModel.objects.update_or_create(cname=key, defaults={"cvalue": value})
@admin.register(ConfigModel)
# Register your models here.
class ConfigAdmin(admin.ModelAdmin):
    actions = None
    list_display = ["cname", "cvalue"]
    def get_urls(self):
        urls = super().get_urls()
        custom_url=[path('showsave', self.admin_site.admin_view(self.showsave_view),
                name="config_showsave",
            ),]
        return custom_url
  
 
    def _saveConfig(self,post,param=1):
        form1=ConfigBasic(post)
        form2=ConfigForm1(post)
        if form1.is_valid():
            for k, v in form1.cleaned_data.items():
                    set_config(k, v)
        set_config('logo',post['logo'])
        if form2.is_valid():
            for k, v in form2.cleaned_data.items():
                    set_config(k, v)
                     
    def get_initial_config(self,param=1):
     if param==1 :
        configs = ConfigModel.objects.filter(
            cname__in=["support_email", "mmode", "logo"]
        )
     if param==2:
         configs = ConfigModel.objects.filter(
            cname__in=["fb_id","x_id", "gci_id", "instagram_id"]
        )
     return {
        c.cname:  c.cvalue
        for c in configs
    }
    
    def showsave_view(self, request):
        context = dict(
        self.admin_site.each_context(request),
        title="Site Settings",
    )
        #extra_context = extra_context or {}
        logo = request.POST.get('logo', '') if request.method == 'POST' else get_config('logo')
        pimg = get_logo_image(logo)
        if request.method=='POST':
          

            self._saveConfig(request.POST)
            #self._saveConfig(request.POST)
            messages.success(request,"Saved")
                    
        form1=ConfigBasic(self.get_initial_config())
        form2=ConfigForm1(self.get_initial_config(2))
        context["title"] = "Site Configuration"
        context["form2"]=form2
        context['form1']=form1
        context['pimg']=pimg
        context['logo']=logo
        #extra_context["total_configs"] = self.model.objects.count()
        return render(request, "add.html", {
           **context
          
        })
 
    def has_add_permission(self, request):
        return False
