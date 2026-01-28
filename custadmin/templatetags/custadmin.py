import json
import logging
from custadmin.utils import get_installed_apps, getIcons
from django.conf import settings
from django.template import Context, Library
from django.templatetags.static import static

logger = logging.getLogger(__name__)
from django.utils.html import escape, format_html
from django.template.loader import get_template

register = Library()


@register.simple_tag(takes_context=True)
def get_side_menu(context: Context, using: str = "available_apps"):
    user = context.get("user")

    if not user:
        return []
    apps = get_installed_apps()
    # print(vars(settings))
    # print(dir(context))
    # print(vars(context))
    hide = []
    # print(getattr(settings,'HIDE_APPS'))
    hide = getattr(settings, "HIDE_APPS", [])
    hidem = getattr(settings, "HIDE_MODELS", [])
    clinks = getattr(settings, "custom_links", [])
    # print(clinks)
    # for s in settings:
    #    print(s)

    # apps=[x for x in apps if not x in hide ]
    # print(apps)
    menu = []
    available_apps = context.get("available_apps")
    # print(available_apps)
    for i, app in enumerate(available_apps):
        app_label = app["app_label"].lower()
        if app_label in hide:
            continue
        models = app.get("models", [])
        menu_items = []
        for ii, model in enumerate(models):
            model_str = "{app_label}.{model}".format(
                app_label=app_label, model=model["object_name"]
            ).lower()
            if model_str in hidem:
                continue
            model["index"] = ii
            model["url"] = model["admin_url"]
            model["model_str"] = model_str
            menu_items.append(model)
        app["models"] = menu_items
        app["icon"] = getIcons(app_label)
        app["index"] = i
        menu.append(app)

    return menu
    # for a in apps:
    # mods=a.get("models",[])
    # print(mods)
