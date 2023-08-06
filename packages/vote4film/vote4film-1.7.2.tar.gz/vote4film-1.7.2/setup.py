# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['calender',
 'calender.migrations',
 'films',
 'films.clients',
 'films.core',
 'films.migrations',
 'films.templatetags',
 'schedule',
 'schedule.migrations',
 'vote4film',
 'votes',
 'votes.migrations',
 'web']

package_data = \
{'': ['*'],
 'calender': ['templates/calender/*'],
 'films': ['templates/films/*'],
 'schedule': ['templates/schedule/*'],
 'votes': ['templates/votes/*', 'templates/votes/includes/*'],
 'web': ['static/web/*',
         'static/web/favicon/*',
         'static/web/images/*',
         'static/web/vendor/fontawesome/*',
         'static/web/vendor/fontawesome/css/*',
         'static/web/vendor/fontawesome/webfonts/*',
         'static/web/vendor/instantclick/*',
         'static/web/vendor/sanitize/*',
         'templates/web/*']}

modules = \
['manage']
install_requires = \
['bbfcapi>=3.0.1,<4.0.0',
 'django-environ>=0.4.5,<0.5.0',
 'django-extensions>=3.0.9,<4.0.0',
 'django>=2.2.17,<3.0.0',
 'lxml>=4.6.2,<5.0.0',
 'pyhumps>=1.6.1,<2.0.0',
 'requests>=2.24,<3.0',
 'xdg>=5.0,<6.0']

extras_require = \
{'postgres': ['psycopg2>=2.8,<3.0'], 'sentry': ['sentry-sdk>=0.19.2,<0.20.0']}

entry_points = \
{'console_scripts': ['manage = manage:main']}

