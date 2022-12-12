# Standard-Library imports
import datetime
import sys

# External imports
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.layout_engine import ConstrainedLayoutEngine
from matplotlib.dates import ConciseDateFormatter 
import matplotlib.dates as mdates
from typing import Iterable


pdf = matplotlib.backends.backend_pdf.PdfPages("out_pdf.pdf")

A4_SIZE = (8.27, 11.69)


##############################################################################
# Data processing
##############################################################################

def get_category_volume_by_period(df, category, period) -> pd.Series:
    
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#anchored-offsets
    if period == "week":
        rule = 'W-Mon'
    elif period == "month":
        rule = 'M'
    
    for group_name, group in df.groupby("Category"):
        if group_name == category:
            series = group.resample(rule, on='Date', label='right')["Volume"].sum()
            return series


df = pd.read_csv(
    r"C:\Users\Manuel\Desktop\Documentos\1.PROJECTS\Gym data\FitNotes_Export_2022_12_11_14_34_57.csv",
    parse_dates=["Date"]
)

# Remove unused columns
df = df.drop(["Distance", "Distance Unit", "Time"], axis=1)

# Filter by date
df = df[(df['Date'] > '2022-09-01')]

# Calculate volume
df["Volume"] = df["Weight (lbs)"] * df["Reps"]


##############################################################################
# Plotting functions
##############################################################################

def plot_ax(ax, x, y, title):
    ax.plot(x, y, "k-", marker='.' )
    ax.set(title=title)
    ax.set(xlabel=None)
    ax.grid(True)
    
    # https://matplotlib.org/stable/gallery/ticks/date_concise_formatter.html
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=1))
    ax.xaxis.set_major_formatter(
        ConciseDateFormatter(
            locator=ax.xaxis.get_major_locator(), 
            show_offset=False
        )
    ) 


def plot_categories(df, axes, categories, period):
    for i, category in enumerate(categories):
        series = get_category_volume_by_period(df, category=category, period=period)
        plot_ax(axes[i], series.index, series.values, category)


def prepare_shared_y_subfigure(subfigure, ylabel, categories):
    columns = len(categories)
    axes = subfigure.subplots(1, columns, sharey=True)
    subfigure.supylabel(ylabel)
    subfigure.autofmt_xdate() # automatically makes the x-labels rotate
    if not isinstance(axes, Iterable):
        axes = [axes]
    return subfigure, axes


##############################################################################
# Prepare page 1
##############################################################################

def prepare_page(title, rows=3, columns=1):
    # rect: Rectangle in figure coordinates to perform constrained layout in 
    # (left, bottom, width, height), each from 0-1.
    # Allows me to have some space between the figure suptitle and the figures
    # Needs to be activated before any axes are added to a figure
    layout_engine = ConstrainedLayoutEngine(rect=(0, 0, 1, 0.95))
    figure = plt.figure(figsize=A4_SIZE, layout=layout_engine)
    
    # Using Text works better than using figure.suptitle
    # figure.suptitle("Gym report1", fontsize='xx-large')
    figure.text(
        0.5, 0.98,
        title,
        fontsize='xx-large',
        horizontalalignment="center",
        fontweight="bold"
    )
    figure.supxlabel(datetime.datetime.now().strftime('%d/%m/%Y %H:%M'))

    subfigures = figure.subfigures(rows, columns, hspace=0.1)

    return figure, subfigures


##############################################################################
# Page 1
##############################################################################

figure, subfigures = prepare_page("Volume per week - 2022")

##############################################################################
# Row 1
##############################################################################

subfigure = subfigures[0]
# subfigure.suptitle('Volume per week', fontsize='x-large')
# subfigure.supxlabel("Week",y=-0.13)
categories = ["Back", "Chest", "Shoulders"]
subfigure, axes = prepare_shared_y_subfigure(subfigure, "Volume [lbs]", categories)
plot_categories(df, axes, categories, period="week")


##############################################################################
# Row 2
##############################################################################

subfigure = subfigures[1]
categories = ["Legs"]
subfigure, axes = prepare_shared_y_subfigure(subfigure, "Volume [lbs]", categories)
plot_categories(df, axes, categories, period="week")


##############################################################################
# Row 3
##############################################################################

subfigure = subfigures[2]
categories = ["Biceps", "Triceps"]
subfigure, axes = prepare_shared_y_subfigure(subfigure, "Volume [lbs]", categories)
plot_categories(df, axes, categories, period="week")


# The position of the left edge of the subplots, as a fraction of the figure width.
# plt.subplots_adjust(left=0.1, right=0.95, top=0.90, bottom=0.0)
pdf.savefig(figure, bbox_inches="tight", pad_inches=0.4)
plt.show()





##############################################################################
# Page 2
##############################################################################

figure2, subfigures2 = prepare_page("Volume per month - 2022", rows=3, columns=1)

##############################################################################
# Row 1
##############################################################################

subfigure = subfigures2[0]
categories = ["Back", "Chest", "Shoulders"]
subfigure, axes = prepare_shared_y_subfigure(subfigure, "Volume [lbs]", categories)
plot_categories(df, axes, categories, period="month")


subfigure = subfigures2[1]
categories = ["Legs"]
subfigure, axes = prepare_shared_y_subfigure(subfigure, "Volume [lbs]", categories)
plot_categories(df, axes, categories, period="month")


subfigure = subfigures2[2]
categories = ["Biceps", "Triceps"]
subfigure, axes = prepare_shared_y_subfigure(subfigure, "Volume [lbs]", categories)
plot_categories(df, axes, categories, period="month")

   
# The position of the left edge of the subplots, as a fraction of the figure width.
# plt.subplots_adjust(left=0.1, right=0.95, top=0.90, bottom=0.0)
pdf.savefig(figure2, bbox_inches="tight", pad_inches=0.4)
plt.show()
pdf.close()