from calender.models import Register


def next_event_register_url(request):
    if not request.user.is_authenticated:
        return {}

    register = Register.objects.next_event_register(request.user)
    if not register:
        return {
            "next_event_register_url": None,
            "next_event_registered": False,
        }

    return {
        "next_event_register_url": register.get_absolute_url(),
        "next_event_registered": register.is_registered,
    }
