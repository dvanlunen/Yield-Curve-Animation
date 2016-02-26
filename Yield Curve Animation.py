import urllib.request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd

# Scrap the Data
yieldcurve_website = 'http://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldAll'

soup = BeautifulSoup(urllib.request.urlopen(yieldcurve_website).read(),
                     'lxml-xml')
rows = []
headers = ['Date', '1 Month Treasury Yield', '3 Month Treasury Yield',
           '6 Month Treasury Yield', '1 Year Treasury Yield',
           '2 Year Treasury Yield', '3 Year Treasury Yield',
           '5 Year Treasury Yield', '7 Year Treasury Yield',
           '10 Year Treasury Yield', '20 Year Treasury Yield',
           '30 Year Treasury Yield']

inttable = soup.find('table', attrs={'class': 't-chart'})

for row in inttable.findAll('tr')[1:]:
    rows.append([val.text for val in row.find_all('td')])

yield_curve = np.array(rows)
yield_curve[yield_curve == '\n\t\t\tN/A\n\t\t'] = np.nan
dates = yield_curve[:, 0]
yield_curve = yield_curve[:, 1:]

# create animation


class UpdateDist(object):
    """docstring for UpdateDist"""
    def __init__(self, ax):
        self.line, = ax.plot([], [], 'r-')
        self.xdat = np.array([1, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360])
        self.ax = ax
        self.ax.set_xlim(0, 361)
        self.ax.set_ylim(0, 10)
        self.period = 0
        self.ax.set_title(dates[self.period])
        self.ax.set_xlabel('Months to Maturity')
        self.ax.set_ylabel('Yield Rate (%)')

    def init(self):
        self.line.set_data([], [])
        return self.line,

    def __call__(self, i):
        if i == 0:
            return self.init()
        if self.period != len(dates)-1:
            self.period += 1
        else:
            self.period = 0
        # set up data masking out missing values
        ydat = yield_curve[self.period, :].astype(np.double)
        ymask = np.isfinite(ydat)
        y = ydat[ymask]
        x = self.xdat[ymask]
        self.line.set_data(x, y)
        self.ax.set_title(dates[self.period])
        ax.figure.canvas.draw()
        return self.line,


fig, ax = plt.subplots()
ud = UpdateDist(ax)
anim = FuncAnimation(fig, ud, frames=np.arange(100),
                     init_func=ud.init, interval=.1, blit=True)
plt.show()
