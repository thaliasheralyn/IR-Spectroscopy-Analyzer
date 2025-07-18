# -*- coding: utf-8 -*-
"""AI_Pyhton_Final Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Cy3G5TECH915yE7EdBQHYC6BeivWMCrG

**Formaldehyde**
"""

import csv
import math
def read_jdx_file(file_path):

#Reads a JCAMP-DX file, extracts the X and Y values, and returns a list of (x, y) pairs.
    with open(file_path, 'r') as file:
        lines = file.readlines()

    x_values = []
    y_values = []
    superX_values=[]
    superY_values=[]

    # Skip all lines that start with '#' and begin processing the data
    data_started = False
    for line in lines:
        line = line.strip()

        # Skip lines that did not start with a number
        if not line or not line[0].isdigit():
            continue

        # If we encounter a non-# line, data starts
        data_started = True

        # Process data lines only
        if data_started and line:
            # Split the line into individual values
            values = list(map(float, line.split()))

            superX_values.append(values[0])  # First value is X
            superY_values.append(values[1:])  # Remaining values are Y
      #result -> superX_values=[x1, x6, ...] superY_values=[(y1,y2,y3,y4,y5), (y6, y7, y8, y9, y10), ...

    for x in superX_values:
      x_values.append(x)
      x_values.append(x+1)
      x_values.append(x+2)
      x_values.append(x+3)
      x_values.append(x+4)
    #result -> x_values=[x1, x2, x3,...]

    for ys in superY_values:
      for y in ys:
        y_values.append(y)
    #result -> y_values=[y1, y2, y3,...]

    if not x_values or not y_values:
        raise ValueError("No data found in the JCAMP-DX file.")

    return x_values, y_values
    #result -> x_values=[x1, x2, x3,...] y_values=[y1, y2, y3,...]

    try:
        with open(file_path, "r") as file:
            for line in file.readlines()[36:]:  # Skip the first 36 lines
                if line.strip():  # Ignore empty lines
                    try:
                        x, y = map(float, line.split())
                        if y != 0:  # Exclude lines with y = 0
                            x_values.append(x)
                            y_values.append(y)
                    except ValueError:
                        # Skip lines that cannot be parsed as numbers
                        continue
    except FileNotFoundError:
        raise Exception(f"File {file_path} not found.")

    return x_values, y_values

def generate_xy_pairs(x_values, y_values):
    """
    Converts the list of X values and corresponding list of Y values into (x, y) pairs.
    """
    xy_pairs = []
    counter=0
    while counter < len(y_values):
      y=y_values[counter]
      x=x_values[counter]
      if y==0:
        xy_pairs.append((x, y))
      else:
         y=-math.log(y,10)
         xy_pairs.append((x, y))
      counter+=1
    return xy_pairs
    #result: [(x1, y1), (x2, y2), (x3, y3), ...]

def save_xy_to_csv(output_path, xy_pairs):

#Saves the (x, y) pairs to a CSV file.
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(["Wavenumber", "Absorbance"])

        # Write the (x, y) pairs
        for x, y in xy_pairs:
            writer.writerow([x, y])

