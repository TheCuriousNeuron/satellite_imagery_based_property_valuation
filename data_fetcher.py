# Import libraries
import pandas as pd
import requests
import os
import time
from pathlib import Path

# Set variables, file/folder paths & API Key
API_KEY = 'API Key'  
CSV_FILE = 'CSV File'  
OUTPUT_FOLDER = 'Output Folder'  
LAT_COLUMN = 'lat'  
LONG_COLUMN = 'long' 
ID_COLUMN = 'id' 

# Images parameters
ZOOM_LEVEL = 20  
IMAGE_SIZE = '640x640' 
MAP_TYPE = 'satellite' 

# Output Folder
def create_output_folder(folder_name):
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    print(f"Output folder created: {folder_name}")

# Fetching and saving images
def fetch_satellite_image(lat, lon, property_id, api_key, output_folder):

    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        'center': f'{lat},{lon}',
        'zoom': ZOOM_LEVEL,
        'size': IMAGE_SIZE,
        'maptype': MAP_TYPE,
        'key': api_key
    }   

    try:
        response = requests.get(base_url, params=params, timeout=10) 

        if response.status_code == 200:

            filename = f'{property_id}.png'
            filepath = os.path.join(output_folder, filename) 

            with open(filepath, 'wb') as f:
                f.write(response.content)      

            print(f"Image saved: {filename}")
            return filename
        
        else:
            print(f"Error for property {property_id}: Status {response.status_code}")
            return None     
               
    except Exception as e:
        print(f"Exception for property {property_id}: {str(e)}")
        return None

# Calling function
def main():  

    create_output_folder(OUTPUT_FOLDER)    

    try:
        df = pd.read_csv(CSV_FILE)
        print(f"\nLoaded CSV with {len(df)} rows")

    except FileNotFoundError:
        print(f"ERROR: CSV file '{CSV_FILE}' not found")
        return
    
    except Exception as e:
        print(f"ERROR reading CSV: {str(e)}")
        return
       
    df_clean = df.dropna(subset=[LAT_COLUMN, LONG_COLUMN, ID_COLUMN])
    print(f"\nProcessing {len(df_clean)} properties with valid coordinates and IDs")
    
    successful = 0
    failed = 0
    filenames = []
    
    for idx, row in df_clean.iterrows():
        lat = row[LAT_COLUMN]
        lon = row[LONG_COLUMN]
        index=row[ID_COLUMN]
        print(f"\nFetching image {idx + 1}/{len(df_clean)}: Lat={lat}, Lon={lon}")
        
        filename = fetch_satellite_image(lat, lon, index, API_KEY, OUTPUT_FOLDER)
        
        if filename:
            successful += 1
            filenames.append(filename)
        else:
            failed += 1
            filenames.append(None)
        
        time.sleep(0.5)
    
    print(f"Total properties processed: {len(df_clean)}")
    print(f"Successfully fetched: {successful}")
    print(f"Failed: {failed}")
    print(f"Images saved in: {OUTPUT_FOLDER}")

if __name__ == "__main__":
    main()   