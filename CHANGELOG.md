# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased
- Make sure none of the XPaths are fixed

## 0.1.0 - 2017-02-26
### Added
- New Patches, players, region, roles, stages, teams, and tournament tables
  to in the SQLite database to better keep track of extra information from
  Masterleague API.
- Added appropriate code `pipelines.py` and a new file `update_sqlite.py`
  to collect information from the API.

### Changed
- Cleaned up SQLite code significantly in `pipelines.py`.
- Select desired match_id to start from in command line. This is much
  better than previously. *thanks to ialwaysbecoding*
