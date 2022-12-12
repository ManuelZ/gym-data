# Standard-Library imports
import datetime

# External imports
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.layout_engine import ConstrainedLayoutEngine
from matplotlib.dates import ConciseDateFormatter 
import matplotlib.dates as mdates


pdf = matplotlib.backends.backend_pdf.PdfPages("out_pdf.pdf")

A4_SIZE = (8.27, 11.69)


##############################################################################
# Data processing
##############################################################################

df = pd.read_csv(
    r"C:\Users\Manuel\Desktop\Documentos\1.PROJECTS\Gym data\FitNotes_Export_2022_12_11_14_34_57.csv",
    parse_dates=["Date"]
)

# Remove unused columns
df = df.drop(["Distance", "Distance Unit", "Time"], axis=1)

# Filter by date
df = df[(df['Date'] > '2022-09-01')]

# Extract week number
# df["Week"] = df["Date"].dt.strftime('%W')
df["volume"] = df["Weight (lbs)"] * df["Reps"]

result = df.groupby(["Date", "Category"])["volume"].sum()
# result = df.resample('W-Mon', on='Date').sum().groupby(by=["Date", "Category"])["volume"]
# result = df.groupby([pd.Grouper(key='Date', freq='W')])['volume'].sum()

result = pd.DataFrame({
    "Date":     result.index.get_level_values(0),
    "Category": result.index.get_level_values(1),
    "Volume":   result.values
})


##############################################################################
# Plotting
##############################################################################

# rect: Rectangle in figure coordinates to perform constrained layout in 
# (left, bottom, width, height), each from 0-1.
# Allows me to have some space between the figure suptitle and the figures
layout_engine=ConstrainedLayoutEngine(rect=(0, 0, 1, 0.95))
figure = plt.figure(figsize=A4_SIZE, layout=layout_engine)
# Using Text works better than using title
# figure.suptitle("Gym report1", fontsize='xx-large')
figure.text(
    0.5, 0.98,
    "Gym volume per workout - 2022",
    fontsize='xx-large',
    horizontalalignment="center",
    fontweight="bold"
    )
figure.supxlabel(datetime.datetime.now().strftime('%d/%m/%Y %H:%M'))

subfigures = figure.subfigures(3, 1, hspace=0.1)

# Row 1
axes0 = subfigures[0].subplots(1, 3, sharey=True)
# subfigures[0].suptitle('Volume per week', fontsize='x-large')
#subfigures[0].supxlabel("Week",y=-0.13)
subfigures[0].supylabel("Volume [lbs]")
subfigures[0].autofmt_xdate() #automatically makes the x-labels rotate
categories = ["Back", "Chest", "Shoulders"]
for i in range(len(categories)):
    ax = axes0[i]
    ax.plot(
        result[result.Category==categories[i]]["Date"], 
        result[result.Category==categories[i]]["Volume"],
        "k-",
        marker='.'
    )
    # result[result.Category==categories[i]].plot(
    #     kind="line",
    #     style="k-",
    #     y="Volume",
    #     x="Date",
    #     legend=False,
    #     ax=ax,
    # )
    ax.set(title=categories[i])
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

# Row 2
axes1 = subfigures[1].subplots(1, 1, sharey=True)
# subfigures[1].suptitle('Volume per week', fontsize='x-large')
subfigures[1].supylabel("Volume [lbs]")
subfigures[0].autofmt_xdate() #automatically makes the x-labels rotate

category = "Legs"
ax = axes1
result[result.Category==category].plot(
    kind="line",
    style="k-",
    marker=".",
    y="Volume",
    x="Date",
    legend=False,
    ax=ax,
)
ax.set(title=category)
ax.set(xlabel=None)
ax.grid(True)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=1))
ax.xaxis.set_major_formatter(
    ConciseDateFormatter(
        locator=ax.xaxis.get_major_locator(), 
        show_offset=False
    )
)

# The position of the left edge of the subplots, as a fraction of the figure width.
# plt.subplots_adjust(left=0.1, right=0.95, top=0.90, bottom=0.0)
pdf.savefig(figure, bbox_inches="tight", pad_inches=0.4)
pdf.close()
plt.show()
