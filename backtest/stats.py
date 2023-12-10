#!/usr/bin/env python3

import glob

# Create a list to store all the file paths
file_paths = glob.glob('./results/X*')  # Replace 'path/to/files/' with the actual path to your files

results = {}  # Dictionary to store the results

# Process each file
for file_path in file_paths:
    with open(file_path, 'r') as file:
        #lines = file.readlines()[:20]  # Read the first 20 lines from the file
        lines = file.readlines()  # Read all lines from the file
        for line in lines:
            # Split the line by multiple spaces
            parts = line.split()
            if len(parts) >= 4:
                name = parts[0]
                percentage = float(parts[2])
                # Update the results dictionary
                if name in results:
                    results[name].append(percentage)
                else:
                    results[name] = [percentage]

# Calculate the average percentage for each name
averages = {name: sum(percentages) / len(percentages) for name, percentages in results.items()}

# Sort the averages dictionary by value (average percentage) in descending order
sorted_averages = sorted(averages.items(), key=lambda x: x[1], reverse=True)

# Print the sorted results
for name, average_percentage in sorted_averages:
    average_percentage = int(average_percentage)  # Convert average to an integer
    print(f"Script: {name} | Average Percentage: {average_percentage}")

