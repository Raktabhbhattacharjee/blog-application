@echo off
REM Development watcher: rebuilds the stylesheet whenever a template or
REM input.css changes. Leave this running in its own terminal alongside
REM `python manage.py runserver`. Stop it with Ctrl+C.
tools\tailwindcss.exe -i blog_main\static_src\input.css -o blog_main\static\css\site.css --watch
