import pandas as pd
import requests

def data_pull():
    # Coflnet -- Hypixel Minecraft Market endpoint for Cocoa Bean Prices
    url = "https://sky.coflnet.com/api/bazaar/INK_SACK:3/history"

    print("Pinging historical data servers")
    response = requests.get(url)

    if response.status_code == 200:  ## If Successful Pull, then ... 
        raw_data = response.json()

        # Coflnet provides an explicit historical list mapping target records
        # Adjust dictionary parsing keys based on their raw payload schema
        df = pd.DataFrame(raw_data)

        # Convert standard time field to date-time objects
        if "time" in df.columns:
            df["Timestamp"] = pd.to_datetime(df["time"])

        df.to_csv("data/raw/cocoa_beans_historical.csv", index=False)
        
        print(f"Successfully Downloaded {len(df)} time-series entries.")
        
    else:                            ## Else, return error code ...
        print(
            f"Server query failed. Status Code: {response.status_code}"
        )