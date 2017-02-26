import sqlite3 as lite
import requests
import time


def setup_db_con(fname="../HotSCompetitive.sqlite"):
    """ Opening the connection to the database """
    print('Opening connection...')
    con = lite.connect(fname)
    cur = con.cursor()
    return con, cur


def update_db_tournament(con, cur):
    """ Adding the necessary tournament and stage lookup information to the
    database """

    print('Getting Tournament Information')

    # Opening requests session and getting json data of tournaments
    sesh = requests.Session()
    req = sesh.get("https://api.masterleague.net/tournaments.json")

    # Looping through all of the results and inserting them into
    # the sqlite database
    print('Updating Database...')
    while True:
        for i in range(len(req.json()['results'])):
            # pulling out the values
            tourn_id = req.json()['results'][i]['id']
            name = req.json()['results'][i]['name']
            start_date = req.json()['results'][i]['start_date']
            end_date = req.json()['results'][i]['end_date']
            region = req.json()['results'][i]['region']

            # Trying to update first
            cur.execute("UPDATE tournaments \
            SET name=?, start_date=?, end_date=?, region=? \
            WHERE id=?", \
            (name, start_date, end_date, region, tourn_id))


            # inserting them if the update failed
            if cur.rowcount == 0:
                cur.execute("INSERT INTO tournaments(\
                id, name, start_date, end_date, region) \
                VALUES( ?, ?, ?, ?, ? )", \
                ( \
                    tourn_id, name, start_date, end_date, region \
                ))

            # committing changes to the database
            con.commit()

            # Now we need to insert the stages, checking to see if there are
            # any stages first
            if len(req.json()['results'][i]['stages']) != 0:
                for j in range(len(req.json()['results'][i]['stages'])):
                    # getting the values
                    stage_id = req.json()['results'][i]['stages'][j]['id']
                    stage_name = req.json()['results'][i]['stages'][j]['name']

                    # trying to update
                    cur.execute("UPDATE stages \
                    SET name=?, tournament_id=? \
                    WHERE id=?", \
                    (stage_name, tourn_id, stage_id))

                    # inserting if no rows were updated
                    if cur.rowcount == 0:
                        cur.execute("INSERT INTO stages(\
                        id, name, tournament_id ) \
                        VALUES( ?, ?, ? )", \
                        ( \
                            stage_id, stage_name, tourn_id
                        ))

                    con.commit()


        # Getting next page if necessary, otherwise breaking out of
        # the loop
        if req.json()['next'] is None:
            break
        else:
            time.sleep(0.5)  # can't submit more than 2 API requests/sec
            req = sesh.get(req.json()['next'])


def update_db_teams(con, cur):
    """ Updates the database with team info, like region """
    print('Getting Team Information')

    # Opening requests session and getting json data of teams
    sesh = requests.Session()
    req = sesh.get("https://api.masterleague.net/teams.json?page_size=100")

    # Looping through all of the results and inserting them into
    # the sqlite database
    print('Updating Database...')
    while True:
        for i in range(len(req.json()['results'])):
            # pulling out the values
            team_id = req.json()['results'][i]['id']
            team_name = req.json()['results'][i]['name']
            region = req.json()['results'][i]['region']

            # trying to update first
            cur.execute("UPDATE teams \
            SET name=?, region=? \
            WHERE id=?", \
            (team_name, region, team_id))

            # inserting them if update fails
            if cur.rowcount == 0:
                cur.execute("INSERT INTO teams(\
                id, name, region ) \
                VALUES( ?, ?, ? )", \
                ( \
                    team_id, team_name, region \
                ))

            # committing changes to the database
            con.commit()

        # Getting next page if necessary, otherwise breaking out of
        # the loop
        if req.json()['next'] is None:
            break
        else:
            time.sleep(0.5)  # can't submit more than 2 API requests/sec
            req = sesh.get(req.json()['next'])


