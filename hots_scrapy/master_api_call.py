import sqlite3 as lite
import requests
import time
from json.decoder import JSONDecodeError


def setup_db_con(fname="./HotSCompetitive.sqlite"):
    """ Opening the connection to the database """
    print('Opening connection...')
    con = lite.connect(fname)
    cur = con.cursor()
    return con, cur


def get_max_match():
    """ Getting the max match number on masterleague """

    print('Getting maximum match id')
    sesh = requests.Session()
    req = sesh.get("https://api.masterleague.net/matches.json")

    return req.json()['results'][0]['id']


def update_db_heroes(con, cur):
    """Updating the list of heroes in the database."""

    print('Getting hero information.')

    sesh = requests.Session()
    req = sesh.get("https://api.masterleague.net/heroes.json")
    print('Updating Database...')

    while True:
        for i in range(len(req.json()['results'])):
            hero_name = req.json()['results'][i]['name']
            hero_id = req.json()['results'][i]['id']
            hero_role = req.json()['results'][i]['role']

            # Trying to update
            cur.execute(("UPDATE heroes "
                         "   SET hero_name = ?, hero_role = ?, id = ? "
                         " WHERE hero_name = ?"), (hero_name, hero_role, hero_id,
                                                   hero_name))

            if cur.rowcount == 0:
                cur.execute(("INSERT INTO heroes( hero_name, hero_role, id) "
                             "VALUES(?, ?, ?)"), (hero_name, hero_role,
                                                  hero_id))
        if req.json()['next'] is None:
            break
        else:
            time.sleep(0.5)
            req = sesh.get(req.json()['next'])

    con.commit()


def update_db_talents(con, cur, game_version):
    """Gets all of the talents for each game version."""
    print('Getting talent information for game_version {0}.'.format(game_version))

    sesh = requests.Session()

    # Setting up the
    cur.execute("SELECT id FROM heroes")
    heroes = cur.fetchall()

    # Iterating through each hero already in the database
    for hero_id in heroes:
        hero_url = "https://api.masterleague.net/heroes/{0}.json/?game_version={1}".format(hero_id[0], game_version)
        req = sesh.get(hero_url)
        time.sleep(1)

        print(hero_id)  # comment out if not testing
        # Iterating through each tier + choice and updating/inserting
        try:
            for talent in req.json()['talents']:
                tier = talent['tier']
                choice = talent['choice']
                description = talent['description']
                name = talent['name']

                cur.execute(("UPDATE talents "
                             "   SET hero_id = ?, game_version = ?, tier = ?, "
                             "       choice = ?, description = ?, name=? "
                             " WHERE hero_id = ? AND game_version = ? AND tier = ? "
                             "   AND choice = ?"), (hero_id[0], game_version, tier,
                                                    choice, description, name,
                                                    hero_id[0], game_version,
                                                    tier, choice))

                if cur.rowcount == 0:
                    cur.execute(("INSERT INTO talents( hero_id, game_version, tier, "
                                 "            choice, description, name)"
                                 "     VALUES (?, ?, ?, ?, ?, ?)"),
                            (hero_id[0], game_version, tier, choice,
                             description, name))
        except JSONDecodeError:
            continue

    con.commit()


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
            cur.execute(("UPDATE tournaments "
                         "SET name=?, start_date=?, end_date=?, region=? "
                         "WHERE id=? "),
                        (name, start_date, end_date, region, tourn_id))

            # inserting them if the update failed
            if cur.rowcount == 0:
                cur.execute(("INSERT INTO tournaments( "
                             "id, name, start_date, end_date, region) "
                             "VALUES( ?, ?, ?, ?, ? )"),
                            (tourn_id, name, start_date, end_date, region))

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
                    cur.execute(("UPDATE stages "
                                 "SET name=?, tournament_id=? "
                                 "WHERE id=?"),
                                (stage_name, tourn_id, stage_id))

                    # inserting if no rows were updated
                    if cur.rowcount == 0:
                        cur.execute("INSERT INTO stages( "
                                    "id, name, tournament_id ) "
                                    "VALUES( ?, ?, ? )",
                                    (stage_id, stage_name, tourn_id))

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
            cur.execute(("UPDATE teams "
                         "   SET name=?, region=? "
                         " WHERE id=?"), (team_name, region, team_id))

            # inserting them if update fails
            if cur.rowcount == 0:
                cur.execute(("INSERT INTO teams( "
                             "id, name, region ) "
                             "VALUES( ?, ?, ? )"), (team_id, team_name, region))

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
            cur.execute(("UPDATE players "
                         "   SET team=?, region=?, nickname=?, realname=?, "
                         "       country=?, role=? "
                         " WHERE id = ?"),
                        (player_team, player_region, player_nickname,
                         player_name, player_country, player_role, player_id))

            # inserting them if the update failed
            if cur.rowcount == 0:
                cur.execute(("INSERT INTO players( "
                             "id, team, region, nickname, realname, country,"
                             "role) "
                             "VALUES( ?, ?, ?, ?, ?, ?, ? )"),
                            (player_id, player_team, player_region,
                             player_nickname, player_name, player_country,
                             player_role))

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
        cur.execute(("UPDATE patches "
                     "SET name=?, from_date=?, to_date=? "
                     "WHERE id=?"),
                    (patch_name, patch_from_dt, patch_to_dt, patch_id))

        # inserting them if update fails
        if cur.rowcount == 0:
            cur.execute(("INSERT INTO patches( "
                         "id, name, from_date, to_date ) "
                         "VALUES( ?, ?, ?, ? )"),
                        (patch_id, patch_name, patch_from_dt, patch_to_dt))

    # committing changes to the database
    con.commit()
    # no next page this time, so just return when the for loop is done


