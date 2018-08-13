# -*- coding: utf-8 -*-
from scrapy import Item, Field
from scrapy.conf import settings

class AlbertasecondaryItem(Item):
    school_name = Field()
    school_sector = Field()
    school_address = Field()
    school_city = Field()
    school_postcode = Field()
    school_phone = Field()
    school_district = Field()

    school_website = Field()

    school_student = Field()
    school_esl = Field()
    school_speneeds = Field()
    school_frenchi = Field()
    school_aveincome = Field()
    school_actrating = Field()

    score_avgmark = [' ']*settings['YEARS_NUM']
    score_failed = [' ']*settings['YEARS_NUM']
    score_markdiff = [' ']*settings['YEARS_NUM']
    score_genlang = [' ']*settings['YEARS_NUM']
    score_genmath = [' ']*settings['YEARS_NUM']
    score_coursetk = [' ']*settings['YEARS_NUM']
    score_dplrate = [' ']*settings['YEARS_NUM']
    score_delayed = [' ']*settings['YEARS_NUM']
    score_all = [' ']*settings['YEARS_NUM']

    score_avgmark = Field()
    score_failed = Field()
    score_markdiff = Field()
    score_genlang = Field()
    score_genmath = Field()
    score_coursetk = Field()
    score_dplrate = Field()
    score_delayed = Field()
    score_all = Field()
