import os
import subprocess
import pandas as pd
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.bytecodes.axml import AXMLPrinter
import xml.etree.ElementTree as ET

# Function to decode APK with apktool (for APK format)
def decode_apk(apk_file):
    decoded_folder = os.path.join(apk_folder,"APK_decoded", os.path.basename(apk_file) + "_decoded")
    
    if os.path.exists(decoded_folder):
        print(f"Directory {decoded_folder} already exists. Removing it...")
        os.rmdir(decoded_folder)

    try:
        subprocess.check_call(['apktool', 'd', apk_file, '-o', decoded_folder])
        print(f"APK '{apk_file}' successfully decompiled into '{decoded_folder}'.")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to decode APK '{apk_file}' with apktool.")
        return False


# Function to extract dynamic loading features from an APK (for APK format)
def extract_dynamic_loading_features_from_apk(apk_file, dynamic_code_loading_features):
    apk = APK(apk_file)
    feature_counts = {feature: 0 for feature in dynamic_code_loading_features}
    vm = DalvikVMFormat(apk.get_dex())
    methods = vm.get_methods()

    for method in methods:
        method_name = method.get_name()
        if isinstance(method_name, bytes):
            method_name = method_name.decode('utf-8', errors='ignore')
        
        for feature in dynamic_code_loading_features:
            if feature in method_name:
                feature_counts[feature] = 1

    return feature_counts


# Function to extract permissions from an APK (for APK format)
def extract_permissions_from_apk(apk_file, desired_permissions):
    apk = APK(apk_file)
    permissions = apk.get_permissions()
    features = {permission: (1 if permission in permissions else 0) for permission in desired_permissions}
    return features


# Function to extract permissions from a folder containing extracted APK files (for folder format)
def extract_permissions_from_folder(folder_path, desired_permissions):
    manifest_path = os.path.join(folder_path, "AndroidManifest.xml")
    permissions = []
    
    if not os.path.exists(manifest_path):
        print(f"AndroidManifest.xml not found in {folder_path}")
        return {permission: 0 for permission in desired_permissions}
    
    try:
        with open(manifest_path, "rb") as f:
            axml = AXMLPrinter(f.read())
            xml_content = axml.get_xml()
        
        tree = ET.ElementTree(ET.fromstring(xml_content))
        for elem in tree.iter():
            if elem.tag == "uses-permission" and 'name' in elem.attrib:
                permissions.append(elem.attrib['name'])
        
    except Exception as e:
        print(f"Error analyzing AndroidManifest.xml in {folder_path}: {e}")
        return {permission: 0 for permission in desired_permissions}
    
    return {permission: (1 if permission in permissions else 0) for permission in desired_permissions}

# Function to extract dynamic code loading features from a folder containing extracted APK files (for folder format)
def extract_dynamic_loading_features_from_folder(folder_path, dynamic_code_loading_features):
    dex_file_path = os.path.join(folder_path, "classes.dex")
    feature_counts = {feature: 0 for feature in dynamic_code_loading_features}
    
    if not os.path.exists(dex_file_path):
        print(f"DEX file not found in {folder_path}")
        return feature_counts
    
    try:
        with open(dex_file_path, "rb") as f:
            vm = DalvikVMFormat(f.read())
            methods = vm.get_methods()
            
            for method in methods:
                method_name = method.get_name()
                if isinstance(method_name, bytes):
                    method_name = method_name.decode('utf-8', errors='ignore')
                
                for feature in dynamic_code_loading_features:
                    if feature in method_name:
                        feature_counts[feature] = 1
    
    except Exception as e:
        print(f"Error analyzing DEX file in {folder_path}: {e}")
    
    return feature_counts


# Main function to analyze both APK files and folder-extracted APK contents
def analyze_apk(apk_folder, output_file, desired_permissions, dynamic_code_loading_features):
    results = []

    columns = ['APK Name'] + desired_permissions + dynamic_code_loading_features
    
    for apk_file in os.listdir(apk_folder):
        apk_path = os.path.join(apk_folder, apk_file)

        if apk_file.endswith('.apk'):
            print(f"Analyzing APK format: {apk_file}")
            # Decode APK with apktool first
            if not decode_apk(apk_path):
                continue  # Skip this APK if decoding fails
            
            row = {'APK Name': apk_file}
            permissions_features = extract_permissions_from_apk(apk_path, desired_permissions)
            dynamic_loading_features = extract_dynamic_loading_features_from_apk(apk_path, dynamic_code_loading_features)
            row.update(permissions_features)
            row.update(dynamic_loading_features)
            results.append(row)

        elif os.path.isdir(apk_path):
            print(f"Analyzing extracted folder format: {apk_file}")
            row = {'APK Name': apk_file}
            permissions_features = extract_permissions_from_folder(apk_path, desired_permissions)
            dynamic_loading_features = extract_dynamic_loading_features_from_folder(apk_path, dynamic_code_loading_features)
            row.update(permissions_features)
            row.update(dynamic_loading_features)
            results.append(row)
            
    
    df = pd.DataFrame(results, columns=columns)
    df.columns = [col.replace('android.permission.', '') if 'android.permission.' in col else col for col in df.columns]

    # save the DataFrame to Excel
    df.to_excel(output_file, index=False)
    print(f"Feature Extraction Completed and Saved to {output_file}")


apk_folder = 'APK_collected_samples' 
output_file = 'Test_Dataset_created.xlsx'

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

dynamic_code_loading_features = [
    'Runtime.exec', 'HttpGet.init', 'attachInterface', 
    'createSubprocess', 'Ljavax.crypto.Cipher', 'Ljava.lang.Class.getCanonicalName', 
    'Ljava.lang.Class.getMethods', 'Ljava.lang.Class.getDeclaredField', 'Ljava.lang.Class.getResource', 
    'Ljava.lang.Class.forName', 'System.loadLibrary', 'DexClassLoader', 'PathClassLoader', 'transact', 'bindService', 
    'android.os.Binder', 'ClassLoader', 'Runtime.getRuntime', 'Ljava.lang.Class.getMethod', 'Ljava.lang.Class.cast', 
    'HttpPost.init', 'ProcessBuilder'
]


analyze_apk(apk_folder, output_file, overprivileged_permissions, dynamic_code_loading_features)



