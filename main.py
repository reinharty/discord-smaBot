import asyncio
import os
from datetime import datetime
import discord
import pycron
from dotenv import load_dotenv
import yfinance as yf

from message import Message
from src.logic.scraper import Scraper

intents = discord.Intents.default()
intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

load_dotenv()

scedule = os.getenv('SCEDULE')

channel_sp500_alarm_id = int(os.getenv('SP500_ALARM_200'))
channel_sp500_report_id = int(os.getenv('SP500_REPORT'))

channel_sp500_190_alarm_id = int(os.getenv('SP500_ALARM_190'))
channel_sp500_190_report_id = int(os.getenv('SP500_REPORT_OFFSET'))

channel_nasdaq_alarm_id = int(os.getenv('NASDAQ_ALARM_220'))
channel_nasdaq_report_id = int(os.getenv('NASDAQ_REPORT'))

channel_dax_alarm_id = int(os.getenv('DAX_ALARM_200'))
channel_dax_report_id = int(os.getenv('DAX_REPORT'))

channel_tlt_alarm_id = int(os.getenv('TYX_ALARM_60'))
channel_tlt_report_id = int(os.getenv('TYX_REPORT'))

channel_debug_id = int(os.getenv('DEBUG'))

token = os.getenv('TOKEN')

channels_of_tickers = {
    "^GSPC" : [channel_sp500_alarm_id, channel_sp500_report_id],
    "^SP500TR" : [channel_sp500_190_alarm_id, channel_sp500_190_report_id],
    "^NDX" : [channel_nasdaq_alarm_id, channel_nasdaq_report_id],
    "^GDAXI" : [channel_dax_alarm_id, channel_dax_report_id],
    "TLT" : [channel_tlt_alarm_id, channel_tlt_report_id]
}


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    #schedule_daily_task()  # Schedule the daily message
    debug_channel = client.get_channel(channel_debug_id)
    await debug_channel.send("Online again at " + datetime.today().strftime("%Y-%m-%d-%H:%M:%S") + " " + scedule)
    await debug_channel.send("yfinance version = " + yf.__version__)
    await debug_channel.send("version = 11.3.2025")

    await generateAndSendSignal("^GSPC", 200)
    await generateAndSendSignal("^SP500TR", 190, 0.025)
    await generateAndSendSignal("^NDX", 220)
    await generateAndSendSignal("^GDAXI", 200)
    await generateAndSendSignal("TLT", 60)

    await generateAndSendReport("^GSPC", 200)
    await generateAndSendReport("^SP500TR", 190, 0.025)
    await generateAndSendReport("^NDX", 220)
    await generateAndSendReport("^GDAXI", 200)
    await generateAndSendReport("TLT", 60)

    #
    # # SP500TR
    # # alarm
    #
    # #TODO funktioniert noch nicht, weil sich zwar der benutzte SMA übergeben lässt, aber die flags noch nicht zurÜckgesetzt werden
    # #denke zwei separate results objecte für den jeweiligen SMA könnten sinnvoller sein
    # channel = client.get_channel(channel_debug_id)
    # result = Scraper().get_signals("^SP500TR", 190, 0.025)
    # message = Message().alarm_message('^SP500TR', result.signal_now)
    # sma_high = result.current_sma * (1+0.025)
    # sma_low = result.current_sma * (1-0.025)
    # result.current_sma = sma_high
    # sma_high_text = Message.get_alarms(result)
    # if sma_high_text != "":
    #     message += "For high SMA:\n"
    #     message += sma_high_text
    #
    # result.current_sma = sma_low
    # sma_low_text = Message.get_alarms(result)
    # if sma_low_text != "":
    #     message += "For low SMA:\n"
    #     message += sma_low_text
    #
    # await channel.send(message + " ^SP500TR, SMA = 190, offset = 2.5%")
    # # report
    # channel = client.get_channel(channel_debug_id)
    # message = Scraper().get_report("^SP500TR", 190, 0.025)
    # await channel.send(message + " ^SP500TR, SMA = 190, offset = 2.5%")



    # await jobs()
    # await reports()
    await scheduler()  # Start the scheduler loop


async def scheduler():
    """Run the scheduler loop to execute scheduled tasks."""
    print('Scheduler started')
    while True:
        #schedule.run_pending()
        if pycron.is_now(scedule):
            await signals()
            await reports()
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(15)


async def signals():

    await generateAndSendSignal("^GSPC", 200)
    await generateAndSendSignal("^SP500TR", 190, 0.025)
    await generateAndSendSignal("^NDX", 220)
    await generateAndSendSignal("^GDAXI", 200)
    await generateAndSendSignal("TLT", 60)


async def reports():

    await generateAndSendReport("^GSPC", 200)
    await generateAndSendReport("^SP500TR", 190, 0.025)
    await generateAndSendReport("^NDX", 220)
    await generateAndSendReport("^GDAXI", 200)
    await generateAndSendReport("TLT", 60)

async def generateAndSendSignal(ticker, sma_days, offset=0.0):

    channel = client.get_channel(channels_of_tickers[ticker][0])
    result = Scraper().get_signals(ticker, sma_days)
    message = Message().alarm_message(ticker, result.signal_now)
    message += Message.get_alarms(result)
    await channel.send(message)

async def generateAndSendReport(ticker, sma_days, offset=0.0):
    channel = client.get_channel(channels_of_tickers[ticker][1])
    message = Scraper.get_report(ticker, sma_days, offset)
    await channel.send(message)

#load_dotenv()
client.run(token)