def update_db_maps(con, cur):
    """ Updates the database with map info. """
    print('Getting Map Information')

    # Opening requests session and getting json data of patches
    sesh = requests.Session()
    req = sesh.get("https://api.masterleague.net/maps.json")

    # Looping through the results and inserting them
    print('Updating Database...')
    for i in range(len(req.json())):
        # pulling out the values
        map_id = req.json()[i]['id']
        map_name = req.json()[i]['name']

        # trying to update first
        cur.execute(("UPDATE maps "
                     "   SET name=? "
                     " WHERE id=?"),
                    (map_name, map_id))

        # inserting them if update fails
        if cur.rowcount == 0:
            cur.execute(("INSERT INTO maps( id, name ) "
                         "VALUES( ?, ? )"),
                        (map_id, map_name))

    # committing changes to the database
    con.commit()


def update_player_detail(con, cur, match_id, match_date, draft):
    """ updates the player_detailed table """

    for team in draft:
        team_id = team["team"]
        for player in team["picks"]:
            player_id = player["player"]
            hero_id = player["hero"]
            cur.execute(("UPDATE player_details "
                         "   SET date = ?, team_id = ?, hero_id =? "
                         " WHERE match_id = ? AND player_id = ? "),
                        (match_date, team_id, hero_id, match_id, player_id))

            if cur.rowcount == 0:
                cur.execute(("INSERT INTO player_details(match_id, team_id, "
                             "            hero_id, date, player_id) "
                             "VALUES ( ?, ?, ?, ?, ? ) "),
                            (match_id, team_id, hero_id, match_date, player_id))

            stats = player['stats']
            talents = player['talents']

            # Only update all of the stats if they exist
            if len(stats) > 0:
                cur.execute(("UPDATE player_details "
                             "   SET kills = ?, assists = ?, deaths = ?, "
                             "       siege_damage = ?, hero_damage = ?, "
                             "       exp = ?, time_spent_dead = ?, "
                             "       self_healing = ?, healing = ?, "
                             "       damage_taken = ? "
                             " WHERE match_id = ? AND player_id = ?"),
                            (stats['kills'], stats['assists'], stats['deaths'],
                             stats['siege_damage'], stats['hero_damage'],
                             stats['experience'], stats['time_spent_dead'],
                             stats['self_healing'], stats['healing'],
                             stats['damage_taken'], match_id, player_id))

            for i in range(len(talents)):
                talent_id = talents[i]

                # we can use string formatting here because we know the
                # input is just an integer from the for loop
                cur.execute(("UPDATE player_details "
                             "   SET talent_{0} = ? "
                             " WHERE match_id = ? AND player_id = ?").format(i+1),
                            (talent_id, match_id, player_id))

    con.commit()
    return None


