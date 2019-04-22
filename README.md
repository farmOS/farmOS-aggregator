# farmOS Aggregator

[![Licence](https://img.shields.io/badge/Licence-GPL%203.0-blue.svg)](https://opensource.org/licenses/GPL-3.0/)
[![Release](https://img.shields.io/github/release/farmOS/farmOS-aggregator.svg?style=flat)](https://github.com/farmOS/farmOS-aggregator/releases)
[![Last commit](https://img.shields.io/github/last-commit/farmOS/farmOS-aggregator.svg?style=flat)](https://github.com/farmOS/farmOS-aggregator/commits)
[![Twitter](https://img.shields.io/twitter/follow/farmOSorg.svg?label=%40farmOSorg&style=flat)](https://twitter.com/farmOSorg)
[![Chat](https://img.shields.io/matrix/farmOS:matrix.org.svg)](https://riot.im/app/#/room/#farmOS:matrix.org)

farmOS Aggregator is an application for aggregating data from multiple
[farmOS](https://farmOS.org) instances.

For more information on farmOS, visit [farmOS.org](https://farmOS.org).

## GETTING STARTED

To launch the application in Docker, run the following command:

    sudo docker-compose up

Then open `https://localhost` in your browser to view the application.

## INSTANCE FILES

When you start up an instance of the farmOS Aggregator, any files that are
needed for state persistence will be stored in the `./instance` directory.

The `./instance` directory may contain sensitive information, so it is
important that it is stored and managed securely on production servers.

### Database

An SQLite3 database is automatically created to store information about the
farmOS instances that are being tracked. By default, this will be saved to
`./instance/database.sqlite3`.

### Configuration

Configuration for the instance can be overridden by creating a `settings.py`
file inside the `./instance` directory. For a list of available settings and
their default values, see `farmOSaggregator/default_settings.py`.

Some settings that you will want to override are:

 * `BASIC_AUTH_USERNAME`: The Basic Authorization username.
 * `BASIC_AUTH_PASSWORD`: The Basic Authorization username.
 * `SECRET_KEY`: The Flask secret key.

## RUNNING TESTS

Tests can be run with:

    python setup.py test

This will run all included tests in the `tests/` directory. Pytest is the default test runner.


## MAINTAINERS

 * Michael Stenta (m.stenta) - https://github.com/mstenta

This project has been sponsored by:

 * [Farmier](https://farmier.com)
 * [Pennsylvania Association for Sustainable Agriculture](https://pasafarming.org)
 * [Our Sci](http://our-sci.net)
 * [Bionutrient Food Association](https://bionutrient.org)
 * [Foundation for Food and Agriculture Research](https://foundationfar.org/)
