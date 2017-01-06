import sqlite3 as lite
from datetime import datetime

con = None  # db connection

class HotsPipeline(object):
    def process_item(self, item, spider):
        return item

class SQLiteStorePipeline(object):
    filename = 'HotSCompetitive.sqlite'

    def __init__(self):
        self.setupDBcon()
        self.createMatchTable

    def process_item(self, item, spider):
        self.storeInDB(item)
        return item

    def storeInDB(self, item):
        # Stores information if there is no replay available to get stats
        # Only uses some of the fields in the tables

        # Calculating the week and adjusting the date for an
        # appropriate format
        self.cur.execute("SELECT date FROM match_basic ORDER BY ROWID ASC LIMIT 1")
        m_date1_str = self.cur.fetchall()[0][0]  # should always have one entry
        m_date1_obj = datetime.strptime(m_date1_str, '%m/%d/%Y')
        try:
            print('1')
            m_date2_obj = datetime.strptime(item['match_date'], '%b. %d, %Y')
        except ValueError:
            pass
        try:
            print('2')
            m_date2_obj = datetime.strptime(item['match_date'], '%B %d, %Y')
        except ValueError:
            pass

        # Finding the number of weeks difference and adding one
        # for player ratings
        delta = m_date2_obj - m_date1_obj
        weeks = int(delta.days / 7) + 1  # Remember int rounds down

        # Converting the match date to a correct string
        m_date2_str = datetime.strftime(m_date2_obj, '%m/%d/%Y')

        # Inserting the match data into the database if only basic info is
        # available. The short should only include 30 objects
        if len(item) <= 35:
            self.cur.execute("INSERT INTO match_basic(\
            match_id, \
            date, \
            week, \
            home_team, \
            away_team, \
            score, \
            map, \
            home_ban1, \
            home_ban2, \
            away_ban1, \
            away_ban2 \
            ) \
            VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
            (
            item['match_id'],
            m_date2_str,
            weeks,
            item['home_team'],
            item['away_team'],
            item['score'],
            item['map_name'],
            item['home_ban1'],
            item['home_ban2'],
            item['away_ban1'],
            item['away_ban2']
            ))

            # Inserting the player details into the database
            # when no stats are available. MATCH_ID and TEAM_NAME
            # should match relevant entries in match_basic
            # Cycling through 5 rows, this time for home
            for i in range(5):
                # Choosing player and adjusting index
                player_id = str(i + 1)
                self.cur.execute("INSERT INTO player_details(\
                match_id, \
                date, \
                team_name, \
                player_name, \
                hero_name \
                ) \
                VALUES( ?, ?, ?, ?, ? )",
                (
                item['match_id'],
                m_date2_str,
                item['home_team'],
                item['home_p' + player_id],
                item['home_p' + player_id + '_hero']
                ))

            # Cycling through another 5 rows, this time for away
            for i in range(5):
                # Choosing player and adjusting index
                player_id = str(i + 1)
                self.cur.execute("INSERT INTO player_details(\
                match_id, \
                date, \
                team_name, \
                player_name, \
                hero_name \
                ) \
                VALUES( ?, ?, ?, ?, ? )",
                (
                item['match_id'],
                m_date2_str,
                item['away_team'],
                item['away_p' + player_id],
                item['away_p' + player_id + '_hero']
                ))
            self.con.commit()

        # Checking if the item is long enough to contain full stats
        # info and storing it in the database if it does. An alter
        # statement might make for shorter python code
        elif len(item) > 35:
            # Match Duration is now in the stats page
            self.cur.execute("INSERT INTO match_basic(\
            match_id, \
            date, \
            week, \
            home_team, \
            away_team, \
            score, \
            map, \
            home_ban1, \
            home_ban2, \
            away_ban1, \
            away_ban2, \
            duration \
            ) \
            VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
            (
            item['match_id'],
            m_date2_str,
            weeks,
            item['home_team'],
            item['away_team'],
            item['score'],
            item['map_name'],
            item['home_ban1'],
            item['home_ban2'],
            item['away_ban1'],
            item['away_ban2'],
            item['duration']
            ))
            
            # Home first
            for i in range(5):
                # Choosing player and adjusting index
                player_id = str(i + 1)
                self.cur.execute("INSERT INTO player_details(\
                match_id, \
                date, \
                team_name, \
                player_name, \
                hero_name, \
                kills, \
                assists, \
                deaths, \
                siege_damage, \
                hero_damage, \
                role_val, \
                exp \
                ) \
                VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
                (
                item['match_id'],
                m_date2_str,
                item['home_team'],
                item['home_p' + player_id],
                item['home_p' + player_id + '_hero'],
                item['home_p' + player_id + '_kills'],
                item['home_p' + player_id + '_assists'],
                item['home_p' + player_id + '_deaths'],
                item['home_p' + player_id + '_siege'],
                item['home_p' + player_id + '_hero_dmg'],
                item['home_p' + player_id + '_role_val'],
                item['home_p' + player_id + '_exp']
                ))
            
            # Away now
            for i in range(5):
                # Choosing player and adjusting index
                player_id = str(i + 1)
                self.cur.execute("INSERT INTO player_details(\
                match_id, \
                date, \
                team_name, \
                player_name, \
                hero_name, \
                kills, \
                assists, \
                deaths, \
                siege_damage, \
                hero_damage, \
                role_val, \
                exp \
                ) \
                VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
                (
                item['match_id'],
                m_date2_str,
                item['away_team'],
                item['away_p' + player_id],
                item['away_p' + player_id + '_hero'],
                item['away_p' + player_id + '_kills'],
                item['away_p' + player_id + '_assists'],
                item['away_p' + player_id + '_deaths'],
                item['away_p' + player_id + '_siege'],
                item['away_p' + player_id + '_hero_dmg'],
                item['away_p' + player_id + '_role_val'],
                item['away_p' + player_id + '_exp']
                ))
            self.con.commit()

    def setupDBcon(self):
        self.con = lite.connect('HotSCompetitive.sqlite')
        self.cur = self.con.cursor()

    def __del__(self):
        self.closeDB()

    def createMatchTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS match_basic(\
        match_id INTEGER NOT NULL, \
        date TEXT NOT NULL, \
        week TEXT, \
        home_team TEXT NOT NULL, \
        away_team TEXT NOT NULL, \
        score INTEGER NOT NULL, \
        map TEXT, \
        duration INTEGER, \
        home_ban1 TEXT, \
        home_ban2 TEXT, \
        away_ban1 TEXT, \
        away_ban2 TEXT \
        PRIMARY KEY(match_id) \
        )")
        self.cur.execute("CREATE TABLE IF NOT EXISTS `player_details`(\
        `match_id` INTEGER NOT NULL, \
        `date` TEXT NOT NULL, \
        `team_name` TEST NOT NULL, \
        `player_name` TEXT NOT NULL, \
    	`hero_name` TEXT NOT NULL, \
    	`kills` REAL, \
    	`assists` REAL, \
    	`deaths` REAL, \
    	`siege_damage` INTEGER, \
    	`hero_damage` INTEGER, \
    	`role_val` INTEGER, \
    	`exp` INTEGER, \
    	PRIMARY KEY(`match_id`) \
        )")

    def closeDB(self):
        self.con.close() # definitely need to make sure con closed