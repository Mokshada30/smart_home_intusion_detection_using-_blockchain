import os
import pandas as pd

folder = r"C:\Users\malim\OneDrive\Desktop\smart_home_ids_project\data\N_BaIoT_csv"

device_map = {
    "1": "Philips_B120N10_Baby_Monitor",
    "2": "Danmini_Doorbell",
    "3": "Ecobee_Smart_Thermostat",
    "4": "Samsung_SNH_1011_N_Webcam",
    "5": "SimpleHome_XCS7_1003_WHT_Security_Camera",
    "6": "TP_Link_Smart_Plug",
    "7": "Insteon_Smart_Plug",
    "8": "SimpleHome_XCS7_1002_WHT_Security_Camera",
    "9": "SimpleHome_XCS7_1003_WHT_Security_Camera"
}

dfs = []
for fname in os.listdir(folder):
    if fname.endswith(".csv"):
        prefix = fname.split(".")[0]
        device = device_map.get(prefix, "Unknown_Device")
        df = pd.read_csv(os.path.join(folder, fname))
        df['device'] = device

        # derive intrusion label from filename
        if "benign" in fname.lower():
            df['intrusion_label'] = 0
        else:
            df['intrusion_label'] = 1

        dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv(r"C:\Users\malim\OneDrive\Desktop\smart_home_ids_project\data\combined_nbaiot.csv", index=False)
print("Combined dataset saved: combined_nbaiot.csv")
