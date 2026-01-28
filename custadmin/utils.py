from django.apps import apps

licons = {
    "auth": "fa-cog",
    "order": "fa-file-invoice",
    "information": "fa-bell",
    "category": "fa-puzzle-piece",
    "doctor": "fa-stethoscope",
    "group": "fa-user-group",
    "tax": "fa-list-ul",
    "payment": "fa-wallet",
    "service": "fa-tags",
    "user": "fa-user",
    "service": "fa-handshake",
    "doctorspecial": "fa-calendar-days",
    "customer": "fa-person",
}


def getIcons(name, type="parent"):
    match (type):
        case "parent":
            return licons.get(name, "fa fa-folder")
        case _:
            return licons.get(name, "fa fa-folder")


def get_installed_apps():
    return [app_config.label for app_config in apps.get_app_configs()]
