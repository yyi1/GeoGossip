from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone
from django.db import transaction
from geogossip.models import Group
import datetime

HOUR = 3600.0


class Command(BaseCommand):
    help = 'delete the stale groups'

    @transaction.atomic
    def handle(self, *args, **options):
        groups = Group.objects.all()
        now = datetime.datetime.now(tz=get_current_timezone())
        count = 0
        for group in groups:
            if (now - group.created_on).total_seconds() > group.lifetime * HOUR:
                count += 1
                self.stdout.write(self.style.SUCCESS('Deleted group: {}'.format(group.name)))
                group.delete()
            pass
        self.stdout.write(self.style.SUCCESS('Deleted totally {} groups.'.format(count)))
        pass
    pass
