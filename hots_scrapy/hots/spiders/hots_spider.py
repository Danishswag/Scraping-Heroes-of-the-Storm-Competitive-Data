import scrapy                    # The basis of everything
import re                        # Want this for extracting game num from url
from hots.items import HotsItem  # The item I created earlier


class HotsSpider(scrapy.Spider):
    # Basic spider information
    name = "hots"

    def __init__(self, match_id=2038, *args, **kwargs):
        self.allowed_domains = ["masterleague.net"]
        self.start_urls = [
            'https://masterleague.net/match/{}/'.format(match_id)
        ]

    def parse(self, response):
        item = HotsItem()
        item['match_date'] = response.xpath('/html/body/div/ol/li[6]/text()').extract_first()

        for match in response.xpath('//*[@id="draft"]'):
            # Scraping basic match information
            item['map_name'] = match.xpath('div[5]/div[2]/span/text()').extract_first()
            item['home_team'] = match.xpath('div[1]/div[1]/div/div[1]/h2/a/text()').extract_first()
            item['away_team'] = match.xpath('div[1]/div[2]/div/div[2]/h2/a/text()').extract_first()

            # Bans
            item['home_ban1'] = match.xpath('div[5]/div[1]/div[1]/a/img/@title').extract_first()
            item['home_ban2'] = match.xpath('div[5]/div[1]/div[2]/a/img/@title').extract_first()
            item['away_ban1'] = match.xpath('div[5]/div[3]/div[2]/a/img/@title').extract_first()
            item['away_ban2'] = match.xpath('div[5]/div[3]/div[1]/a/img/@title').extract_first()

            # Checking for winner and making the score correct for PlayerRatings
            outcome = match.xpath('//div[1]/div[1]/div/div[1]/span/text()').extract_first()
            if outcome == 'WINNER':
                item['score'] = 1
            else:
                item['score'] = 0

        # Now checking if there are statistics and downloading a second page if so
        # Depending on if watch or anythign else has been added, need to check other
        # column too.
        stat_check = response.xpath('/html/body/div/ul/li[3]/a/text()').extract_first()
        stat_check2 = response.xpath('/html/body/div/ul/li[4]/a/text()').extract_first()
        if (stat_check == 'Statistics') or (stat_check2 == 'Statistics'):
            request = scrapy.Request(response.request.url + 'stats/', callback=self.parseStats)
            request.meta['item'] = item
            yield request
        else:
            for pdata in response.xpath('//*[@id="draft"]/div[3]'):
                # Need to get basic player information from draft tag
                # Home Player 1
                item['home_p1'] = pdata.xpath('div[1]/div[1]/a[2]/text()').extract_first()
                item['home_p1_hero'] = pdata.xpath('div[1]/div[1]/a[1]/img/@title').extract_first()

                # Home Player 2
                item['home_p2'] = pdata.xpath('div[1]/div[2]/a[2]/text()').extract_first()
                item['home_p2_hero'] = pdata.xpath('div[1]/div[2]/a[1]/img/@title').extract_first()

                # Home Player 3
                item['home_p3'] = pdata.xpath('div[1]/div[3]/a[2]/text()').extract_first()
                item['home_p3_hero'] = pdata.xpath('div[1]/div[3]/a[1]/img/@title').extract_first()

                # Home Player 4
                item['home_p4'] = pdata.xpath('div[1]/div[4]/a[2]/text()').extract_first()
                item['home_p4_hero'] = pdata.xpath('div[1]/div[4]/a[1]/img/@title').extract_first()

                # Home Player 5
                item['home_p5'] = pdata.xpath('div[1]/div[5]/a[2]/text()').extract_first()
                item['home_p5_hero'] = pdata.xpath('div[1]/div[5]/a[1]/img/@title').extract_first()

                # Away Player 1
                item['away_p1'] = pdata.xpath('div[2]/div[1]/a[2]/text()').extract_first()
                item['away_p1_hero'] = pdata.xpath('div[2]/div[1]/a[1]/img/@title').extract_first()

                # Away Player 2
                item['away_p2'] = pdata.xpath('div[2]/div[2]/a[2]/text()').extract_first()
                item['away_p2_hero'] = pdata.xpath('div[2]/div[2]/a[1]/img/@title').extract_first()

                # Away Player 3
                item['away_p3'] = pdata.xpath('div[2]/div[3]/a[2]/text()').extract_first()
                item['away_p3_hero'] = pdata.xpath('div[2]/div[3]/a[1]/img/@title').extract_first()

                # Away Player 4
                item['away_p4'] = pdata.xpath('div[2]/div[4]/a[2]/text()').extract_first()
                item['away_p4_hero'] = pdata.xpath('div[2]/div[4]/a[1]/img/@title').extract_first()

                # Away Player 5
                item['away_p5'] = pdata.xpath('div[2]/div[5]/a[2]/text()').extract_first()
                item['away_p5_hero'] = pdata.xpath('div[2]/div[5]/a[1]/img/@title').extract_first()

            # Checking for a next match
            prev_id = int(''.join(list(filter(str.isdigit, response.request.url))))
            item['match_id'] = prev_id
            # 36 is with 4 digit match id, 35 for 3 digit, 37 for >= 10000
            if len(response.request.url) == 36:
                next_page_url = response.request.url[:-5] + str(prev_id+1) + '/'
            elif len(response.request.url) == 35:
                next_page_url = response.request.url[:-4] + str(prev_id+1) + '/'
            elif len(response.request.url) == 37:
                next_page_url = response.request.url[:-6] + str(prev_id+1) + '/'
            if outcome is not None:
                yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

            yield item

