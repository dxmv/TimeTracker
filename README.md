# Time Tracker
If you want to finally take control of your life, this is the app for you.

To control your life, you need to control your time. You need to be disciplined and productive. Everybody knows that, but that begs the question, "how do I control my time?"

Well, first, you need to know how you spend your time during the day and identify the biggest time wasters. Once you know what the biggest time wasters are, you can simply eliminate them. But how do you keep track of your time and the time wasters?

The simplest solution is a notebook. However, the problem with using a notebook is that you will waste a lot of pages, and you may forget to write things down. Moreover, the biggest issue with the notebook approach is that you need to do all the work, which can lead to mistakes. This is where the Time Tracker comes in. It replaces the notebook and does all the work for you. It even runs on a timer. Every 30 minutes, a window pops up where you can type in what you did, and that's it. The Time Tracker will handle the calculations and provide visualizations with graphs. Most importantly, it will help you in your mission to conquer your time. As we established in the beginning, those who control their time also control their own lives.
## Features
This app consits of two parts:
- Desktop app - used for inputing the activity
- Website - used for presentation

The desktop app runs in 30 minute intervals (at 12:30, 13:00, 13:30...), by clicking the submit button the text you typed in is saved in the database.
The website has 3 different pages home, week and date. Home represents the month, it shows the things you did the most this month, and also a pie chart. The same goes for the week page, but you can also see the calendar, you can click on any of those days and get to the date page. On date page you can see what you did every hour of the today. You can also edit the activites for the day on that page.
## Instalation
Install all librararies in requirements.txt

To use the destkop app (it runs every 30 mins):
```sh
py schedule_app.py
```

To use the website:
```sh
flask run
```

Enviroment variables:
```sh
DB_HOST = host name
DB_DATABASE = name of database
DB_USERNAME = username
DB_PASSWORD = password
```
## Tech
Frontend technologies:
- [Bootstrap](https://getbootstrap.com/) - Frontend toolkit
- [Chart.js](https://www.chartjs.org/)  - JavaScript charting library for the modern web

Backend technologies:
- [Flask](https://flask.palletsprojects.com/en/2.3.x/)  - Used for developing web applications using python
- [Customtkinter](https://github.com/TomSchimansky/CustomTkinter)  - Modern GUI 
- [Psycopg2](https://www.psycopg.org/docs/)  - PostgreSQL database adapter for the Python 

