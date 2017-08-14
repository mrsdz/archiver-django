# &#x1F534; This project is under development so take it easy :) &#x1F534;

## About
Online Archiver is a web app for Shamsipour Technical and Vocational College.

## How to run
To run archiver; Just use steps below:

1. Install `python2`, `pip`, `virtualenv` and `pillow` in your system.
2. Clone the project `https://github.com/mrsdz/archiver-django`.
3. Make development environment ready using commands below;

  ```bash
  git clone https://github.com/mrsdz/archiver-django && cd archiver-django
  virtualenv -p python2 build  # Create virtualenv named build
  source build/bin/activate
  pip install django pillow
  mv  onlineArchiver/settings.py.sample onlineArchiver/settings.py
  python manage.py migrate  # Create database tables
  ```

4. Run `Online Archiver` using `python manage.py runserver`
5. Go to [http://localhost:8000](http://localhost:8000) to see it.
