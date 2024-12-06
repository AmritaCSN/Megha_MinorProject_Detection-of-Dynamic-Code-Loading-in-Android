# Megha_MinorProject_Detection-of-Dynamic-Code-Loading-in-Android
This repository contains implementation code and necessary data files for the project "Detection of Dynamic Code Loading in Android", focused on identification of dynamic code loading behavior in android malware.

## Overview

Dynamic code loading (DCL) has become a common tactic for bypassing Google Play Store’s security scanning, allowing malicious actors to inject harmful code through app updates, runtime server downloads or pre-packages files in APKs. Recent research revealed gaps in Google’s policies that enable this behaviour, making it a significant threat to android security. This work aims to develop a model to detect dynamic code loading behaviour in android malware while addressing the resource constraints of mobile devices. Unlike previous studies that mostly relied on API calls and permissions, this work focuses on overprivileged permissions (manifest based features) and classes (code-based features) which are characteristic of android malware with DCL behaviour. By combining machine learning technique with this feature set, the model can detect dynamic code loading malware while minimizing resource usage on mobile devices by selecting minimal feature set that reduces model size without compromising predictive performance.

## Experimentation

The performance of classification model with different feature sets was analysed using two datasets. Initially using the MH-100K_Dataset, followed by Android Malware Genome Dataset.

### Datasets used

1. **MH-100K Dataset** 
[1](https://github.com/Malware-Hunter/MH-100K-dataset):
   
   Android Malware dataset of 1,01,975 samples comprising 166 permissions, 24,417 API calls, 250 intents and meta data as features.

2. **Android Malgenome Dataset** 
[2](https://figshare.com/articles/dataset/Android_malware_dataset_for_machine_learning_1/5854590):
   
    The dataset consists of 3799 android app samples, where 2539 are benign, rest 1260 are samples from 49 malware families and 215 features including API calls, permissions.

### Features used
* **Manifest based features**:
  
  Features extracted from manifest file (AndroidManifest.xml). Permissions which are requested but unused in the manifest file, also known as overprivileged permissions are used in this project.
  
*	**Code based features**:
  
    Features extracted from application code. Methods available in classes in the application code that enable dynamic code loading are extracted from classes.dex file (contains compiled bytecode for the app).

## Project files description 

This project is organized into the following:

| **Folder**                    | **File/Folder**                                   | **Description**                                                                                                                                     |
|--------------------------------|--------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| **Data**                       | Test_Dataset_1.xlsx                        | Dataset created using `ExtractPermissions_APK.py` code, for use as a testing set in `Code_Dataset_1.ipynb`.                                        |
|                                | Test_Dataset_2.xlsx                        | Dataset created using `ExtractFeatures_APK_Folder.py` code, for use as a testing set in `Code_Dataset_2.ipynb`. |
| **Notebooks**                  | Code_Dataset_1.ipynb                       | Code for analyzing model performance with different feature sets using the MH-100K Dataset.                                                       |
|                                | Code_Dataset_2.ipynb                       | Code for analyzing model performance with different feature sets using the Android Malgenome Dataset.                                               |
| **Scripts**                    | ZIP_extract_script.sh                      | Script to unzip compressed APKs into a folder.                                                                                                     |
|                                | ExtractPermissions_APK.py                  | Code to extract desired permissions from APK samples.                                                                                             |
|                                | ExtractFeatures_APK.py                     | Code to extract permissions and additional features from APK samples or APK in folder format.                                                     |

## Architectural Diagram

![image](https://github.com/user-attachments/assets/d790f313-2523-4fe1-8112-5259fe206a53)



## Flow of Project Code

Listed below is the common sequence of experimentation followed for each of the datasets:

1. **Import the Dataset**
   - Load the dataset as an excel file.

2. **Dataset Splitting**
   - Split the dataset into a training and testing set.

3. **Declaring Feature Sets**
   - Create lists with different sets of features.
   - The feature set of all features in the dataset is taken as the baseline.

4. **Model Training and Testing for Each Feature Set**
   - Extract Smaller Train and Test Sets:
     - Extract a smaller train and test set containing feature columns from each feature set.
   - Training and Testing Models:
     - Train a classification model and test it using the test set for each feature set.

5. **Comparison of Model Performance**
   - Compare performance of models for different feature sets, keeping the full feature set as the baseline.
   - Model performance is evaluated by analyzing variation of the following metrics against number of features: Number of true positives, number of false negatives, f1-score, training and testing time and reduction in F1-score with respect to the baseline.

6. **Choosing the Optimal Model**
   - Choose model with optimal performance on the metrics analyzed in previous step.

7. **Feature Analysis**
   - The correct and misclassified samples are analyzed to observe the effect of selected features based on feature distribution.

8. **Testing with New Samples**
   - Collect APK samples to create a testset.
   - Use python scripts to extract features and create a test set from the collected APK files.
     
9. **Model Testing with the Created Test Set**
     - The model is tested using the created test set.
  
## How-to: Set up and Run the project

<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align:center;">Dependencies</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Oracle VirtualBox</strong></td>
      <td>Used to set up a virtual machine running Ubuntu to download APK samples and create test sets.</td>
    </tr>
    <tr>
      <td><strong>Androguard</strong></td>
      <td>Used for analyzing APK files for feature extraction.</td>
    </tr>
    <tr>
      <td><strong>APKTool</strong></td>
      <td>Used for analyzing APK files for feature extraction.</td>
    </tr>
    <tr>
      <td><strong>Python</strong></td>
      <td>Used for automation of feature extraction, model training, and testing.</td>
    </tr>
    <tr>
      <td><strong>Shell Scripting</strong></td>
      <td>Used to automate the extraction of APK files from compressed format.</td>
    </tr>
    <tr>
      <td><strong>Visual Studio Code</strong></td>
      <td>Installed with Jupyter Notebook and Python extensions to run the main code for model training, testing, and results analysis.</td>
    </tr>
  </tbody>
</table>

1. 	Clone the repository
2. 	Datasets are available in /data folder.
3.  Run the code books:
   
    * Start with Code_Dataset_1.iypnb: Analysis focused on using only manifest based permissions as features. 
    * Then Run Code_Dataset_2.iypnb: Analysis using permissions and along with code based features.
---








