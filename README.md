# Image Stereo-Pairs

## Problem we are trying to solve

**Project Description** - "*Create a software system that produces an image stereo-pair from a single, ortho-corrected image and a height (depth) field with identical sample spacing.  Ortho-corrected satellite imagery and the corresponding pixel-for-pixel height fields are readily available and are used as inputs to scientific models.  We seek a process that will create an image stereo-pair for visualization purposes, utilizing the two readily available sources above.  We are interested in software to both create and validate the process.*"

We - Abemelech, Deepak, Sofonias, and Soobin (ADSS) - are planning on creating an interface for users to input *Ortho-corrected satellite imagery* with depth field data and output stereo-pair images.

## Installation
To use this software, clone this repository and install the required dependencies:

### For Windows
```
git clone https://github.com/your-repository/stereo-depth.git
cd stereo-depth
python -m venv venv
venv/Script/activate 
pip install -r requirements.txt
```

### For Linux/Mac
```bash
git clone https://github.com/your-repository/stereo-depth.git
cd stereo-depth
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

## Usage
To use the software, provide the left and right stereo images as inputs. The software supports two main operations: --execute for processing and generating depth maps, and --validate for validating generated maps against provided depth maps.

Execution
```bash
python main.py --execute -l path/to/left_image.jpg -r path/to/right_image.jpg -b <baseline> -f <focal-length pixel>
```
This command processes the provided stereo images to generate a depth map. The results will be saved as 'test.png'.

**NOTE**: We have example images in the images folder for testing purposes (Baseline = 0.6, Focal-length in pixel = 645.24)

## Validation
```bash
python main.py --validate -l path/to/left_image.jpg -r path/to/right_image.jpg  -b <baseline> -f <focal-length pixel> -d path/to/provided_depth_map.csv
```
This command validates the generated depth map against the provided reference depth map. The accuracy metrics will be displayed in the console.
