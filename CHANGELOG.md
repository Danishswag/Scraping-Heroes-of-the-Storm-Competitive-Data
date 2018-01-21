# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.2.0] - 2018-01-21
### Added
- New SQLite tables that more closely resemble the structure of
  [Masterleague's](https://masterleague.net) API.
- Updated sqlite database up to use number identifiers with lookup
  tables to save on space.
- `update_hots_db.py`, acting as a frontend to `master_api_call.py`

### Changed
- Moved scrapy files to `hots_scrapy\old`
- All update functions now check to see if lookup tables have the
  lookup values, and gets the data if it is not there
- `README.md` to reflect current state of the project
- RStudio notebook is now broken
- Removed html behind Rstudio notebook

## 0.1.0 - 2017-02-26
### Added
- New Patches, players, region, roles, stages, teams, and tournament tables
  to in the SQLite database to better keep track of extra information from
  Masterleague API.
- Added appropriate code `pipelines.py` and a new file `update_sqlite.py`
  to collect information from the API.

### Changed
- Cleaned up SQLite code significantly in `pipelines.py`.
- Select desired `match_id` to start from in command line. This is much
  better than previously. *thanks to ialwaysbecoding*
