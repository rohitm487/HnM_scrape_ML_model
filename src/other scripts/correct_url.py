import csv
import pandas as pd
def convert_image_paths(input_filename, output_filename="converted_image_paths.csv"):
    with open(input_filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        
        image_paths = []
        for row in reader:
            if len(row) > 0:
                image_path = row[0].strip()
                if image_path.startswith("//"):
                    full_url = "https:" + image_path
                    image_paths.append([full_url])
                else:
                    image_paths.append([image_path])
    
    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image Path"])
        writer.writerows(image_paths)

  
input_filename = "male_short.csv"  # Replace with your actual input CSV file
output_filename = "converted_" + input_filename
convert_image_paths(input_filename, output_filename)