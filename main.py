import os
from process_file import return_tracker
import pandas as pd

# top directory should refer to the top of your data_folder
top_directory = r'C:\Users\Mitchell Gaming PC\Documents\10-K Files'
os.chdir(top_directory)

path = top_directory + '\{}\{}'

tracker = {}
index = 0

# Data Folder Structure Loop
for year in ['10_X_C_2020', '10-X_C_2019', '10-X_C_2021']:
    for quarter in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:
        print('On year {}, quarter {}.'.format(year, quarter))
        os.chdir(path.format(year, quarter))
        file_list = os.listdir()
        for file in file_list:
            tracker[index] = return_tracker(file)
            index += 1

df = pd.DataFrame.from_dict(tracker, orient = 'index')

# output directory should refer to the output directory in your project folder
output_directory = r'C:\Users\Mitchell Gaming PC\OneDrive - Visual Risk IQ, LLC\School Files\Fall 2022\Advanced Business Analytics (TA)\10-K Extraction\Outputs'
os.chdir(output_directory)

df.to_csv('secfilings_parsed.csv')