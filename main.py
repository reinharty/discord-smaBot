import asyncio
import os
from datetime import datetime
import discord
import pycron
from dotenv import load_dotenv

from message import Message
from scraper import Scraper

intents = discord.Intents.default()
intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

load_dotenv()

scedule = os.getenv('SCEDULE')

channel_sp500_alarm_id = int(os.getenv('SP500_ALARM_200'))
channel_sp500_report_id = int(os.getenv('SP500_REPORT'))

channel_nasdaq_alarm_id = int(os.getenv('NASDAQ_ALARM_220'))
channel_nasdaq_report_id = int(os.getenv('NASDAQ_REPORT'))

channel_dax_alarm_id = int(os.getenv('DAX_ALARM_200'))
channel_dax_report_id = int(os.getenv('DAX_REPORT'))

channel_tyx_alarm_id = int(os.getenv('TYX_ALARM_60'))
channel_tyx_report_id = int(os.getenv('TYX_REPORT'))

channel_debug_id = int(os.getenv('DEBUG'))

token = os.getenv('TOKEN')



@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    #schedule_daily_task()  # Schedule the daily message
    debug_channel = client.get_channel(channel_debug_id)
    await debug_channel.send("Online again at " + datetime.today().strftime("%Y-%m-%d-%H:%M:%S") + " " + scedule)
    #await jobs()
    await scheduler()  # Start the scheduler loop

async def scheduler():
    """Run the scheduler loop to execute scheduled tasks."""
    print('Scheduler started')
    while True:
        #schedule.run_pending()
        if pycron.is_now(scedule):
            await jobs()
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(15)

async def jobs():
    # SP500
    # alarm
    channel = client.get_channel(channel_sp500_alarm_id)
    signal = Scraper().get_signal("^GSPC", 200)
    message = Message().alarm_message('sp500', signal)
    await channel.send(message)

    # SP500
    # report
    channel = client.get_channel(channel_sp500_report_id)
    message = Scraper().daily_report("^GSPC", 200)
    await channel.send(message)

    # NASDAQ
    # alarm
    channel = client.get_channel(channel_nasdaq_alarm_id)
    signal = Scraper().get_signal("^NDX", 220)
    message = Message().alarm_message('nasdaq', signal)
    await channel.send(message)

    # NASDAQ
    # report
    channel = client.get_channel(channel_nasdaq_report_id)
    message = Scraper().daily_report("^NDX", 220)
    await channel.send(message)

    # DAX
    # alarm
    channel = client.get_channel(channel_dax_alarm_id)
    signal = Scraper().get_signal("^GDAXI", 200)
    message = Message().alarm_message('dax', signal)
    await channel.send(message)

    # DAX
    # report
    channel = client.get_channel(channel_dax_report_id)
    message = Scraper().daily_report("^GDAXI", 200)
    await channel.send(message)

    # Treasury Yield 30
    # alarm
    channel = client.get_channel(channel_tyx_alarm_id)
    signal = Scraper().get_signal("^TYX", 60)
    message = Message().alarm_message('tyx', signal)
    await channel.send(message)

    # Treasury Yield 30
    # report
    channel = client.get_channel(channel_tyx_report_id)
    message = Scraper().daily_report("^TYX", 60)
    await channel.send(message)

#load_dotenv()
client.run(token)
