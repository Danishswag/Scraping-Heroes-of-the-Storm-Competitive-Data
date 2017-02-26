import sqlite3 as lite
from datetime import datetime
import update_sqlite as update # should be in directory

con = None  # db connection


class HotsPipeline(object):
    def process_item(self, item, spider):
        """ Pipeline object for it to return the item """
        return item

class SQLiteStorePipeline(object):
    filename = 'HotSCompetitive.sqlite'

    def __init__(self):
        self.setup_db_con()
        self.create_match_table


    def process_item(self, item, spider):
        """ Sends the item to the processing function and returns it """
        self.store_in_db(item)
        return item


    def store_in_db(self, item):
        """ Stores all items in the database """
        # Stores information if there is no replay available to get stats
        # Only uses some of the fields in the tables

        # Calculating the week and adjusting the date for an
        # appropriate format
        self.cur.execute("SELECT date FROM match_basic ORDER BY ROWID ASC LIMIT 1")
        m_date1_str = self.cur.fetchall()[0][0]  # should always have one entry
        m_date1_obj = datetime.strptime(m_date1_str, '%Y-%m-%d')
        try:
            m_date2_obj = datetime.strptime(item['match_date'], '%b. %d, %Y')
        except ValueError:
            pass
        try:
            m_date2_obj = datetime.strptime(item['match_date'], '%B %d, %Y')
        except ValueError:
            pass

        # Finding the number of weeks difference and adding one
        # for player ratings
        delta = m_date2_obj - m_date1_obj
        weeks = int(delta.days / 7) + 1  # Remember int rounds down

        # Converting the match date to a correct string
        m_date2_str = datetime.strftime(m_date2_obj, '%Y-%m-%d')

        # Inserting the match data into the database
        self.cur.execute("INSERT INTO match_basic(\
        match_id, date, week, home_team, away_team, score, map, home_ban1, \
        home_ban2, away_ban1, away_ban2 ) \
        VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
        (
            item['match_id'], m_date2_str, weeks,
            item['home_team'], item['away_team'], item['score'],
            item['map_name'], item['home_ban1'], item['home_ban2'],
            item['away_ban1'], item['away_ban2']
        ))

        # Inserting the player details into the database
        # when no stats are available. MATCH_ID and TEAM_NAME
        # should match relevant entries in match_basic
        for i in range(5):
            # Choosing player and adjusting index
            player_id = str(i + 1)

            # starting with the home players
            self.cur.execute("INSERT INTO player_details(\
            match_id, date, team_name, player_name, hero_name) \
            VALUES( ?, ?, ?, ?, ? )",
            (
                item['match_id'], m_date2_str, item['home_team'],
                item['home_p' + player_id], item['home_p' + player_id + '_hero']
            ))

            # now updating the away players
            self.cur.execute("INSERT INTO player_details(\
            match_id, date, team_name, player_name, hero_name) \
            VALUES( ?, ?, ?, ?, ? )",
            (
                item['match_id'], m_date2_str, item['away_team'],
                item['away_p' + player_id],
                item['away_p' + player_id + '_hero']
            ))
        self.con.commit()

        # Checking if the item is long enough to contain full stats
        # info and updating the previous entries if it does.
        if len(item) > 35:
            # Adding duration to match_basic
            self.cur.execute("UPDATE match_basic \
            SET duration=? WHERE match_id=?", (item['duration'], item['match_id']))

            # Updating player_details
            for i in range(5):
                # Choosing player and adjusting index
                player_id = str(i + 1)

                # updating player_details with the extra info, home first
                self.cur.execute("UPDATE player_details \
                SET kills=?, assists=?, deaths=?, siege_damage=?, \
                hero_damage=?, role_val=?, exp=? \
                WHERE match_id=? AND player_name=?", \
                (
                    item['home_p' + player_id + '_kills'],
                    item['home_p' + player_id + '_assists'],
                    item['home_p' + player_id + '_deaths'],
                    item['home_p' + player_id + '_siege'],
                    item['home_p' + player_id + '_hero_dmg'],
                    item['home_p' + player_id + '_role_val'],
                    item['home_p' + player_id + '_exp'],
                    item['match_id'], item['home_p' + player_id]
                ))

                self.cur.execute("UPDATE player_details \
                SET kills=?, assists=?, deaths=?, siege_damage=?, \
                hero_damage=?, role_val=?, exp=? \
                WHERE match_id=? AND player_name=?", \
                (
                    item['away_p' + player_id + '_kills'],
                    item['away_p' + player_id + '_assists'],
                    item['away_p' + player_id + '_deaths'],
                    item['away_p' + player_id + '_siege'],
                    item['away_p' + player_id + '_hero_dmg'],
                    item['away_p' + player_id + '_role_val'],
                    item['away_p' + player_id + '_exp'],
                    item['match_id'], item['away_p' + player_id]
                ))
            self.con.commit()

        # Now updating more info with API that is not easily available on the
        # webpage to scrape
        update.update_db_match_basic(self.con, self.cur, item['match_id'])


    def setup_db_con(self):
        """ Sets up the database connection """
        self.con = lite.connect('HotSCompetitive.sqlite')
        self.cur = self.con.cursor()


    def __del__(self):
        self.close_db()


    def create_match_table(self):
        """ Creates the match tables if they do not exist yet """
        # first creating match_basic
        self.cur.execute("CREATE TABLE IF NOT EXISTS match_basic(\
        match_id INTEGER NOT NULL, date TEXT NOT NULL, week TEXT, \
        home_team TEXT NOT NULL, away_team TEXT NOT NULL, \
        score INTEGER NOT NULL, map TEXT, duration INTEGER, \
        home_ban1 TEXT, home_ban2 TEXT, away_ban1 TEXT, away_ban2 TEXT, \
        patch INTEGER, tournament INTEGER, stage INTEGER, game INTEGER \
        PRIMARY KEY(match_id))")

        # now creating player_details
        self.cur.execute("CREATE TABLE IF NOT EXISTS `player_details`(\
        `match_id` INTEGER NOT NULL, `date` TEXT NOT NULL, \
        `team_name` TEST NOT NULL, `player_name` TEXT NOT NULL, \
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


    def close_db(self):
        """ Closing the connection to the database. """
        self.con.close() # definitely need to make sure con closed
