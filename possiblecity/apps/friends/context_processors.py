from .models import Suggestion


def suggestions(request):
    if request.user.is_authenticated():
        return {
            "new_suggestion_count": Suggestion.objects.for_user(
                request.user
            ).filter(relationship__isnull=True).count(),
        }
    return {}