setup_kwargs = {
    'name': 'vote4film',
    'version': '1.7.2',
    'description': 'Easy scheduling for regular film nights',
    'long_description': '# Vote4Film\n\nSimplify film selection for regular film nights. Participants can:\n\n- Add films\n- Vote for films\n- Declare absences\n- See the schedule which takes into account votes and absences\n\nAdmins can set the schedule of film nights.\n\nThis is a simple WSGI Web Application. The back-end is Django, and the front-end\nis dynamic HTML served by Django (no JavaScript is used).\n\n## Development\n\n1. `poetry install` to set-up the virtualenv (one-off)\n2. `poetry run ./src/manage.py migrate` to set-up the local DB (one-off)\n3. `poetry run ./src/manage.py runserver_plus`\n4. `make fix`, `make check` and `make test` before committing\n\n### Contributing\n\nPull requests are welcome :)\n\nTODO: Fix dependency on `bbfcapi` to be `bbfcapi[apis]` and remove direct\ndependency on `pyhumps`.\n\n### Publishing\n\nThis application is published on PyPi.\n\n1. Ensure you have configured the PyPi repository with Poetry (one-off)\n2. Add the release notes in this README.md\n3. `poetry version minor` to bump the major/minor/patch version\n4. Also bump version in `vote4film/__init__.py`\n4. `poetry publish --build` to release\n\nTo publish to the test repository:\n\n1. Ensure you have configured the Test PyPi repository with Poetry (one-off)\n2. `poetry publish --build -r testpypi` to upload to the test repository\n\n## Deployment\n\nUnfortunately, I will not provide detailed guidance for production deployment.\n\nSome general tips:\n\n* Create a virtualenv, e.g. in `~/virtualenv`\n* Install with `pip install vote4film[postgres]`\n* Write the configuration at `~/.config/vote4film/local.env`\n* Use Postgres as the database\n* Use Nginx/uWSGI to to serve the site (with HTTPS)\n* Run Django management commands using `./virtualenv/bin/manage`\n\n## Changelog\n\n### Unpublished\n\n...\n\n### v1.7.2 - 2021-03-04\n\n- Fix getting age rating from BBFC\n- Upgrade dependencies\n\n### v1.7.1 - 2021-02-20\n\n- Add colour to system status bar at the top on iOS Safari\n- Fix vote symbols across different web browsers\n- Reduce page loading times\n\n### v1.7.0 - 2021-01-26\n\n- Add share button to tell people about the next event\n- Add login page\n- Fix webmanifest link on mobile web app\n- Increase size of film posters on larger displays\n- Prettify next event date heading\n\n### v1.6.0 - 2021-01-24\n\n- Treat users with unknown presence as being absent for the event\n- Add link to edit films on film cards\n- Add button to refresh film information\n- Fix colours on film cards\n\n### v1.5.8 - 2021-01-17\n\n- [SECURITY] Fix security vulnerability in underlying dependencies\n- Fix linking to films on BBFC\'s website\n- Fix retrieving age rating from BBFC\n\n### v1.5.7 - 2020-11-08\n\n- [SECURITY] Fix security vulnerability in underlying dependencies\n- Fix vendored YouTube icon being hidden by adblockers\n- Fix missing BBFC age rating symbols\n- Fix failing to log correct error when adding films\n\n### v1.5.6 - 2020-09-20\n\n- Fix parsing omdb film rating when it is missing\n- Add search to the admin page for films\n- Stop content reflow on film cards\n- Stop BBFC icon downloads redirecting\n- Replace external YouTube icon with a local SVG\n- Log more information to Sentry (if enabled)\n\n### v1.5.5 - 2020-06-20\n\n- [SECURITY] Fix security vulnerability in underlying dependencies\n- Add website favicon\n- Fix parsing "PG" age rating\n\n### v1.5.4 - 2020-05-29\n\n- Fix missing icons on upcoming and add film pages (use fontawesome)\n\n### v1.5.3 - 2020-05-02\n\n- Add "update film" link when editing a film\n- Add redirects after editing a film\n- Miscellaneous UI tweaks\n- Add support for "G" age rating on IMDB\n- Fix initial choice on the calender not matching the user\'s previous choice\n- Add option for Sentry\'s trace sample rate\n\n### v1.5.2 - 2020-04-04\n\n- Fix link to calender when there is no upcoming event\n\n### v1.5.1 - 2020-04-04\n\n- Fix call-to-action flow for the upcoming page\n\n### v1.5.0 - 2020-04-04\n\n- Overhaul user interface\n- Enable additional Sentry features including tracing\n\n### v1.4.0 - 2020-03-22\n\n- Allow users to change their vote\n- Redirect the user to the schedule after registering for the event\n- Hide upcoming film until the user has voted for all films\n- Add actually usable admin interface\n- Add optional Sentry integration\n\n### v1.3.0 - 2020-03-22\n\n- Fix error adding film when age rating on IMDB/OMDB is "N/A"\n- Add BBFC age ratings\n\n### v1.2.3 - 2020-02-01\n\n- Redirect to upcoming schedule after voting for every film\n- Fix HTTP 500 error when on schedule page without registering for the event\n\n### v1.2.2 - 2019-12-05\n\n- Fix HTTP 500 error when adding a film that was already added (again)\n- Highlight calender and vote links when there is a user action to take\n- Pick the oldest added film for upcoming when scores are a draw\n\n### v1.2.1 - 2019-11-21\n\n- Remove "film is not available" from the voting page\n- Remove "vote for this film" from the voting page\n- Fix the upcoming page asking absent users to register on calender\n\n### v1.2.0 - 2019-11-21\n\n- Fix ranking films with zero votes as number one\n- Hide upcoming film until the user has registered for the next event\n- Clarify what will happen when adding a film by giving the user more choices\n- Fix HTTP 500 error when adding a film that was already added\n- Hide a film\'s votes from the user until they have voted\n\n### v1.1.0 - 2019/11/16\n\n- Show the register of present/absent users for upcoming films\n- Fix not highlighting films that are not available to be watched\n- Fix parsing of "Not Rated" age ratings resulting in an error\n\n### v1.0.9 - 2019/11/13\n\n- Actually let\'s not be too dumb about packaging\n\n### v1.0.8 - 2019/11/13\n\n- Rename management command from vote4film to manage\n- Stop trying to be smart about packaging\n\n### v1.0.7 - 2019/11/13\n\n- The same fixes as v1.0.6 but for real this time\n\n### v1.0.6 - 2019/11/13\n\n- Fix url patterns for internal apps in installed environment\n- Fix missing template files in PyPi package (so typical!)\n\n### v1.0.5 - 2019/11/12\n\n- Add optional postgres support, e.g. `pip install vote4film[postgres]`\n\n### v1.0.4 - 2019/11/12\n\n- Fix bug loading config from XDG config home (sigh)\n- Fix django-extensions being missed from dependencies\n\n### v1.0.3 - 2019/11/12\n\n- Fix config sub-directory used in XDG config home\n\n### v1.0.2 - 2019/11/12\n\n- Load configuration from XDG config home\n\n### v1.0.1 - 2019/11/10\n\n- First release of Vote4Film\n',
    'author': 'QasimK',
    'author_email': 'noreply@QasimK.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Fustra/vote4film/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
