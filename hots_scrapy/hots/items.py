# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotsItem(scrapy.Item):
    # Basic match info
    match_id = scrapy.Field()
    match_date = scrapy.Field()
    map_name = scrapy.Field()
    home_team = scrapy.Field()
    away_team = scrapy.Field()
    score = scrapy.Field()
    duration = scrapy.Field()    # This is from statistics
    home_level = scrapy.Field()  # Final level of home team
    away_level = scrapy.Field()

    # Bans
    home_ban1 = scrapy.Field()
    home_ban2 = scrapy.Field()
    away_ban1 = scrapy.Field()
    away_ban2 = scrapy.Field()

    # Basic home player info
    home_p1 = scrapy.Field()
    home_p1_hero = scrapy.Field()
    home_p2 = scrapy.Field()
    home_p2_hero = scrapy.Field()
    home_p3 = scrapy.Field()
    home_p3_hero = scrapy.Field()
    home_p4 = scrapy.Field()
    home_p4_hero = scrapy.Field()
    home_p5 = scrapy.Field()
    home_p5_hero = scrapy.Field()

    # Basic away player info
    away_p1 = scrapy.Field()
    away_p1_hero = scrapy.Field()
    away_p2 = scrapy.Field()
    away_p2_hero = scrapy.Field()
    away_p3 = scrapy.Field()
    away_p3_hero = scrapy.Field()
    away_p4 = scrapy.Field()
    away_p4_hero = scrapy.Field()
    away_p5 = scrapy.Field()
    away_p5_hero = scrapy.Field()

    # Advanced information
    home_p1_kills = scrapy.Field()
    home_p1_assists = scrapy.Field()
    home_p1_deaths = scrapy.Field()
    home_p1_siege = scrapy.Field()
    home_p1_hero_dmg = scrapy.Field()
    home_p1_role_val = scrapy.Field()
    home_p1_exp = scrapy.Field()

    home_p2_kills = scrapy.Field()
    home_p2_assists = scrapy.Field()
    home_p2_deaths = scrapy.Field()
    home_p2_siege = scrapy.Field()
    home_p2_hero_dmg = scrapy.Field()
    home_p2_role_val = scrapy.Field()
    home_p2_exp = scrapy.Field()

    home_p3_kills = scrapy.Field()
    home_p3_assists = scrapy.Field()
    home_p3_deaths = scrapy.Field()
    home_p3_siege = scrapy.Field()
    home_p3_hero_dmg = scrapy.Field()
    home_p3_role_val = scrapy.Field()
    home_p3_exp = scrapy.Field()

    home_p4_kills = scrapy.Field()
    home_p4_assists = scrapy.Field()
    home_p4_deaths = scrapy.Field()
    home_p4_siege = scrapy.Field()
    home_p4_hero_dmg = scrapy.Field()
    home_p4_role_val = scrapy.Field()
    home_p4_exp = scrapy.Field()

    home_p5_kills = scrapy.Field()
    home_p5_assists = scrapy.Field()
    home_p5_deaths = scrapy.Field()
    home_p5_siege = scrapy.Field()
    home_p5_hero_dmg = scrapy.Field()
    home_p5_role_val = scrapy.Field()
    home_p5_exp = scrapy.Field()

    away_p1_kills = scrapy.Field()
    away_p1_assists = scrapy.Field()
    away_p1_deaths = scrapy.Field()
    away_p1_siege = scrapy.Field()
    away_p1_hero_dmg = scrapy.Field()
    away_p1_role_val = scrapy.Field()
    away_p1_exp = scrapy.Field()

    away_p2_kills = scrapy.Field()
    away_p2_assists = scrapy.Field()
    away_p2_deaths = scrapy.Field()
    away_p2_siege = scrapy.Field()
    away_p2_hero_dmg = scrapy.Field()
    away_p2_role_val = scrapy.Field()
    away_p2_exp = scrapy.Field()

    away_p3_kills = scrapy.Field()
    away_p3_assists = scrapy.Field()
    away_p3_deaths = scrapy.Field()
    away_p3_siege = scrapy.Field()
    away_p3_hero_dmg = scrapy.Field()
    away_p3_role_val = scrapy.Field()
    away_p3_exp = scrapy.Field()

    away_p4_kills = scrapy.Field()
    away_p4_assists = scrapy.Field()
    away_p4_deaths = scrapy.Field()
    away_p4_siege = scrapy.Field()
    away_p4_hero_dmg = scrapy.Field()
    away_p4_role_val = scrapy.Field()
    away_p4_exp = scrapy.Field()

    away_p5_kills = scrapy.Field()
    away_p5_assists = scrapy.Field()
    away_p5_deaths = scrapy.Field()
    away_p5_siege = scrapy.Field()
    away_p5_hero_dmg = scrapy.Field()
    away_p5_role_val = scrapy.Field()
    away_p5_exp = scrapy.Field()
