import urllib.request
import os
import csv

# Function to download image from URL and save as JPEG
def download_image(url, save_folder):
    try:
        # Download image using urllib
        response = urllib.request.urlopen(url)
        image_data = response.read()

        # Ensure the save folder exists
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Extract filename from URL
        filename = os.path.basename(url)

        # Ensure the file extension is .jpg
        if not filename.lower().endswith('.jpg'):
            filename = filename + '.jpg'

        # Save image with a unique incremental count in the filename
        count = 1
        while os.path.exists(os.path.join(save_folder, f"image{count}.jpg")):
            count += 1

        filename = f"image{count}.jpg"

        with open(os.path.join(save_folder, filename), 'wb') as f:
            f.write(image_data)

        print(f"Downloaded image: {filename}")
        return True

    except Exception as e:
        print(f"Failed to download image from {url}: {str(e)}")
        return False

# Main function to process CSV file and download images
def process_csv(csv_file, save_folder):
    # Read CSV file and extract image URLs
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if exists
        for row in reader:
            if row:
                url = row[0].strip()  # Assuming the URL is in the first column
                download_image(url, save_folder)

# Example usage
csv_file = 'female.csv'  # Replace with your CSV file containing image URLs
save_folder = 'downloaded_images'  # Specify the folder to save downloaded images

# Process CSV file and download images
process_csv(csv_file, save_folder)
