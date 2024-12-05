import os
import pandas as pd
from androguard.core.bytecodes.apk import APK

# Function to extract permissions from apk
def extract_permissions(apk_file, desired_permissions):
    
    apk = APK(apk_file)
    permissions = apk.get_permissions()
    
    features = {permission: (1 if permission in permissions else 0) for permission in desired_permissions}
    
    return features

# Function to loop through all apks in a folder
def analyze_apk(apk_folder, output_file, desired_permissions):
    
    results = []
    
    columns = ['APK Name'] + [f"Permission::{permission}" for permission in desired_permissions]
    
    for apk_file in os.listdir(apk_folder):
        if apk_file.endswith('.apk'):
            apk_path = os.path.join(apk_folder, apk_file)

            # Extract permissions from the APK
            row = {'APK Name': apk_file}
            permissions_features = extract_permissions(apk_path, desired_permissions)
            row.update(permissions_features)

            results.append(row)
    
    # Convert results to a DataFrame
    df = pd.DataFrame(results, columns=columns)
    
    # Save the DataFrame to an Excel file
    df.to_excel(output_file, index=False)
    print(f"Feature Extraction Completed and Saved to {output_file}")


apk_folder = 'APK_samples_extracted'  
output_file = 'Created_Dataset.xlsx'

# Desired permissions to extract
overprivileged_permissions = [
    'android.permission.GET_ACCOUNTS',
    'android.permission.BROADCAST_STICKY',
    'android.permission.ACCESS_NETWORK_STATE',
    'android.permission.READ_CONTACTS',
    'android.permission.CHANGE_NETWORK_STATE',
    'android.permission.BLUETOOTH',
    'android.permission.WAKE_LOCK',
    'android.permission.READ_SMS',
    'android.permission.ACCESS_COARSE_LOCATION',
    'android.permission.VIBRATE'
]

analyze_apk(apk_folder, output_file, overprivileged_permissions)