def update_db_players(con, cur):
    """ Updates the database with player info, like team """
    print('Getting Player Information')

    # Opening requests session and getting json data of teams
    sesh = requests.Session()
    req = sesh.get("https://api.masterleague.net/players.json?page_size=100")

    # Looping through all of the results and inserting them into
    # the sqlite database
    print('Updating Database...')
    while True:
        for i in range(len(req.json()['results'])):
            # pulling out the values
            player_id = req.json()['results'][i]['id']
            player_team = req.json()['results'][i]['team']
            player_region = req.json()['results'][i]['region']
            player_nickname = req.json()['results'][i]['nickname']
            player_name = req.json()['results'][i]['realname']
            player_country = req.json()['results'][i]['country']
            player_role = req.json()['results'][i]['role']

            # updating if possible
            cur.execute("UPDATE players \
            SET team=?, region=?, nickname=?, realname=?, country=?, role=? \
            where id = ?", \
            (player_team, player_region, player_nickname, player_name, \
            player_country, player_role, player_id))


            # inserting them if the update failed
            cur.execute("INSERT INTO players(\
            id, team, region, nickname, realname, country, role) \
            VALUES( ?, ?, ?, ?, ?, ?, ? )", \
            ( \
                player_id, player_team, player_region, player_nickname, \
                player_name, player_country, player_role \
            ))

            # committing changes to the database
            con.commit()

        # Getting next page if necessary, otherwise breaking out of
        # the loop
        if req.json()['next'] is None:
            break
        else:
            time.sleep(0.5)  # can't submit more than 2 API requests/sec
            req = sesh.get(req.json()['next'])


def update_db_patches(con, cur):
    """ Updates the database with patch info. """
    print('Getting Patch Information')

    # Opening requests session and getting json data of patches
    sesh = requests.Session()
    req = sesh.get("https://api.masterleague.net/patches.json")

    # Looping through the results and inserting them
    print('Updating Database...')
    for i in range(len(req.json())):
        # pulling out the values
        patch_id = req.json()[i]['id']
        patch_name = req.json()[i]['name']
        patch_from_dt = req.json()[i]['from_date']
        patch_to_dt = req.json()[i]['to_date']

        # trying to update first
        cur.execute("UPDATE patches \
        SET name=?, from_date=?, to_date=? \
        WHERE id=?", \
        (patch_name, patch_from_dt, patch_to_dt, patch_id))

        # inserting them if update fails
        if cur.rowcount == 0:
            cur.execute("INSERT INTO patches(\
            id, name, from_date, to_date ) \
            VALUES( ?, ?, ?, ? )", \
            ( \
                patch_id, patch_name, patch_from_dt, patch_to_dt \
            ))

    # committing changes to the database
    con.commit()
    # no next page this time, so just return when the for loop is done


def update_db_match_basic(con, cur, match_id):
    """ updates the match table with patch, tournament, stage, and game """
    print('Getting Match Information')

    # Opening requests session and getting json data for a specific match
    sesh = requests.Session()
    req = sesh.get("https://api.masterleague.net/matches/" + str(match_id) +
                   ".json")

    # looping through the information and updating the information
    # the information should be in the database already from the web scraper
    print('Updating Database...')

    # pulling out the extra values and making sure
    match_patch = req.json()['patch']
    # need to check to see if the value exists, and update if
    # it does not. The update function updates the entire table. It does not
    # just insert the new value. Since id is the primary key, it will not
    # change
    check_patch = cur.execute("select id from patches where id=?",
                              (str(match_patch), ))
    if check_patch.fetchone() is None:
        # if none, then does not exist, run code
        update_db_patches(con, cur)

    # now checking tournament info
    match_tourn = req.json()['tournament']
    check_tourn = cur.execute("select id from tournaments where id=?",
                              (str(match_tourn), ))
    if check_tourn.fetchone() is None:
        update_db_tournament(con, cur)

    match_stage = req.json()['stage']  # no need to check stages, tournament updates it
    match_game = req.json()['game']  # game does not have a lookup table since
                                     # it is not unique

    # updating the match_basic table
    cur.execute("UPDATE match_basic \
    SET patch=?, tournament=?, stage=?, game=? \
    WHERE match_id=?", \
    (match_patch, match_tourn, match_stage, match_game, match_id))

    # committing changes
    con.commit()


def close_db(con):
    """ Closing the connection to the database """
    con.close()  # closing the connection
    print('Connection closed! (and hopefully a success)')

if __name__ == "__main__":
    # just runs through all 4 of the reference table updates
    CONN, CURR = setup_db_con()
    update_db_tournament(CONN, CURR)
    update_db_teams(CONN, CURR)
    update_db_players(CONN, CURR)
    update_db_patches(CONN, CURR)
    close_db(CONN)
