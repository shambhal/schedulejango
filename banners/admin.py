from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from banners.models import Banner
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from banners.forms import BannerForm1
from django.utils.html import format_html
from fm.models import ImageTool, FaltuModel as fm2
# Register your models here.
@admin.register(Banner)
class Bannerdmin(admin.ModelAdmin):
    change_form_template = "admin/banner_form.html"
    add_form_template = "admin/banner_form.html"
    list_display = ("category", "sort_order","tag", "image_tag")
    list_editable = ("sort_order",)
    ordering = ("sort_order",)

    def image_tag(self, obj):
        if obj.image:
            im=ImageTool.resize(obj.image,100,100)
            return format_html('<img src="{}" width="100" height="50" style="object-fit:cover;"/>', im)
        return "-"
    image_tag.short_description = "Preview"
    def add_view(self, request, form_url="", extra_context={}):
        if request.method == "POST":
            form1=BannerForm1(request.POST)
            if(form1.is_valid()):
            
                if request.POST["img"] != None:
                 return self._save(request, form_url, extra_context)
            else:
                # when form is not valid
                #
                thumb=ImageTool.resize(request.POST['img'],100,100)
                extra_content = {
                    "thumb": thumb,
                    "image":request.POST['img'],
                    "form1":form1
                }
                return super().add_view(request, form_url, extra_content)
        else:
            form1 = BannerForm1()
           

        extra_context["form1"] = BannerForm1()
      
        thumb = ImageTool.resize("placeholder.png", 100, 100)
        extra_content = {
            #'furl':furl,
            
            "thumb": thumb,
            "image": None,
            "form1": form1,
            
        }
        return super().add_view(request, form_url, extra_content)
# Register your models here.
    def _update(self, request, object_id, form_url="", extra_context={}):
        # checked

        obj = Banner.objects.get(pk=object_id)
        img = request.POST["img"]
        pimg = ImageTool.resize("placeholder.png", 100, 100)
        if img != None and img != "":
            thumb = ImageTool.resize(img, 100, 100)
            img = obj.image
        else:
            thumb = ImageTool.resize("placeholder.png", 100, 100)
            img = None
        if obj.id:
            form1 = BannerForm1(request.POST, instance=obj)
            # form1['first_name']="laila"
            
            extra_context = {
                "form1": form1,
               
                "pimg": pimg,
            }
            img = request.POST["img"]
            """
                    if(obj.image!=None and obj.image!='') :
                        thumb=ImageTool.resize(obj.image,100,100)
                        img=obj.image
                    else:
                     thumb=ImageTool.resize('placeholder.png',100,100)
                     img=None
                     """

            if form1.is_valid() :
                form1.save()
                
                img = request.POST["img"]
                # if(img!=None and img!='') :
                obj.image = img
                obj.save()
                messages.add_message(request, messages.INFO, "Updated Record")
            else:
                print("forms are not valid")
        extra_context["image"] = img
        extra_context["thumb"] = thumb
        extra_context["pimg"] = pimg
        return super().change_view(request, object_id, form_url, extra_context)
    def _save(self, request, form_url="", extra_context={}):
        img = request.POST.get("img", None)
        pimg = ImageTool.resize("placeholder.png", 100, 100)
        if img != None:
            thumb = ImageTool.resize(request.POST["img"], 100, 100)

        else:
            img = None
            thumb = ImageTool.resize("placeholder.png", 100, 100)
        form1 = BannerForm1(request.POST)
     
        if form1.is_valid() :
            
                    #combined_data={**form1,'image':img}

               
                   
                   dpc=form1.save(commit=False)
                   dpc.image=img
                    
                   dpc.save()
        else:    
                   extra_context={ "thumb": thumb,
                    "image": img,
                    "form1": form1,}
                   return super().add_view(request, form_url, extra_context)
        messages.success(request, "Banner saved successfully")
        return redirect("/banners/banner")
    def change_view(self, request, object_id, form_url="", extra_context={}):
        pimg = ImageTool.resize("placeholder.png", 100, 100)
        if request.method == "POST":
            return self._update(request, object_id, form_url, extra_context)
            pass
        else:
            obj = Banner.objects.get(pk=object_id)
            form1 = BannerForm1(instance=obj)

          
            if obj.image != None and obj.image != "":
                thumb = ImageTool.resize(obj.image, 100, 100)
                img = obj.image
            else:
                thumb = ImageTool.resize("placeholder.png", 100, 100)
                img = None
            extra_context = {
                "pimg": pimg,
                "form1": form1,
              
                "image": img,
                "thumb": thumb,
            }

            return super().change_view(request, object_id, form_url, extra_context)



