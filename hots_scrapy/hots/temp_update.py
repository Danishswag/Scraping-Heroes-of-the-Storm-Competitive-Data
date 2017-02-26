import sqlite3 as lite
import requests
import time


def main():
    print('Opening connection...')
    con = lite.connect("../HotSCompetitive.sqlite")
    cur = con.cursor()

    sesh = requests.Session()
    req = sesh.get("https://api.masterleague.net/matches.json?page_size=25")

    # looping through the information and updating the information
    # the information should be in the database already from the web scraper
    print('Updating Database...')
    while True:
        for i in range(len(req.json()['results'])):
            # pulling out the extra values
            match_id = req.json()['results'][i]['id']
            match_patch = req.json()['results'][i]['patch']
            match_tourn = req.json()['results'][i]['tournament']
            match_stage = req.json()['results'][i]['stage']
            match_game = req.json()['results'][i]['game']

            # trying to update first
            cur.execute("UPDATE match_basic \
            SET patch=?, tournament=?, stage=?, game=? \
            WHERE match_id=?", \
            (match_patch, match_tourn, match_stage, match_game, match_id))

            # no insert because we want to make sure the scraper happens
            # first
            con.commit()

        if req.json()['next'] is None:
            break
        else:
            time.sleep(0.5)
            req = sesh.get(req.json()['next'])

    con.close()  # closing the connection
    print('Connection closed! (and hopefully a success)')

if __name__ == "__main__":
    main()
