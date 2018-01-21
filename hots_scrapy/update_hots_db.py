from master_api_call import *


def update_hots_data():
    con, cur = setup_db_con()
    # to try to avoid an excessive number of API calls,
    # update most lookup tables beforehand
    update_db_tournament(con, cur)
    update_db_teams(con, cur)
    update_db_players(con, cur)
    update_db_patches(con, cur)
    update_db_heroes(con, cur)
    update_db_maps(con, cur)

    min_match_id = 4020  # overall min is 118
    max_match_id = get_max_match()

    for i in range(min_match_id, max_match_id+1):
        print('Updating database for match', i)
        update_db_match_basic(con, cur, i)

    close_db(con)


if __name__ == "__main__":
    update_hots_data()

