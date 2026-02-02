from django.db import models
import os.path
import pathlib
from django.conf import settings

# from settings import MEDIA_ICACHE, MEDIA_ROOT,ICACHE_URL
from PIL import Image
import shutil


# Create your models here.
class FaltuModel(models.Model):
    """class Meta:
    abstract = True
    """


class ImageTool:
    def resize(filename, width, height):
        fpath = settings.MEDIA_ROOT + filename
        # print(__file__,fpath)

        # print(fpath)

        DIR_IMAGE = settings.MEDIA_ICACHE
        if not os.path.exists(fpath):
            return
        extension = pathlib.Path(filename).suffix
        # print(extension)
        allowed_ext = [".jpg", ".JPG", ".GIF", ".PNG", ".png", ".gif", ".jpeg"]
        image_old = filename
        """filename without extension
        """
        fwext = pathlib.Path(filename).stem
        dirds = os.path.split(filename)
        # print(fwext)
        # print(dirds)
        # dirs=pathlib.Path(filename).parts
        # dirs='cache/'+dirds[0]
        dirs = dirds[0]
        # image_new = 'cache/' +dirs+ fwext+ '-' +str(width) + 'x' + str(height) + extension
        if dirs != "":
            image_new = (
                dirs + "/" + fwext + "-" + str(width) + "x" + str(height) + extension
            )
        else:
            image_new = fwext + "-" + str(width) + "x" + str(height) + extension
        # print(image_new)
        # print(fpath)
        ow, oh = Image.open(fpath).size
        if not os.path.exists(DIR_IMAGE + image_new):
            #print("not cached")
            # print(DIR_IMAGE,image_new)
            # print("dirs")
            # print(dirs)

            if not extension in allowed_ext:
                return DIR_IMAGE + image_old

            path = ""

            directories = dirs.split("/")
            # print(directories)

            prefix = ""
            for dir in directories:
                if dir != "":
                    path = path + prefix + dir
                    # print(DIR_IMAGE+path)
                    if not os.path.exists(DIR_IMAGE + path):
                        # print("moning path")
                        # print(DIR_IMAGE+path+'/')
                        os.mkdir(DIR_IMAGE + path + "/")
                    prefix = "/"

            # os.makedirs(DIR_IMAGE+dirs,0o777,True)
            # print("old width not equal to width")
            if ow != width or oh != height:
                # print("oh!=wid")
                image = Image.open(settings.MEDIA_ROOT + image_old)
                image.thumbnail((width, height))
                # print(DIR_IMAGE+image_new)
                image.save(DIR_IMAGE + image_new)
                # shutil.copyfile(fpath,DIR_IMAGE+image_new)
                return settings.ICACHE_URL + image_new
            else:
                shutil.copyfile(fpath, DIR_IMAGE + image_new)
                return settings.ICACHE_URL + image_new
        else:
            return settings.ICACHE_URL + image_new
