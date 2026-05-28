import pandas as pd
import requests
import os

def data_pull():
    url = "https://sky.coflnet.com/api/bazaar/ENCHANTED_COCOA/history"
    output_path = os.path.join("data", "raw", "cocoa_beans_historical.csv")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        raw_data = response.json()
        
        # CHECK
        if not raw_data:
            print("Warning: API returned an empty list. Aborting file write.")
            return

        df = pd.DataFrame(raw_data)
        df.to_csv(output_path, index=False)
        print(f"Success: {len(df)} entries saved.")

    except requests.exceptions.RequestException as e:
        print(f"Data pull failed: {e}")