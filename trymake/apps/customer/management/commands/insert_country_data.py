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
            self.stdout.write(
                "Inserting states into database for country: {0}({1})...".format(c.name,c.alpha_2),
                ending=""
            )
            if Country.objects.filter(code=c.alpha_2).exists():
                self.stdout.write("Failed")
                self.stderr.write("{0} already exists in database...\n"
                                  "Skipping over to next.".format(c.name))
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
            self.stdout.write("OK")
        self.stdout.write("")
