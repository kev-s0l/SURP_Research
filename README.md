# SURP_Research Research Toolkit
This repository contains a comprehensive suite of Python scripts designed for the extraction, analysis, and visualization of multi-modal data from infants. The toolkit focuses on integrating data from three primary sources:

  * **LENA (Language Environment Analysis)**: For measuring a child's linguistic environment.
  * **Accelerometry**: For quantifying sleep-related movement patterns.
  * **EEG (Electroencephalography)**: For classifying sleep stages.

The primary goal of this project is to explore the feasibility of using non-invasive behavioral data to identify early developmental markers in infants, particularly those at high familial risk for autism. This toolkit represents a custom data processing and analysis pipeline, enabling researchers to preprocess, visualize, and identify potential correlations between sleep, movement, and language development.

-----

### File Structure

The repository is organized into three main directories, each containing a set of specialized Python scripts. Each script is designed to process data from a specific source, as noted below.

```
/
├── LENA ANALYSIS/                  # Scripts for LENA data processing
│   ├── ITS EXTRACTOR.py            # Processes data from LENA .its files
│   └── LENA_AWC_CTC_CVC.py
│
├── MOVEMENT ANALYSIS/              # Scripts for accelerometry data processing
│   ├── Accel_Magnitude.py          # Processes data from APDM Opal h5 files
│   ├── Bowely_Skew_stat.py         # Processes data from APDM Opal h5 files
│   ├── CoV_stat.py                 # Processes data from APDM Opal h5 files
│   ├── head_accel.py               # Processes data from APDM Opal h5 files
│   ├── head_accel_metrics.py       # Processes data from APDM Opal h5 files
│   ├── head_accel_visualizer.py    # Processes data from APDM Opal h5 files
│   ├── raw_movement_stat.py        # Processes data from APDM Opal h5 files
│   ├── scalar_speed_stat.py        # Processes data from APDM Opal h5 files
│   ├── skew_stat.py                # Processes data from APDM Opal h5 files
│   └── zcr_stat.py                 # Processes data from APDM Opal h5 files
│
└── SLEEP ANALYSIS/                 # Scripts for EEG and sleep profile analysis
    ├── better_sleep_stages.py      # Processes data from SOMNOmedics DOMINO .edf files
    ├── ICA_HighRisk02_SleepStagesV4.py # Processes data from SOMNOmedics DOMINO .edf files
    └── sleep_profile_line_graph.py # Processes data from SOMNOmedics DOMINO sleep scoring text files
```

-----

### Getting Started

#### Prerequisites

All scripts require a Python environment and several standard scientific computing libraries. You can install all necessary packages using `pip`:

```bash
pip install h5py numpy pandas matplotlib mne scipy seaborn
```

#### Data and Configuration

Most scripts are designed to work with proprietary data files and require you to configure file paths and sensor IDs before running. Please open the relevant script and update the following lines to match your local data:

  * **For all scripts:** ` filename = r'path/to/your/file.h5'  ` or `edf_file_path = r'path/to/your/file.edf'`
  * **For movement scripts:** `target_ID = 'Your_Sensor_ID'`
  * **For sleep scripts:** `sleep_file = r'path/to/your/sleep_profile.txt'`

-----

### Core Functionality

This toolkit is a custom-built solution for a multi-modal analysis pipeline, comprising 18 custom Python scripts.

#### LENA Analysis

These scripts process LENA audio recordings to quantify an infant's linguistic environment.

  * **`ITS EXTRACTOR.py`**: This core script parses the raw, proprietary LENA XML (`.its`) file format. It extracts granular data on every audio segment and conversation, including timestamps, speaker type, and utterance counts, providing a deep level of control over the analysis.
  * **`LENA_AWC_CTC_CVC.py`**: This script takes the extracted data and computes key language metrics such as **Adult Word Count (AWC)**, **Child Vocalization Count (CVC)**, and **Conversational Turns Count (CTC)**. It then generates a summary and visualizations of these metrics.

#### Movement Analysis

This set of scripts processes accelerometer data to quantify subtle movement patterns during sleep. From the raw 3-axis data, the scripts compute a variety of sophisticated metrics for each 30-second epoch.

  * **Movement Magnitude, Instantaneous Speed, and Zero-Crossing Rate (ZCR)**: These scripts measure the overall intensity, velocity, and "restlessness" of movements.
  * **Coefficient of Variation (CoV)** and **Skewness**: These statistical measures quantify the variability and asymmetry of motor activity, which are important because "heightened motor variability" has been shown to be "predictive of cognitive outcomes in toddlers with autism".

#### Sleep Analysis

These scripts analyze EEG data to classify and visualize sleep stages.

  * **`better_sleep_stages.py` & `ICA_HighRisk02_SleepStagesV4.py`**: These scripts use the **MNE-Python** library to process raw EEG data. They apply a bandpass filter and use **Independent Component Analysis (ICA)** to automatically remove artifacts like eye blinks and muscle movements. The processed data is then used to classify sleep states based on brainwave power.
  * **`sleep_profile_line_graph.py`**: This script is for visualizing pre-annotated sleep profiles from a text file, providing a quick way to generate a line plot of sleep progression over time.
