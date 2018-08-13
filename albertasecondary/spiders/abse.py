# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.conf import settings
from albertasecondary.items import AlbertasecondaryItem

class AbseSpider(Spider):
    name = 'abse'
    allowed_domains = ['alberta.compareschoolrankings.org']
    start_urls = ['http://alberta.compareschoolrankings.org/']

    def start_requests(self):
        url = "http://alberta.compareschoolrankings.org/high/SchoolsByRankLocationName.aspx"
        yield Request(url, callback=self.parse_links)

    def parse_links(self, response):
        links = response.xpath('//td[@class="tdcell"]//a')
        for temp in links:
            link = "http://alberta.compareschoolrankings.org" + temp.xpath('./@href').extract_first()
            yield Request(link, callback=self.parse_page)

    def parse_page(self, response):
        
        block_info = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_SchoolInfoDisplay"]//text()').extract()
        school_website = response.xpath('//a[@id="ctl00_ContentPlaceHolder1_hlSchoolWebsite"]//text()').extract_first()
        report_info = response.xpath('//table[@id="ctl00_ContentPlaceHolder1_detailedReportCard_SchoolProperties1_tblProps"]//td//text()').extract()
        report_scores = response.xpath('//table[@id="ctl00_ContentPlaceHolder1_detailedReportCard_tblReportCard"]//td').extract()

        # Get the basic information of school
        # In block of basic information, there are alwalys 6 lines, so set the constant 6
        if (len(block_info) == 6):
            school_name = block_info[0]
            school_sector = block_info[1]
            school_address = block_info[2]
            school_city = block_info[3].split(',')[0]
            school_postcode = block_info[3].split(',')[1].replace(' ','')[2:]
            school_phone = block_info[4]
            school_district = block_info[5]
        else:
            print("Length of block_info is not 6. School Name: {0}".format(block_info[0]))

        if school_website is None:
            school_website = "nd"

        # Get the information of recent year
        if (len(report_info) == 13):
            # Gr 12 Enrollment, ESL (%), Special needs (%)
            # Alt. French (%), Parents' average income ($), Actual rating vs. predicted based on parents' avg. inc.
            school_student, school_esl, school_speneeds, school_frenchi, school_aveincome, school_actrating = report_info[2::2]
        else:
            print("Length of report_info is not 13. School Name: {0}".format(block_info[0]))

        # Get the information of recent settings['YEARS_NUM'] years scores data
        # Get the rows and colums from setting page
        imax = settings['SCORES_NUM']
        jmax = settings['YEARS_NUM']
        if (len(report_scores) == ((jmax+2)*(imax+1))):
            a = [['nd']*jmax for i in range(imax)]
            
            # replace "," to "." for Quebec Schools
            for i in range(imax):
                for j in range(jmax):
                    a[i][j] = report_scores[(i+1)*(jmax+2)+(j+1)][4:-5].replace(',', '.')
            
            # 9 arguments: 
            # Average exam mark, Percentage of exams failed, School vs exam mark difference,
            # Language Arts gender gap, Math gender gap, Courses taken per student, 
            # Diploma completion rate, Delayed advancement rate, Overall rating out of 10
            score_avgmark, score_failed, score_markdiff, score_genlang, score_genmath, score_coursetk, score_dplrate, score_delayed, score_all = a

        else:
            print("Length of report_score is not {0}x{1}. School Name: {2}".format(jmax, imax, block_info[0]))
        

        abs_item = AlbertasecondaryItem()
        for field in abs_item.fields:
            try:
                abs_item[field] = eval(field)
            except NameError:
                self.logger.debug('Field is Not Defined: ' + field)
        yield abs_item
