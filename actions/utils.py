import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import Action


def create_action(user, verb, target=None):
    """
    Try to create an action instance for given info.
    If action exist in database and was created within last minute False will
    be returned otherwise True
    """

    # check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
        verb=verb,
        created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
            target_id=target.id)

    if not similar_actions:
        # no existing actions found
        Action.objects.create(user=user, verb=verb, target=target)
        return True
    return False