def update_db_match_basic(con, cur, match_id):
    """ updates the match table with patch, tournament, stage, and game """
    print('Getting Match Information')

    # Opening requests session and getting json data for a specific match
    sesh = requests.Session()
    req = sesh.get("https://api.masterleague.net/matches/" + str(match_id) +
                   ".json")

    try:
        match_patch = req.json()['patch']
    except KeyError:
        return False

    # looping through the information and updating the information
    # the information should be in the database already from the web scraper
    print('Updating Database...')

    # pulling out the extra values and making sure
    match_patch = req.json()['patch']
    # need to check to see if the value exists, and update if
    # it does not. The update function updates the entire table. It does not
    # just insert the new value. Since id is the primary key, it will not
    # change
    check_patch = cur.execute("SELECT id FROM patches WHERE id=?",
                              (str(match_patch), ))
    if check_patch.fetchone() is None:
        # if none, then does not exist, run code
        update_db_patches(con, cur)

    # now checking tournament info and updating
    match_tourn = req.json()['tournament']
    cur.execute("SELECT id FROM tournaments WHERE id=?",
                (str(match_tourn), ))
    if cur.fetchone() is None:
        update_db_tournament(con, cur)

    # checking game version and updating
    match_version = req.json()['game_version']
    cur.execute("SELECT game_version FROM talents WHERE game_version = ?",
                (match_version, ))

    if cur.fetchone() is None and match_version != 0:
        time.sleep(1)
        update_db_talents(con, cur, match_version)

    # checking maps and updating
    match_map = req.json()['map']
    cur.execute("SELECT name FROM maps WHERE id = ?",
                (match_map, ))

    if cur.fetchone() is None:
        update_db_maps(con, cur)

    # Getting match date
    match_date = req.json()['date'][0:10]  # first 10 chars are date

    # Getting the rest of the basic match information
    match_duration = req.json()['duration']
    match_game = req.json()['game']
    match_stage = req.json()['stage']  # no need to check stages, tournament updates it
    match_game_version = req.json()['game_version']
    match_round = req.json()['round']
    match_format = req.json()['series_format']
    match_series = req.json()['series']

    # Pulling out and processing match data
    match_team1 = req.json()['drafts'][0]
    match_team2 = req.json()['drafts'][1]
    update_player_detail(con, cur, match_id, match_date, req.json()['drafts'])

    match_home_team = match_team1['team']
    match_away_team = match_team2['team']
    match_home_bans = match_team1['bans']
    match_away_bans = match_team2['bans']

    if match_team1['is_winner'] is True:
        match_score = 1
    else:
        match_score = 0

    # updating the match_basic table
    cur.execute(("UPDATE match_basic "
                 "SET patch=?, tournament=?, stage=?, game=?, game_version=? "
                 "WHERE match_id=?"),
                (match_patch, match_tourn, match_stage, match_game, match_game_version,
                 match_id))

    if cur.rowcount == 0:
        cur.execute(("INSERT INTO match_basic( "
                     "match_id, date, home_team, away_team, score, map, "
                     "duration, home_ban1, home_ban2, away_ban1, away_ban2, "
                     "patch, tournament, stage, game, format, game_version, "
                     "match_round, series) "
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                     "        ?, ?, ?, ?)"),
                    (match_id, match_date, match_home_team, match_away_team,
                     match_score, match_map, match_duration, match_home_bans[0],
                     match_home_bans[1], match_away_bans[0], match_away_bans[1],
                     match_patch, match_tourn, match_stage, match_game,
                     match_format, match_game_version, match_round, match_series))

    # committing changes
    con.commit()
    return True


def close_db(con):
    """ Closing the connection to the database """
    con.close()  # closing the connection
    print('Connection closed! (and hopefully a success)')


if __name__ == "__main__":
    # just runs through all 4 of the reference table updates
    CONN, CURR = setup_db_con()
    # update_db_tournament(CONN, CURR)
    # update_db_teams(CONN, CURR)
    # update_db_players(CONN, CURR)
    # update_db_patches(CONN, CURR)
    # update_db_heroes(CONN, CURR)
    update_db_match_basic(CONN, CURR, 804)
    close_db(CONN)
