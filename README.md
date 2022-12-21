# 10-K Extraction
## Introduction
Scrapes the '1A' section from a directory of SEC filings converted to .txt files. The files are first mined to detect if they are 10Ks based on content and then parsed if they are a 10K filing.
The general logic of the script looks for all of the occurences of keyword terms (item 1a. and item 1b/2) which would indicate the start and end of the section we are looking for. 
Then, the list of these locations are converted into pairs of "closest" coordinates, and the text between each coordinate pair is extracted if it is longer than 40 characters.

## File Structure
Your project folder structure should look like this:
```
project_folder/
├─ Notebooks/
├─ Outputs/
├─ main.py - navigates data_folder and creates output using function from process_file.py
├─ generate_stats.py - generates summary statistics based on output
├─ process_file.py - contains the function to process a single file
```
In addition to this, you should have a data folder (either inside the project folder, or elsewhere) that takes the following form:
```
data_folder/
├─ 10_X_C_2020/
│  ├─ QTR1/
│  │  ├─ 10-K-company.txt
│  ├─ QTR2/
│  ├─ QTR3/
│  ├─ QTR4/
```
Within your data folder, there should be a subfolder for each year. Within a year, there should be a subfolder for each quarter, which contains the SEC filings for that quarter.
If you'd like to change the way the data_folder is set up, add additional years, etc., you are free to do so, but you will need to change the way it is navigated through in main.py.

## Usage
To use this tool, first ensure that you have changed the ```top_directory``` and ```output_directory``` file paths in main.py as well as verified that the data folder structure loop in the code (example below) aligns with your true folder structure.

Code:
```
for year in ['10_X_C_2020']:
    for quarter in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:
        ...
```
lines up with
```
data_folder/
├─ 10_X_C_2020/
│  ├─ QTR1/
│  │  ├─ 10-K-company.txt
│  ├─ QTR2/
│  ├─ QTR3/
│  ├─ QTR4/
```
Then, in a virtual environment, cd into your project directory and run main.py using
```
python main.py
```

In addition to this, you can use ```generate_stats.py``` to generate summary statistic for your output. To ensure this works, make sure that you have changed the ```output_directory``` variable the same way you did for ```main.py```, then run it using:
```
python generate_stats.py
```

I have included a requirements.txt, but the only dependency is really pandas - and I don't do anything that should be sensitive to versioning.

## Future Improvements and Limitations
The function of the program is somewhat limited in flexibility due to how I hard-coded directory paths into the code in certain locations, which require the user to alter the code to make it function locally. In addition, the locating function of the 10-K is not perfect and is sometimes under or over sensitive to the string matching methods.
To improve this, I would move the directory paths into a configuration file, or have them "inferred" as part of a local file structure. I didn't enforce that the data was stored in the project directory since I was working with the project in OneDrive at the time, and the data was far too large to be stored alongside it.