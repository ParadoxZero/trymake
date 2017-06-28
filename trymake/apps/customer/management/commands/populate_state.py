"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Trymake Inc
All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

import pycountry
from django.core.management import BaseCommand

from trymake.apps.customer.models import State, Country


class Command(BaseCommand):
    help = "Populate state and Country models"

    def handle(self, *args, **options):
        for c in pycountry.countries:
            if c.alpha_2=='IN':
                continue
            country = Country()
            country.name = c.name
            country.code = c.alpha_2
            country.save()

            state_list = pycountry.subdivisions.get(country_code=country.code)
            for state in state_list:
                s = State()
                s.code = state.code
                s.name = state.name
                s.country = country
                s.save()
