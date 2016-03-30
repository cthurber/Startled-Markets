# Main App

import atexit, time
from flask import Flask
from flask import render_template
from apscheduler.scheduler import Scheduler
from CBOE_API import getTotalData

app = Flask(__name__)

cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()

@cron.interval_schedule(minutes=15)
def refresh_data():
    return getTotalData() # Function asks for latest CBOE data

@app.route('/')
def home(board=refresh_data()):
    return render_template('index.html', board=refresh_data())

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
