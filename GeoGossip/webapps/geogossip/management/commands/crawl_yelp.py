import os
import time
import sys
from django.core.management.base import BaseCommand
from django.db import transaction
from geogossip.models import Business
from geogossip.forms import BusinessForm
from geogossip.utils import merge_categories
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


class Command(BaseCommand):
    help = 'crawl businesses from yelp around CMU'

    @transaction.atomic
    def handle(self, *args, **options):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        auth = Oauth1Authenticator(
            consumer_key=os.environ['CONSUMER_KEY'],
            consumer_secret=os.environ['CONSUMER_SECRET'],
            token=os.environ['TOKEN'],
            token_secret=os.environ['TOKEN_SECRET']
        )
        client = Client(auth)
        params = {
            'location': 'Carnegie+Mellon+University',
            'radius_filter': 2500
        }
        response = client.search(**params)
        total = response.total
        self.stdout.write(self.style.SUCCESS('Found {} businesses'.format(total)))
        Business.objects.all().delete()
        offset = 0
        malformed = 0
        while offset < total:
            for business in response.businesses:
                offset += 1
                if not business.location or not business.location.coordinate:
                    malformed += 1
                    continue
                    pass
                business_form = BusinessForm({
                    'name': business.name,
                    'categories': merge_categories(business.categories),
                    'lat': business.location.coordinate.latitude,
                    'lon': business.location.coordinate.longitude,
                    'is_closed': business.is_closed,
                    'image_url': business.image_url,
                    'url': business.url,
                    'display_phone': business.display_phone,
                    'review_count': business.review_count,
                    'rating': business.rating
                })
                if business_form.is_valid():
                    business_form.save()
                    pass
                else:
                    malformed += 1
                    pass
                pass
            self.stdout.write(self.style.SUCCESS('{} businesses are saved.'.format(offset - malformed)))
            if offset < total:
                time.sleep(0.01)
                params['offset'] = offset
                response = client.search(**params)
                pass
            pass
        self.stdout.write(self.style.SUCCESS('There are {} businesses saved.'.format(len(Business.objects.all()))))
        self.stderr.write(self.style.NOTICE('There are totally {} malformed businesses.'.format(malformed)))
        pass
    pass