# Main function
if __name__ == "__main__":
    input_file = "formaldehyde.jdx"  # Replace with the path to your JCAMP-DX file
    output_file = "formaldehyde.csv"  # Output file for (x, y) pairs in CSV format

    try:
        # Read the .jdx file, skipping the first 36 lines
        x_values, y_values = read_jdx_file(input_file)

        # Generate the (x, y) pairs
        xy_pairs = generate_xy_pairs(x_values, y_values)

        # Save the results to a .csv file
        save_xy_to_csv(output_file, xy_pairs)

        print(f"Converted (x, y) data saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
from ipywidgets import interact, widgets
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from tabulate import tabulate
from IPython.display import display

# Load data
data = pd.read_csv('formaldehyde.csv')

# Check for peaks in 'Absorbance'
# Calculate the mean and standard deviation for threshold
mean_height = data['Absorbance'].mean()
std_height = data['Absorbance'].std()
threshold = mean_height + std_height

# Find peaks above the threshold
peak_indices, properties = find_peaks(data['Absorbance'], height=threshold)

# Loop through all the peaks and check for nearby peaks
unique_peak_indices = []
max_distance = 15  # The distance for overlapping peaks

for i in peak_indices:
    is_unique = True
    for j in unique_peak_indices:
        if abs(data['Wavenumber'][i] - data['Wavenumber'][j]) < max_distance:
            if data['Absorbance'][i] > data['Absorbance'][j]:
                unique_peak_indices.remove(j)
                unique_peak_indices.append(i)
            is_unique = False
            break
    if is_unique:
        unique_peak_indices.append(i)

# Create label: 1 if there's a peak, otherwise 0
data['label'] = 0
data.loc[unique_peak_indices, 'label'] = 1

# Visualize data to verify peaks
plt.figure(figsize=(10, 6))
plt.plot(data['Wavenumber'], data['Absorbance'], label='Absorbance')
plt.scatter(data.loc[unique_peak_indices, 'Wavenumber'], data.loc[unique_peak_indices, 'Absorbance'], color='red', label='Peaks')
plt.xlabel('Wavenumber')
plt.ylabel('Absorbance')
plt.title('Absorbance vs Wavenumber with Peak Detection')
plt.legend()
plt.show()
print("\n")

# Dictionary for functional groups
functional_groups = {
    "C‒H Alkanes": (3000, 2850),
    "C‒H Alkanes ‒CH3": [(1450, 1450), (1375, 1375)],
    "C‒H Alkanes ‒CH2‒": (1465, 1465),
    "C‒H Alkenes": (3100, 3000),
    "C‒H Aromatics": [(3150, 3050), (900, 690)],
    "C‒H Alkyne": (3300, 3300),
    "C‒H Aldehyde": [(2900, 2800), (2800, 2700)],
    "C=C Alkene": (1680, 1600),
    "C=C Aromatic": [(1600, 1600), (1475, 1475)],
    "C≡C Alkyne": (2250, 2100),
    "C=O Aldehyde": (1740, 1720),
    "C=O Ketone": (1725, 1705),
    "C=O Carboxylic acid": [(1725, 1700), (3400, 2400)],
    "C=O Ester": (1750, 1730),
    "C=O Amide": (1670, 1640),
    "C=O Anhydride": [(1810, 1810), (1760, 1760)],
    "C=O Acid chloride": (1800, 1800),
    "C‒O Alcohols, Ethers, Esters": (1300, 1000),
    "O‒H Alcohols, Phenols (Free)": (3650, 3600),
    "O‒H Alcohols, Phenols (H-Bonded)": (3500, 3200),
    "N‒H Primary and Secondary Amines": [(3500, 3100), (1640, 1550)],
    "C‒N Amines": (1350, 1000),
    "C=N Imines and Oximes": (1690, 1640),
    "C≡N Nitriles": (2260, 2240),
    "X=C=Y Allenes, Ketenes, Isocyanates": (2270, 1950),
    "N=O Nitro (R-NO2)": [(1550, 1550), (1350, 1350)],
    "S‒H Mercaptans": (2550, 2550),
    "S=O Sulfoxides": (1050, 1050),
    "C‒X Fluoride": (1400, 1000),
    "C‒X Chloride": (800, 600),
    "C‒X Bromide and Iodide": (667, 0),
}

def combined_analysis(start_wavenumber=None, end_wavenumber=None):
    print("\n")

    # Filter data based on the user-defined range
    if start_wavenumber and end_wavenumber:
        filtered_data = data[(data['Wavenumber'] >= start_wavenumber) & (data['Wavenumber'] <= end_wavenumber)]
        unique_peak_indices_filtered = [i for i in unique_peak_indices if start_wavenumber <= data['Wavenumber'][i] <= end_wavenumber]
    else:
        filtered_data = data
        unique_peak_indices_filtered = unique_peak_indices

    if len(unique_peak_indices_filtered) == 0:
        print("No peaks detected in the selected range. Please select another range.")
        return

    peak_values = filtered_data.loc[unique_peak_indices_filtered, ['Wavenumber', 'Absorbance']]
    peak_values['Wavenumber'] = peak_values['Wavenumber'].astype(float)
    peak_values['Absorbance'] = peak_values['Absorbance'].astype(float)

    # Identify the highest peak
    highest_peak_index = peak_values['Absorbance'].idxmax()
    highest_peak_row = peak_values.loc[highest_peak_index]

    # Prepare rows for the combined table
    table_data = []

    # Header row for the table
    table_data.append(["Wavenumber", "Functional Groups", "Absorbance", "Peak Intensity"])

    # Define thresholds for categorization of high, medium, and low
    peak_heights = peak_values['Absorbance'].values
    high_threshold = np.percentile(peak_heights, 80)  # Top 20%
    low_threshold = np.percentile(peak_heights, 20)   # Bottom 20%

    # Loop through each peak to add functional groups and intensity categorization
    for index, row in peak_values.iterrows():
        wavenumber = row['Wavenumber']
        absorbance = row['Absorbance']
        matched_groups = []

        # Find matching functional groups
        for group, value in functional_groups.items():
            if isinstance(value[0], int):  # Single range
                high, low = value
                if low <= wavenumber <= high:
                    matched_groups.append(group)
            else:  # Multiple ranges
                for high, low in value:
                    if low <= wavenumber <= high:
                        matched_groups.append(group)

        # Categorize peak intensity
        category = "High" if absorbance >= high_threshold else "Low" if absorbance <= low_threshold else "Medium"

        # Style the highest peak row
        if index == highest_peak_index:
            wavenumber = f"\033[1m\033[31m{wavenumber:.2f}\033[0m"  # Bold + Red
            category = f"\033[1m\033[31m{category}\033[0m"          # Bold + Red

        # Add row to the table
        functional_groups_str = ', '.join(matched_groups) if matched_groups else "No matching functional group"
        table_data.append([wavenumber, functional_groups_str, category])

    # Print the combined table
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    print("\n")

# Interactive analysis for a user-defined range
def interactive_analysis():
    interact(
        analyze_range,
        start=widgets.FloatText(value=data['Wavenumber'].min(), description='Start Wavenumber:'),
        end=widgets.FloatText(value=data['Wavenumber'].max(), description='End Wavenumber:')
    )

# Function to analyze the selected range
def analyze_range(start, end):
    combined_analysis(start, end)

print(f"Default range: Start Wavenumber = {data['Wavenumber'].min():.2f}, End Wavenumber = {data['Wavenumber'].max():.2f}")
print("If you wish to analyze a specific range, you can enter the range below:")
interactive_analysis()

"""**Phenol**"""

import csv
import math
def read_jdx_file(file_path):

#Reads a JCAMP-DX file, extracts the X and Y values, and returns a list of (x, y) pairs.
    with open(file_path, 'r') as file:
        lines = file.readlines()

    x_values = []
    y_values = []
    superX_values=[]
    superY_values=[]

    # Skip all lines that start with '#' and begin processing the data
    data_started = False
    for line in lines:
        line = line.strip()

        # Skip lines that did not start with a number
        if not line or not line[0].isdigit():
            continue

        # If we encounter a non-# line, data starts
        data_started = True

        # Process data lines only
        if data_started and line:
            # Split the line into individual values
            values = list(map(float, line.split()))

            superX_values.append(values[0])  # First value is X
            superY_values.append(values[1:])  # Remaining values are Y
      #result -> superX_values=[x1, x6, ...] superY_values=[(y1,y2,y3,y4,y5), (y6, y7, y8, y9, y10), ...

    for x in superX_values:
      x_values.append(x)
      x_values.append(x+1)
      x_values.append(x+2)
      x_values.append(x+3)
      x_values.append(x+4)
    #result -> x_values=[x1, x2, x3,...]

    for ys in superY_values:
      for y in ys:
        y_values.append(y)
    #result -> y_values=[y1, y2, y3,...]

    if not x_values or not y_values:
        raise ValueError("No data found in the JCAMP-DX file.")

    return x_values, y_values
    #result -> x_values=[x1, x2, x3,...] y_values=[y1, y2, y3,...]

    try:
        with open(file_path, "r") as file:
            for line in file.readlines()[36:]:  # Skip the first 36 lines
                if line.strip():  # Ignore empty lines
                    try:
                        x, y = map(float, line.split())
                        if y != 0:  # Exclude lines with y = 0
                            x_values.append(x)
                            y_values.append(y)
                    except ValueError:
                        # Skip lines that cannot be parsed as numbers
                        continue
    except FileNotFoundError:
        raise Exception(f"File {file_path} not found.")

    return x_values, y_values

def generate_xy_pairs(x_values, y_values):
    """
    Converts the list of X values and corresponding list of Y values into (x, y) pairs.
    """
    xy_pairs = []
    counter=0
    while counter < len(y_values):
      y=y_values[counter]
      x=x_values[counter]
      if y==0:
        xy_pairs.append((x, y))
      else:
         y=-math.log(y,10)
         xy_pairs.append((x, y))
      counter+=1
    return xy_pairs
    #result: [(x1, y1), (x2, y2), (x3, y3), ...]

def save_xy_to_csv(output_path, xy_pairs):

#Saves the (x, y) pairs to a CSV file.
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(["Wavenumber", "Absorbance"])

        # Write the (x, y) pairs
        for x, y in xy_pairs:
            writer.writerow([x, y])

# Main function
if __name__ == "__main__":
    input_file = "phenol.jdx"  # Replace with the path to your JCAMP-DX file
    output_file = "phenol.csv"  # Output file for (x, y) pairs in CSV format

    try:
        # Read the .jdx file, skipping the first 36 lines
        x_values, y_values = read_jdx_file(input_file)

        # Generate the (x, y) pairs
        xy_pairs = generate_xy_pairs(x_values, y_values)

        # Save the results to a .csv file
        save_xy_to_csv(output_file, xy_pairs)

        print(f"Converted (x, y) data saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

import numpy as np
from ipywidgets import interact, widgets
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from tabulate import tabulate
from IPython.display import display

# Load data
data = pd.read_csv('phenol.csv')

# Check for peaks in 'Absorbance'
# Calculate the mean and standard deviation for threshold
mean_height = data['Absorbance'].mean()
std_height = data['Absorbance'].std()
threshold = mean_height + std_height

# Find peaks above the threshold
peak_indices, properties = find_peaks(data['Absorbance'], height=threshold)

# Loop through all the peaks and check for nearby peaks
unique_peak_indices = []
max_distance = 15  # The distance for overlapping peaks

for i in peak_indices:
    is_unique = True
    for j in unique_peak_indices:
        if abs(data['Wavenumber'][i] - data['Wavenumber'][j]) < max_distance:
            if data['Absorbance'][i] > data['Absorbance'][j]:
                unique_peak_indices.remove(j)
                unique_peak_indices.append(i)
            is_unique = False
            break
    if is_unique:
        unique_peak_indices.append(i)

# Create label: 1 if there's a peak, otherwise 0
data['label'] = 0
data.loc[unique_peak_indices, 'label'] = 1

# Visualize data to verify peaks
plt.figure(figsize=(10, 6))
plt.plot(data['Wavenumber'], data['Absorbance'], label='Absorbance')
plt.scatter(data.loc[unique_peak_indices, 'Wavenumber'], data.loc[unique_peak_indices, 'Absorbance'], color='red', label='Peaks')
plt.xlabel('Wavenumber')
plt.ylabel('Absorbance')
plt.title('Absorbance vs Wavenumber with Peak Detection')
plt.legend()
plt.show()
print("\n")

# Dictionary for functional groups
functional_groups = {
    "C‒H Alkanes": (3000, 2850),
    "C‒H Alkanes ‒CH3": [(1450, 1450), (1375, 1375)],
    "C‒H Alkanes ‒CH2‒": (1465, 1465),
    "C‒H Alkenes": (3100, 3000),
    "C‒H Aromatics": [(3150, 3050), (900, 690)],
    "C‒H Alkyne": (3300, 3300),
    "C‒H Aldehyde": [(2900, 2800), (2800, 2700)],
    "C=C Alkene": (1680, 1600),
    "C=C Aromatic": [(1600, 1600), (1475, 1475)],
    "C≡C Alkyne": (2250, 2100),
    "C=O Aldehyde": (1740, 1720),
    "C=O Ketone": (1725, 1705),
    "C=O Carboxylic acid": [(1725, 1700), (3400, 2400)],
    "C=O Ester": (1750, 1730),
    "C=O Amide": (1670, 1640),
    "C=O Anhydride": [(1810, 1810), (1760, 1760)],
    "C=O Acid chloride": (1800, 1800),
    "C‒O Alcohols, Ethers, Esters": (1300, 1000),
    "O‒H Alcohols, Phenols (Free)": (3650, 3600),
    "O‒H Alcohols, Phenols (H-Bonded)": (3500, 3200),
    "N‒H Primary and Secondary Amines": [(3500, 3100), (1640, 1550)],
    "C‒N Amines": (1350, 1000),
    "C=N Imines and Oximes": (1690, 1640),
    "C≡N Nitriles": (2260, 2240),
    "X=C=Y Allenes, Ketenes, Isocyanates": (2270, 1950),
    "N=O Nitro (R-NO2)": [(1550, 1550), (1350, 1350)],
    "S‒H Mercaptans": (2550, 2550),
    "S=O Sulfoxides": (1050, 1050),
    "C‒X Fluoride": (1400, 1000),
    "C‒X Chloride": (800, 600),
    "C‒X Bromide and Iodide": (667, 0),
}

def combined_analysis(start_wavenumber=None, end_wavenumber=None):
    print("\n")

    # Filter data based on the user-defined range
    if start_wavenumber and end_wavenumber:
        filtered_data = data[(data['Wavenumber'] >= start_wavenumber) & (data['Wavenumber'] <= end_wavenumber)]
        unique_peak_indices_filtered = [i for i in unique_peak_indices if start_wavenumber <= data['Wavenumber'][i] <= end_wavenumber]
    else:
        filtered_data = data
        unique_peak_indices_filtered = unique_peak_indices

    if len(unique_peak_indices_filtered) == 0:
        print("No peaks detected in the selected range. Please select another range.")
        return  # Exit the function if no peaks are found

    peak_values = filtered_data.loc[unique_peak_indices_filtered, ['Wavenumber', 'Absorbance']]
    peak_values['Wavenumber'] = peak_values['Wavenumber'].astype(float)
    peak_values['Absorbance'] = peak_values['Absorbance'].astype(float)

    # Identify the highest peak
    highest_peak_index = peak_values['Absorbance'].idxmax()
    highest_peak_row = peak_values.loc[highest_peak_index]

    # Prepare rows for the combined table
    table_data = []

    # Header row for the table
    table_data.append(["Wavenumber", "Functional Groups", "Absorbance", "Peak Intensity"])

    # Define thresholds for categorization of high, medium, and low
    peak_heights = peak_values['Absorbance'].values
    high_threshold = np.percentile(peak_heights, 80)  # Top 20%
    low_threshold = np.percentile(peak_heights, 20)   # Bottom 20%

    # Loop through each peak to add functional groups and intensity categorization
    for index, row in peak_values.iterrows():
        wavenumber = row['Wavenumber']
        absorbance = row['Absorbance']
        matched_groups = []

        # Find matching functional groups
        for group, value in functional_groups.items():
            if isinstance(value[0], int):  # Single range
                high, low = value
                if low <= wavenumber <= high:
                    matched_groups.append(group)
            else:  # Multiple ranges
                for high, low in value:
                    if low <= wavenumber <= high:
                        matched_groups.append(group)

        # Categorize peak intensity
        category = "High" if absorbance >= high_threshold else "Low" if absorbance <= low_threshold else "Medium"

        # Style the highest peak row
        if index == highest_peak_index:
            wavenumber = f"\033[1m\033[31m{wavenumber:.2f}\033[0m"  # Bold + Red
            category = f"\033[1m\033[31m{category}\033[0m"          # Bold + Red

        # Add row to the table
        functional_groups_str = ', '.join(matched_groups) if matched_groups else "No matching functional group"
        table_data.append([wavenumber, functional_groups_str, category])

    # Print the combined table
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    print("\n")

# Interactive analysis for a user-defined range
def interactive_analysis():
    interact(
        analyze_range,
        start=widgets.FloatText(value=data['Wavenumber'].min(), description='Start Wavenumber:'),
        end=widgets.FloatText(value=data['Wavenumber'].max(), description='End Wavenumber:')
    )

# Function to analyze the selected range
def analyze_range(start, end):
    combined_analysis(start, end)

print(f"Default range: Start Wavenumber = {data['Wavenumber'].min():.2f}, End Wavenumber = {data['Wavenumber'].max():.2f}")
print("If you wish to analyze a specific range, you can enter the range below:")
interactive_analysis()

"""**Salicylic Acid**"""

import csv
import math
def read_jdx_file(file_path):

#Reads a JCAMP-DX file, extracts the X and Y values, and returns a list of (x, y) pairs.
    with open(file_path, 'r') as file:
        lines = file.readlines()

    x_values = []
    y_values = []
    superX_values=[]
    superY_values=[]

    # Skip all lines that start with '#' and begin processing the data
    data_started = False
    for line in lines:
        line = line.strip()

        # Skip lines that did not start with a number
        if not line or not line[0].isdigit():
            continue

        # If we encounter a non-# line, data starts
        data_started = True

        # Process data lines only
        if data_started and line:
            # Split the line into individual values
            values = list(map(float, line.split()))

            superX_values.append(values[0])  # First value is X
            superY_values.append(values[1:])  # Remaining values are Y
      #result -> superX_values=[x1, x6, ...] superY_values=[(y1,y2,y3,y4,y5), (y6, y7, y8, y9, y10), ...

    for x in superX_values:
      x_values.append(x)
      x_values.append(x+1)
      x_values.append(x+2)
      x_values.append(x+3)
      x_values.append(x+4)
    #result -> x_values=[x1, x2, x3,...]

    for ys in superY_values:
      for y in ys:
        y_values.append(y)
    #result -> y_values=[y1, y2, y3,...]

    if not x_values or not y_values:
        raise ValueError("No data found in the JCAMP-DX file.")

    return x_values, y_values
    #result -> x_values=[x1, x2, x3,...] y_values=[y1, y2, y3,...]

    try:
        with open(file_path, "r") as file:
            for line in file.readlines()[36:]:  # Skip the first 36 lines
                if line.strip():  # Ignore empty lines
                    try:
                        x, y = map(float, line.split())
                        if y != 0:  # Exclude lines with y = 0
                            x_values.append(x)
                            y_values.append(y)
                    except ValueError:
                        # Skip lines that cannot be parsed as numbers
                        continue
    except FileNotFoundError:
        raise Exception(f"File {file_path} not found.")

    return x_values, y_values

def generate_xy_pairs(x_values, y_values):
    """
    Converts the list of X values and corresponding list of Y values into (x, y) pairs.
    """
    xy_pairs = []
    counter=0
    while counter < len(y_values):
      y=y_values[counter]
      x=x_values[counter]
      if y==0:
        xy_pairs.append((x, y))
      else:
         y=-math.log(y,10)
         xy_pairs.append((x, y))
      counter+=1
    return xy_pairs
    #result: [(x1, y1), (x2, y2), (x3, y3), ...]

def save_xy_to_csv(output_path, xy_pairs):

#Saves the (x, y) pairs to a CSV file.
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(["Wavenumber", "Absorbance"])

        # Write the (x, y) pairs
        for x, y in xy_pairs:
            writer.writerow([x, y])

# Main function
if __name__ == "__main__":
    input_file = "salicylic acid.jdx"  # Replace with the path to your JCAMP-DX file
    output_file = "salicylic acid.csv"  # Output file for (x, y) pairs in CSV format

    try:
        # Read the .jdx file, skipping the first 36 lines
        x_values, y_values = read_jdx_file(input_file)

        # Generate the (x, y) pairs
        xy_pairs = generate_xy_pairs(x_values, y_values)

        # Save the results to a .csv file
        save_xy_to_csv(output_file, xy_pairs)

        print(f"Converted (x, y) data saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

import numpy as np
from ipywidgets import interact, widgets
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from tabulate import tabulate
from IPython.display import display

# Load data
data = pd.read_csv('salicylic acid.csv')

# Check for peaks in 'Absorbance'
# Calculate the mean and standard deviation for threshold
mean_height = data['Absorbance'].mean()
std_height = data['Absorbance'].std()
threshold = mean_height + std_height

# Find peaks above the threshold
peak_indices, properties = find_peaks(data['Absorbance'], height=threshold)

# Loop through all the peaks and check for nearby peaks
unique_peak_indices = []
max_distance = 15  # The distance for overlapping peaks

for i in peak_indices:
    is_unique = True
    for j in unique_peak_indices:
        if abs(data['Wavenumber'][i] - data['Wavenumber'][j]) < max_distance:
            if data['Absorbance'][i] > data['Absorbance'][j]:
                unique_peak_indices.remove(j)
                unique_peak_indices.append(i)
            is_unique = False
            break
    if is_unique:
        unique_peak_indices.append(i)

# Create label: 1 if there's a peak, otherwise 0
data['label'] = 0
data.loc[unique_peak_indices, 'label'] = 1

# Visualize data to verify peaks
plt.figure(figsize=(10, 6))
plt.plot(data['Wavenumber'], data['Absorbance'], label='Absorbance')
plt.scatter(data.loc[unique_peak_indices, 'Wavenumber'], data.loc[unique_peak_indices, 'Absorbance'], color='red', label='Peaks')
plt.xlabel('Wavenumber')
plt.ylabel('Absorbance')
plt.title('Absorbance vs Wavenumber with Peak Detection')
plt.legend()
plt.show()
print("\n")

# Dictionary for functional groups
functional_groups = {
    "C‒H Alkanes": (3000, 2850),
    "C‒H Alkanes ‒CH3": [(1450, 1450), (1375, 1375)],
    "C‒H Alkanes ‒CH2‒": (1465, 1465),
    "C‒H Alkenes": (3100, 3000),
    "C‒H Aromatics": [(3150, 3050), (900, 690)],
    "C‒H Alkyne": (3300, 3300),
    "C‒H Aldehyde": [(2900, 2800), (2800, 2700)],
    "C=C Alkene": (1680, 1600),
    "C=C Aromatic": [(1600, 1600), (1475, 1475)],
    "C≡C Alkyne": (2250, 2100),
    "C=O Aldehyde": (1740, 1720),
    "C=O Ketone": (1725, 1705),
    "C=O Carboxylic acid": [(1725, 1700), (3400, 2400)],
    "C=O Ester": (1750, 1730),
    "C=O Amide": (1670, 1640),
    "C=O Anhydride": [(1810, 1810), (1760, 1760)],
    "C=O Acid chloride": (1800, 1800),
    "C‒O Alcohols, Ethers, Esters": (1300, 1000),
    "O‒H Alcohols, Phenols (Free)": (3650, 3600),
    "O‒H Alcohols, Phenols (H-Bonded)": (3500, 3200),
    "N‒H Primary and Secondary Amines": [(3500, 3100), (1640, 1550)],
    "C‒N Amines": (1350, 1000),
    "C=N Imines and Oximes": (1690, 1640),
    "C≡N Nitriles": (2260, 2240),
    "X=C=Y Allenes, Ketenes, Isocyanates": (2270, 1950),
    "N=O Nitro (R-NO2)": [(1550, 1550), (1350, 1350)],
    "S‒H Mercaptans": (2550, 2550),
    "S=O Sulfoxides": (1050, 1050),
    "C‒X Fluoride": (1400, 1000),
    "C‒X Chloride": (800, 600),
    "C‒X Bromide and Iodide": (667, 0),
}

def combined_analysis(start_wavenumber=None, end_wavenumber=None):
    print("\n")

    # Filter data based on the user-defined range
    if start_wavenumber and end_wavenumber:
        filtered_data = data[(data['Wavenumber'] >= start_wavenumber) & (data['Wavenumber'] <= end_wavenumber)]
        unique_peak_indices_filtered = [i for i in unique_peak_indices if start_wavenumber <= data['Wavenumber'][i] <= end_wavenumber]
    else:
        filtered_data = data
        unique_peak_indices_filtered = unique_peak_indices

    if len(unique_peak_indices_filtered) == 0:
        print("No peaks detected in the selected range. Please select another range.")
        return  # Exit the function if no peaks are found

    peak_values = filtered_data.loc[unique_peak_indices_filtered, ['Wavenumber', 'Absorbance']]
    peak_values['Wavenumber'] = peak_values['Wavenumber'].astype(float)
    peak_values['Absorbance'] = peak_values['Absorbance'].astype(float)

    # Identify the highest peak
    highest_peak_index = peak_values['Absorbance'].idxmax()
    highest_peak_row = peak_values.loc[highest_peak_index]

    # Prepare rows for the combined table
    table_data = []

    # Header row for the table
    table_data.append(["Wavenumber", "Functional Groups", "Absorbance", "Peak Intensity"])

    # Define thresholds for categorization of high, medium, and low
    peak_heights = peak_values['Absorbance'].values
    high_threshold = np.percentile(peak_heights, 80)  # Top 20%
    low_threshold = np.percentile(peak_heights, 20)   # Bottom 20%

    # Loop through each peak to add functional groups and intensity categorization
    for index, row in peak_values.iterrows():
        wavenumber = row['Wavenumber']
        absorbance = row['Absorbance']
        matched_groups = []

        # Find matching functional groups
        for group, value in functional_groups.items():
            if isinstance(value[0], int):  # Single range
                high, low = value
                if low <= wavenumber <= high:
                    matched_groups.append(group)
            else:  # Multiple ranges
                for high, low in value:
                    if low <= wavenumber <= high:
                        matched_groups.append(group)

        # Categorize peak intensity
        category = "High" if absorbance >= high_threshold else "Low" if absorbance <= low_threshold else "Medium"

        # Style the highest peak row
        if index == highest_peak_index:
            wavenumber = f"\033[1m\033[31m{wavenumber:.2f}\033[0m"  # Bold + Red
            category = f"\033[1m\033[31m{category}\033[0m"          # Bold + Red

        # Add row to the table
        functional_groups_str = ', '.join(matched_groups) if matched_groups else "No matching functional group"
        table_data.append([wavenumber, functional_groups_str, category])

    # Print the combined table
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    print("\n")

# Interactive analysis for a user-defined range
def interactive_analysis():
    interact(
        analyze_range,
        start=widgets.FloatText(value=data['Wavenumber'].min(), description='Start Wavenumber:'),
        end=widgets.FloatText(value=data['Wavenumber'].max(), description='End Wavenumber:')
    )

# Function to analyze the selected range
def analyze_range(start, end):
    combined_analysis(start, end)

print(f"Default range: Start Wavenumber = {data['Wavenumber'].min():.2f}, End Wavenumber = {data['Wavenumber'].max():.2f}")
print("If you wish to analyze a specific range, you can enter the range below:")
interactive_analysis()

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Load data
data = pd.read_csv('phenol.csv')


# Check for peaks in 'absorbance'
# Define peak detection logic (you can fine-tune parameters as needed)
peak_indices, _ = find_peaks(data['Absorbance'], height=0.4)  # Adjust 'height' as necessary

# Create label: 1 if there's a peak, otherwise 0
data['label'] = 0
data.loc[peak_indices, 'label'] = 1

# Visualize data to verify peaks
plt.figure(figsize=(10, 6))
plt.plot(data['Wavenumber'], data['Absorbance'], label='Absorbance')
plt.scatter(data.loc[peak_indices, 'Wavenumber'], data.loc[peak_indices, 'Absorbance'], color='red', label='Peaks')
plt.xlabel('Wavenumber')
plt.ylabel('Absorbance')
plt.title('Absorbance vs Wavenumber with Peak Detection')
plt.legend()
plt.show()

# Features and target
X = data[['Wavenumber', 'Absorbance']]  # Feature columns
y = data['label']  # Target label

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train a KNN model
knn = KNeighborsClassifier(n_neighbors=3)  # You can tune 'n_neighbors'
knn.fit(X_train, y_train)

# Evaluate the model
accuracy = knn.score(X_test, y_test)
print(f'Model Accuracy: {accuracy:.2f}')

# Predict on new data
y_pred = knn.predict(X_test)

# Display whether peaks are detected in the range
for i, pred in enumerate(y_pred):
        if pred == 1:
            print(f"Peak detected in data sample {i} within the range.")

#functional group dictionary
functional_groups = {
    "C‒H Alkanes": (3000, 2850),
    "C‒H Alkanes ‒CH3": [(1450, 1450), (1375, 1375)],
    "C‒H Alkanes ‒CH2‒": (1465, 1465),
    "C‒H Alkenes": (3100, 3000),
    "C‒H Aromatics": [(3150, 3050), (900, 690)],
    "C‒H Alkyne": (3300, 3300),
    "C‒H Aldehyde": [(2900, 2800), (2800, 2700)],
    "C=C Alkene": (1680, 1600),
    "C=C Aromatic": [(1600, 1600), (1475, 1475)],
    "C≡C Alkyne": (2250, 2100),
    "C=O Aldehyde": (1740, 1720),
    "C=O Ketone": (1725, 1705),
    "C=O Carboxylic acid": [(1725, 1700), (3400, 2400)],
    "C=O Ester": (1750, 1730),
    "C=O Amide": (1670, 1640),
    "C=O Anhydride": [(1810, 1810), (1760, 1760)],
    "C=O Acid chloride": (1800, 1800),
    "C‒O Alcohols, Ethers, Esters": (1300, 1000),
    "O‒H Alcohols, Phenols (Free)": (3650, 3600),
    "O‒H Alcohols, Phenols (H-Bonded)": (3500, 3200),
    "N‒H Primary and Secondary Amines": [(3500, 3100), (1640, 1550)],
    "C‒N Amines": (1350, 1000),
    "C=N Imines and Oximes": (1690, 1640),
    "C≡N Nitriles": (2260, 2240),
    "X=C=Y Allenes, Ketenes, Isocyanates": (2270, 1950),
    "N=O Nitro (R-NO2)": [(1550, 1550), (1350, 1350)],
    "S‒H Mercaptans": (2550, 2550),
    "S=O Sulfoxides": (1050, 1050),
    "C‒X Fluoride": (1400, 1000),
    "C‒X Chloride": (800, 600),
    "C‒X Bromide and Iodide": (667, 0),
}
peak_values = data.loc[peak_indices, ['Wavenumber', 'Absorbance']]
peak_values['Wavenumber'] = peak_values['Wavenumber'].astype(float)
peak_values['Absorbance'] = peak_values['Absorbance'].astype(float)  # Absorbance is typically a float


for index, row in peak_values.iterrows():
    wavenumber = row['Wavenumber']
    absorbance = row['Absorbance']
    print_stuff = []  # List to store the matched functional groups
    true = 0
    for group, value in functional_groups.items():
        if isinstance(value[0], int):  # single range
            high, low = value
            if low <= wavenumber <= high:
                print_stuff.append(group)
                true = 1
        else:  # multiple ranges
            for high, low in value:
                if low <= wavenumber <= high:
                    print_stuff.append(group)
                    true = 1
    # Print the results for the current wavenumber
    if true == 1:
        print(f"For Wavenumber {wavenumber:.2f}: {', '.join(print_stuff)}")