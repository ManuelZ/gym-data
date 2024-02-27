import datetime

INPUT_FILE = r"FitNotes_Export_2022_12_28_14_02_54.csv"
OUTPUT_FILE = (
    f"training_report_{datetime.datetime.now().strftime('%d_%b_%Y').lower()}.pdf"
)
A4_SIZE = (8.27, 11.69)
