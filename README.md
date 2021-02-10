To use, you must: Have an alpaca account. Set your api keys via export or in system variables. Manually add your tickers and ideal porfolio quantity. Run daily with crontab and compare excel report to your results unless for safety. *Values for percentages in XLSX are *100 for readability without Excel formatting.

0 12 * * * source /Users/skiwheelr/.bash_profile; cd /Users/skiwheelr/PaperMaker/ && /opt/miniconda3/bin/python daytrade.py >> /Users/skiwheelr/PaperMaker/cron.log 2>&1
