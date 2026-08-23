@echo off
REM One-off production build: compiles + minifies the Tailwind stylesheet.
REM Run from the project root:  tailwind-build.bat
tools\tailwindcss.exe -i blog_main\static_src\input.css -o blog_main\static\css\site.css --minify