#####################################################################


    def parseStats(self, response):
        item = response.meta['item']
        # Starting with the levels of each team
        item['home_level'] = int(response.xpath('/html/body/div[1]/div[1]/div[2]/span[2]/text()').extract_first().strip()[6:])
        item['away_level'] = int(response.xpath('/html/body/div[1]/div[5]/div[2]/span[1]/text()').extract_first().strip()[6:])
        item['duration'] = response.xpath('/html/body/div[1]/div[3]/div[2]/text()').extract_first()

        # Getting player names, heroes, and stats
        for pdata in response.xpath('/html/body/div[2]/div/div[1]/table/tbody'):
            # Home Player 1
            item['home_p1'] = pdata.xpath('tr[1]/td[2]/a/strong/text()').extract_first()
            item['home_p1_hero'] = pdata.xpath('tr[1]/td[1]/div/a/img/@title').extract_first()
            item['home_p1_kills'] = float(pdata.xpath('tr[1]/td[3]/text()').extract_first())
            item['home_p1_assists'] = float(pdata.xpath('tr[1]/td[4]/text()').extract_first())
            item['home_p1_deaths'] = float(pdata.xpath('tr[1]/td[5]/text()').extract_first())
            item['home_p1_siege'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[1]/td[6]').xpath("string()").extract_first()))))
            item['home_p1_hero_dmg'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[1]/td[7]').xpath("string()").extract_first()))))
            item['home_p1_role_val'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[1]/td[8]').xpath("string()").extract_first()))))
            item['home_p1_exp'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[1]/td[9]').xpath("string()").extract_first()))))

            # Home Player 2
            item['home_p2'] = pdata.xpath('tr[2]/td[2]/a/strong/text()').extract_first()
            item['home_p2_hero'] = pdata.xpath('tr[2]/td[1]/div/a/img/@title').extract_first()
            item['home_p2_kills'] = float(pdata.xpath('tr[2]/td[3]/text()').extract_first())
            item['home_p2_assists'] = float(pdata.xpath('tr[2]/td[4]/text()').extract_first())
            item['home_p2_deaths'] = float(pdata.xpath('tr[2]/td[5]/text()').extract_first())
            item['home_p2_siege'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[2]/td[6]').xpath("string()").extract_first()))))
            item['home_p2_hero_dmg'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[2]/td[7]').xpath("string()").extract_first()))))
            item['home_p2_role_val'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[2]/td[8]').xpath("string()").extract_first()))))
            item['home_p2_exp'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[2]/td[9]').xpath("string()").extract_first()))))

            # Home Player 3
            item['home_p3'] = pdata.xpath('tr[3]/td[2]/a/strong/text()').extract_first()
            item['home_p3_hero'] = pdata.xpath('tr[3]/td[1]/div/a/img/@title').extract_first()
            item['home_p3_kills'] = float(pdata.xpath('tr[3]/td[3]/text()').extract_first())
            item['home_p3_assists'] = float(pdata.xpath('tr[3]/td[4]/text()').extract_first())
            item['home_p3_deaths'] = float(pdata.xpath('tr[3]/td[5]/text()').extract_first())
            item['home_p3_siege'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[3]/td[6]').xpath("string()").extract_first()))))
            item['home_p3_hero_dmg'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[3]/td[7]').xpath("string()").extract_first()))))
            item['home_p3_role_val'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[3]/td[8]').xpath("string()").extract_first()))))
            item['home_p3_exp'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[3]/td[9]').xpath("string()").extract_first()))))

            # Home Player 4
            item['home_p4'] = pdata.xpath('tr[4]/td[2]/a/strong/text()').extract_first()
            item['home_p4_hero'] = pdata.xpath('tr[4]/td[1]/div/a/img/@title').extract_first()
            item['home_p4_kills'] = float(pdata.xpath('tr[4]/td[3]/text()').extract_first())
            item['home_p4_assists'] = float(pdata.xpath('tr[4]/td[4]/text()').extract_first())
            item['home_p4_deaths'] = float(pdata.xpath('tr[4]/td[5]/text()').extract_first())
            item['home_p4_siege'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[4]/td[6]').xpath("string()").extract_first()))))
            item['home_p4_hero_dmg'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[4]/td[7]').xpath("string()").extract_first()))))
            item['home_p4_role_val'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[4]/td[8]').xpath("string()").extract_first()))))
            item['home_p4_exp'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[4]/td[9]').xpath("string()").extract_first()))))

            # Home Player 5
            item['home_p5'] = pdata.xpath('tr[5]/td[2]/a/strong/text()').extract_first()
            item['home_p5_hero'] = pdata.xpath('tr[5]/td[1]/div/a/img/@title').extract_first()
            item['home_p5_kills'] = float(pdata.xpath('tr[5]/td[3]/text()').extract_first())
            item['home_p5_assists'] = float(pdata.xpath('tr[5]/td[4]/text()').extract_first())
            item['home_p5_deaths'] = float(pdata.xpath('tr[5]/td[5]/text()').extract_first())
            item['home_p5_siege'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[5]/td[6]').xpath("string()").extract_first()))))
            item['home_p5_hero_dmg'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[5]/td[7]').xpath("string()").extract_first()))))
            item['home_p5_role_val'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[5]/td[8]').xpath("string()").extract_first()))))
            item['home_p5_exp'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[5]/td[9]').xpath("string()").extract_first()))))

            # Away Player 1
            item['away_p1'] = pdata.xpath('tr[6]/td[2]/a/strong/text()').extract_first()
            item['away_p1_hero'] = pdata.xpath('tr[6]/td[1]/div/a/img/@title').extract_first()
            item['away_p1_kills'] = float(pdata.xpath('tr[6]/td[3]/text()').extract_first())
            item['away_p1_assists'] = float(pdata.xpath('tr[6]/td[4]/text()').extract_first())
            item['away_p1_deaths'] = float(pdata.xpath('tr[6]/td[5]/text()').extract_first())
            item['away_p1_siege'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[6]/td[6]').xpath("string()").extract_first()))))
            item['away_p1_hero_dmg'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[6]/td[7]').xpath("string()").extract_first()))))
            item['away_p1_role_val'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[6]/td[8]').xpath("string()").extract_first()))))
            item['away_p1_exp'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[6]/td[9]').xpath("string()").extract_first()))))

            # Away Player 2
            item['away_p2'] = pdata.xpath('tr[7]/td[2]/a/strong/text()').extract_first()
            item['away_p2_hero'] = pdata.xpath('tr[7]/td[1]/div/a/img/@title').extract_first()
            item['away_p2_kills'] = float(pdata.xpath('tr[7]/td[3]/text()').extract_first())
            item['away_p2_assists'] = float(pdata.xpath('tr[7]/td[4]/text()').extract_first())
            item['away_p2_deaths'] = float(pdata.xpath('tr[7]/td[5]/text()').extract_first())
            item['away_p2_siege'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[7]/td[6]').xpath("string()").extract_first()))))
            item['away_p2_hero_dmg'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[7]/td[7]').xpath("string()").extract_first()))))
            item['away_p2_role_val'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[7]/td[8]').xpath("string()").extract_first()))))
            item['away_p2_exp'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[7]/td[9]').xpath("string()").extract_first()))))

            # Away Player 3
            item['away_p3'] = pdata.xpath('tr[8]/td[2]/a/strong/text()').extract_first()
            item['away_p3_hero'] = pdata.xpath('tr[8]/td[1]/div/a/img/@title').extract_first()
            item['away_p3_kills'] = float(pdata.xpath('tr[8]/td[3]/text()').extract_first())
            item['away_p3_assists'] = float(pdata.xpath('tr[8]/td[4]/text()').extract_first())
            item['away_p3_deaths'] = float(pdata.xpath('tr[8]/td[5]/text()').extract_first())
            item['away_p3_siege'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[8]/td[6]').xpath("string()").extract_first()))))
            item['away_p3_hero_dmg'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[8]/td[7]').xpath("string()").extract_first()))))
            item['away_p3_role_val'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[8]/td[8]').xpath("string()").extract_first()))))
            item['away_p3_exp'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[8]/td[9]').xpath("string()").extract_first()))))

            # Away Player 4
            item['away_p4'] = pdata.xpath('tr[9]/td[2]/a/strong/text()').extract_first()
            item['away_p4_hero'] = pdata.xpath('tr[9]/td[1]/div/a/img/@title').extract_first()
            item['away_p4_kills'] = float(pdata.xpath('tr[9]/td[3]/text()').extract_first())
            item['away_p4_assists'] = float(pdata.xpath('tr[9]/td[4]/text()').extract_first())
            item['away_p4_deaths'] = float(pdata.xpath('tr[9]/td[5]/text()').extract_first())
            item['away_p4_siege'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[9]/td[6]').xpath("string()").extract_first()))))
            item['away_p4_hero_dmg'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[9]/td[7]').xpath("string()").extract_first()))))
            item['away_p4_role_val'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[9]/td[8]').xpath("string()").extract_first()))))
            item['away_p4_exp'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[9]/td[9]').xpath("string()").extract_first()))))

            # Away Player 5
            item['away_p5'] = pdata.xpath('tr[10]/td[2]/a/strong/text()').extract_first()
            item['away_p5_hero'] = pdata.xpath('tr[10]/td[1]/div/a/img/@title').extract_first()
            item['away_p5_kills'] = float(pdata.xpath('tr[10]/td[3]/text()').extract_first())
            item['away_p5_assists'] = float(pdata.xpath('tr[10]/td[4]/text()').extract_first())
            item['away_p5_deaths'] = float(pdata.xpath('tr[10]/td[5]/text()').extract_first())
            item['away_p5_siege'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[10]/td[6]').xpath("string()").extract_first()))))
            item['away_p5_hero_dmg'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[10]/td[7]').xpath("string()").extract_first()))))
            item['away_p5_role_val'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[10]/td[8]').xpath("string()").extract_first()))))
            item['away_p5_exp'] = int(''.join(list(filter(str.isdigit, pdata.xpath('tr[10]/td[9]').xpath("string()").extract_first()))))

            # Now setting up the request to the next url in case there
            # actually was a statistics page

        # Checking for a next match
        prev_id = int(''.join(list(filter(str.isdigit, response.request.url))))
        item['match_id'] = prev_id
        # 36 is with 4 digit match id, 35 for 3 digit, 37 for >= 10000
        if len(response.request.url) == 42:
            next_page_url = response.request.url[:-11] + str(prev_id+1) + '/'
        elif len(response.request.url) == 41:
            next_page_url = response.request.url[:-10] + str(prev_id+1) + '/'
        elif len(response.request.url) == 43:
            next_page_url = response.request.url[:-12] + str(prev_id+1) + '/'
        yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
        yield item

