from django.contrib import admin

# from pycom.admin import admin_site
from django.http import JsonResponse
from django.urls import reverse
import re
from django.template.loader import get_template
from pathlib import Path
from django.conf import settings

# import MEDIA_ICACHE, MEDIA_ROOT
from .models import FaltuModel, ImageTool
from django.http.response import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.utils.html import format_html
from django.urls import path
from pathlib import Path
from django.core.paginator import Paginator
import os.path
from django.shortcuts import render

# Register your models here.


class FaltuAdmin(admin.ModelAdmin):
    def folder(self, request):
        directory = request.GET.get("directory", None)
        folder = request.POST.get("folder", "")
        if folder == "":
            return JsonResponse({"error": "Missing Folder Name"})
        folder = folder[0:20]

        folder = self.rename(folder, "")
        if len(folder) < 3:
            return JsonResponse({"error": "Please enter longer folder name"})
        if directory != None:
            directoryp = settings.MEDIA_ROOT + "catalog/" + directory + "/" + folder

        else:
            directoryp = settings.MEDIA_ROOT + "catalog/" + folder

        if not os.path.exists(directoryp):
            os.mkdir(directoryp)
            return JsonResponse({"success": "Created"})
        else:
            return JsonResponse({"error": "Directory Exists"})

    def common_filemanager(self, request):
        target = request.GET.get("target", "")
        kv = request.GET.get("k", 1)
        kv = int(kv)
        # print(kv)
        # exit()
        # thumb= request.GET.get('thumb','')
        pagesize = 8
        directory = request.GET.get("directory", None)
        thumb = request.GET.get("thumb", None)
        prefix = ""
        parent = ""
        if directory != None:
            directorypath = settings.MEDIA_ROOT + "catalog/" + directory
            prefix = "catalog/" + directory + "/"
            parr = directory.split("/")
            for y in parr[0:-1]:
                parent = parent + y + "/"
            parent = parent[0:-1]

        else:
            directorypath = settings.MEDIA_ROOT + "catalog/"
            prefix = "catalog/"
     
        page = request.GET.get("page", 1)

        directories = []
        files = []
        p = Path(directorypath).glob("*")
        for x in p:
            #print(x)
            if x.is_file():
                files.append(x)
            if x.is_dir():
                directories.append(x)
        #print(files)        
        merge = directories + files
        total = len(merge)
        start = (int(page) - 1) * pagesize
        end = start + pagesize
        images = merge[start:end]
        # print(images)
        imgs = []
        for image in images:
            name = os.path.basename(image)
            if Path(image).is_dir():
                # print("yes dir")
                url = ""
                if target != "":
                    url += "&target=" + target
                if thumb != None:
                    url += "&thumb=" + thumb
                imgs.append(
                    {
                        "thumb": "",
                        "type": "directory",
                        "name": name,
                        "path": name,
                        "href": reverse("admin:commonfilemanager")
                        + "?directory="
                        + name
                        + url+'&k=2',
                    }
                )
            else:
                if Path(image).is_file():
                    # print("is file")
                    # print(prefix,image.name)
                    #thumb=ImageTool.resize(prefix+image.name,100,100)
                    imgs.append(
                        {
                            "type": "image",
                            "name": name,
                            "href": reverse("admin:commonfilemanager"),
                       
                        
                            "thumb": ImageTool.resize(
                                prefix + image.name,
                                100,
                                100,
                            ),
                            "path": prefix + image.name,
                        }
                    )
        #print(imgs)
        paginator = Paginator(merge, pagesize)
        page_obj = paginator.get_page(page)
        #############parent url down
        purl = "?stuff=1"
        args = {}
        if target != None:
            purl = purl + "&target=" + target
        if thumb != None:
            purl = purl + "&thumb=" + thumb

        purl = reverse("admin:commonfilemanager") + purl
        rurl = purl
        #print(purl)
        if directory != None:
            rurl = rurl + "&directory=" + directory
           
        if parent != "":
           
           
                  purl = purl + "&directory=" + parent
                  purl = purl + "&k=2" if "&k=2" not in purl else purl
        rurl = rurl + "&k=2" if "&k=2" not in rurl else rurl
        rpurl=rurl
        
        arr = {
            "page_obj": page_obj,
            'page':page,
            "imgs": imgs,
            "target": target,
            "rurl": rurl,
            "thumb": thumb,
            "purl": purl,
            "entry_folder": "Folder",
            "button_folder": "Create Folder",
            "directory": request.GET.get("directory", ""),
            "heading_title": "File Manager",
            "text_confirm": "Do you really want to delete ?",
        }
        #print(f"{kv} is kv")
        if kv == 1:
            return render(request, "admin/fm.html", arr)
            #return HttpResponse(p)
           #template='admin/fm.html'
           #return HttpResponse(template.render(arr))
        else:
            #print("inner")
            template = get_template("admin/fm_inner.html")
            rendered = template.render(arr)
            return HttpResponse(rendered)

    def _innerupload(file):
        jarr = file.split(".")
        name = jarr[0]
        ext = jarr[1]

    def rename(self, file, ext):
        file = re.sub(r"\s", "_", file)
        file = re.sub(r"_{2,}", "_", file)[0:30]

        if ext != "":
            return file + "." + ext
        else:
            return file

    def deleteF(self, request):
        path1 = request.POST.getlist("path", "")
        
        for f1 in path1:
            #print(f1)
            #print(settings.MEDIA_ROOT + f1)
            #if os.path.exists(settings.MEDIA_ROOT + f1):
            if(1==1):
                #print(settings.MEDIA_ROOT+f1)
                #print("here")
                p=Path(settings.MEDIA_ROOT + f1)
                #print(p)
                if(os.path.isfile(settings.MEDIA_ROOT+f1)) :
                   #print("this is file")
                   os.remove(settings.MEDIA_ROOT + f1)
                if p.is_dir() :
                   #print("this is dir")
                   os.rmdir(settings.MEDIA_ROOT + f1)   
          
        '''  
        if os.path.exists(settings.MEDIA_ROOT + f1):
                if(os.path.isfile(settings.MEDIA_ROOT+f1)) :
                   os.remove(settings.MEDIA_ROOT + f1)
                if(os.path.isdir(settings.MEDIA_ROOT+f1)) :
                   os.rmdir(settings.MEDIA_ROOT + f1) 
        '''           
        return JsonResponse({"success": "File(s) deleted"})

    def upload_fm(self, request):
        print("inuploadfm")
        directory = request.GET.get("directory", None)

        parent = ""
        if directory != None and directory != "":
            directory = settings.MEDIA_ROOT + "catalog/" + directory
            prefix = "catalog/" + directory+'/'

        else:
            directory = settings.MEDIA_ROOT + "catalog/"
            prefix = "catalog/"
        files = request.FILES.getlist("file", None)
        for file in files:
            # print(file)
            # print(file.name)
            jarr = str(file.name).split(".")
            name = jarr[0]
            ext = jarr[1]
            ext = ext.lower()
            #print(ext)
        arr = ["jpg", "jpeg", "png", "gif"]
        if ext not in arr:
            err = {"error": "Invalid File uuPloaded"}
            return JsonResponse(err)
        else:
            print("valid file")
            fs = FileSystemStorage()
            nf = self.rename(name, ext)
            print("he shona")
            print(f"{prefix} is prefix and {nf} is nf")
            filename = fs.save(prefix+nf, file)
            print(f" filename is {filename}")
            return JsonResponse({"success": 1})
        return HttpResponse(" is directory")

    def get_urls(self):
        urls = super().get_urls()

        myurls = [
            path(
                "common_filemanager",
                self.admin_site.admin_view(self.common_filemanager),
                name="commonfilemanager",
            ),
            path(
                "uplod_fm", self.admin_site.admin_view(self.upload_fm), name="uploadfm"
            ),
            path(
                "create_folder",
                self.admin_site.admin_view(self.folder),
                name="createfolder",
            ),
            path("deleteF", self.admin_site.admin_view(self.deleteF), name="deleteF"),
        ]
        return myurls


admin.site.register(FaltuModel, FaltuAdmin)
# admin_site.register(FaltuModel,FaltuAdmin )
