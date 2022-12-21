#%%
import os 
import pandas as pd

output_directory = r'C:\Users\Mitchell Gaming PC\OneDrive - Visual Risk IQ, LLC\School Files\Fall 2022\Advanced Business Analytics (TA)\10-K Extraction\Outputs'
os.chdir(output_directory)

df = pd.read_csv('secfilings_parsed.csv')

#%% What percent of files were 10-Ks?
tenK = df[df['type'] == '10-K']
total_tenK = len(tenK)
tenKpercent = len(tenK) / len(df)
#%% What percent of 10-Ks had 1A data extracted?
tenK_extracted = tenK[~tenK['section_list'].isna()]
percent_extracted = len(tenK_extracted) / len(tenK)
total_extracted = len(tenK_extracted)
#%% How many sections were dropped due to short length?
total_skipped = tenK.skipped_sections.sum()
#%% Average number of sections dropped per 10-K?
mean_skipped = tenK.skipped_sections.mean()
#%% Analysis string
analysis = f"""
Of the files provided, {total_tenK}, or {tenKpercent:.2%} were 10-Ks.
Of the 10-Ks, {total_extracted}, or {percent_extracted:.2%} had 1A text extracted.
During the 1A extraction, {total_skipped} sections were skipped, for an average of {mean_skipped:.2} per each 10K.

Also, this is a reminder that not every 10-K should have 1A text extracted, so a higher number for extraction is not necessarily 'more' correct in this case.
"""
print(analysis)