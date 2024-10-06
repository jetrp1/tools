#!/bin/env python3

import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
from argparse import ArgumentParser, FileType
from datetime import datetime

def format_date_long(x, pos=None):
    date = mdates.num2date(x)
    return date.strftime('%m/%d/%Y')

def format_date_medium(x, pos=None):
    date = mdates.num2date(x)
    return date.strftime('%a %H:%M %p')

def format_date_short(x, pos=None):
    date = mdates.num2date(x)
    return date.strftime('%I:%M %p')

def format_date_short_minor(x, pos=None):
    date = mdates.num2date(x)
    return date.strftime('%M')

def date_min_diff(start:datetime, end:datetime):
    return int((end - start).total_seconds() / 60.0)


def main() :
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('logFile', type=FileType('r'))
    parser.add_argument('-t', '--goBackTime', type=int, default=1440, help='time in Minuites of history to show, 0 being all time, default being 1 day')
    args = parser.parse_args()

    df = pd.read_csv(args.logFile, header=0, parse_dates=[0], on_bad_lines='warn')

    if args.goBackTime != 0:
        df = df.tail(args.goBackTime)

    timeDiff = date_min_diff(df.at[df.index[0], 'Date Time'].to_pydatetime(), df.at[df.index[-1], 'Date Time'].to_pydatetime())

    currDate = df.at[df.index[0], 'Date Time'].to_pydatetime().strftime('%b %d, %Y')
    fig, axs = plt.subplots(2,1)
    fig.suptitle(f'Records starting on {currDate}')
    fig.set_size_inches(28,8)
    fig.set_dpi(80)

    axs[0].plot(df['Date Time'], df['Avg RTT'])
    axs[1].set_title('Average RTT')
    axs[0].set_xlabel('Date/Time')
    axs[0].set_ylabel('Round Trip Time')
    axs[0].set_ylim(0, 100)


    # Formatting the Axis

    if timeDiff <= 1440:                                  # If date Range is short (<= 1 day)
        numHours = int(timeDiff/60)
        axs[0].xaxis.set_minor_locator(ticker.LinearLocator(numticks=numHours*2))
        axs[0].xaxis.set_major_locator(ticker.LinearLocator(numticks=numHours))
        axs[0].xaxis.set_minor_formatter(ticker.FuncFormatter(format_date_short_minor))
        axs[0].xaxis.set_major_formatter(ticker.FuncFormatter(format_date_short))

        axs[1].xaxis.set_minor_locator(ticker.LinearLocator(numticks=numHours*4))
        axs[1].xaxis.set_major_locator(ticker.LinearLocator(numticks=numHours))
        axs[1].xaxis.set_minor_formatter(ticker.FuncFormatter(format_date_short_minor))
        axs[1].xaxis.set_major_formatter(ticker.FuncFormatter(format_date_short))
    elif timeDiff <= 10080:                              # If date Range is medium (<= 7 days)
        numHalfDays = int(timeDiff/720)
        axs[0].xaxis.set_major_locator(ticker.LinearLocator(numticks=numHalfDays))
        axs[0].xaxis.set_major_formatter(ticker.FuncFormatter(format_date_medium))

        axs[1].xaxis.set_major_locator(ticker.LinearLocator(numticks=numHalfDays))
        axs[1].xaxis.set_major_formatter(ticker.FuncFormatter(format_date_medium))
    else:
        numDays = int(timeDiff/1440)                                               # If date range is Long (7 days or more)
        axs[0].xaxis.set_major_locator(ticker.LinearLocator(numticks=numDays))
        axs[0].xaxis.set_major_formatter(ticker.FuncFormatter(format_date_long))

        axs[1].xaxis.set_major_locator(ticker.LinearLocator(numticks=numDays))
        axs[1].xaxis.set_major_formatter(ticker.FuncFormatter(format_date_long))


    axs[1].plot(df['Date Time'], df['Packet Loss (%)'])
    axs[1].set_title('Packet Loss')
    axs[1].set_xlabel('Date/Time')
    axs[1].set_ylabel('Packet Loss (%)')
    axs[1].set_ylim(0, 100)
    
    
    axs[1].yaxis.set_major_formatter(ticker.PercentFormatter(100))

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
    exit()