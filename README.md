# mask-rcnn-using-synthetic-data

## Abstract
The durability of construction materials is mainly controlled by the rate of absorption of water by cement pastes. Therefore, it is necessary to find a way to accurately measure and estimate the water absorption as a function of time. However, the traditional approach via ASTM C1585 standard test method makes it not only difficult to estimate but also fails to provide accurate results as it can only estimate by weighing the sample at specific time intervals.

As a result, we present a new approach to water absorption estimation by leveraging image segmentation with Mask R-CNN to effectively estimate the water absorption of cement pastes accurately. In addition, we study a new approach to image segmentation. Prior work on image segmentation mainly uses manually annotated natural images as training data. Instead, we seek to find whether synthetic models can partially (i.e. combination of real and synthetic image dataset) or fully replace natural images for an image segmentation task for measuring water absorption in cement pastes. The automatically generated synthetic images can significantly reduce the overhead of manual annotation and provide more accurate boundaries to be fed into Mask R-CNN.

## Introduction 
Statistical learning methods have been utilized in the last decades to automate processes and reduce extensive human-based efforts. Specifically, machine learning and deep learning approcahes are implemented to automate processes by which algorithmic models are developed and trained using specific inputs and datasets. Supervised learning refers to training models whereas the dataset used is labeled using ground-truths. That is, for each training example input, the ground-truth label is known. To automate certain processes through a machine learning pipeline that uses image-processing techniques, the first step is to detect regions of interests (ROIs) in images that relate to the objects that are intended to be detected. 

The widely used classifier in deep learning for the purpose of image-processing is Convolutional Neural Networks (CNNs) that classifies whether a certain object is found in the image or not. Moreover, a Regional Convolutional Neural Network (R-CNN) utilizes CNNs to localize ROIs of objects to be detected. Finally, Masked R-CNN is a pixel-wise image segmentation network that classifies each pixel to a certain class and then segments pixels of the same class using a unique mask. The input dataset to Mask R-CNN is images that contain objects of interest and associated with them are ground-truth labels represented in the form of a mask. Masks are created manually through annotation tools, and then are feeded to the Mask R-CNN to train a model to automatically detect those objects for general images without further training. 

Nonetheless, the process of manually annotating images is a tedious and consuming prcoess and requires significant amount of time and human resources. Therefore, developing a further algorithm that annotates images and creates masks automatically will be a major breakthrough towards the process of full automation. The automatically created labels or masks are called synthetic images because they were synthesized by an algorithm without human interference or annotation. In this study, both manually annotated images and synthetic images are produced for a dataset of a cement paste specimen to train Mask R-CNN to detect water absorption level. Results are compared between manually annotated labels and synthetic labels by computing model efficiency and error for each dataset type.    

## Theory 
Mask R-CNN is built upon Faster R-CNN, which proposes a method for real-time object detection with Region Proposal Networks (RPN). Mask R-CNN is a 2-stage framework, where the first stage extracts features by passing the image through a CNN backbone architecture based on ResNet, which outputs feature maps. Then, using the feature maps, RPN proposes regions by using sliding window technique on k anchor boxes. The second stage then extracts features from each candidate box using RoIAlign and it performs classification, bounding-box regression, and outputs binary masks for each RoI “in parallel” to be used for instance segmentation. 

One of the key differences of Mask R-CNN from other R-CNN is that it uses Feature Pyramid Network (FPN) for more effective backbone for feature extraction. It extracts the RoI features from different levels and the high level features are passed down to lower layers, allowing the features at every level to have access to features at lower and higher levels. 

Another key difference is that it maintains spatial structure of masks by introducing pixel-to-pixel correspondence when finding RoIs because RoIPool that was used in Faster R-CNN had to quantize a floating-number RoI to the discrete integer number of the feature map dimension, which introduced misalignments between the RoI and the extracted features. After predicting m x m mask from each RoI using an Fully-Convolutional Network, RoIAlign computes the value of each sampling point in each of 2 x 2 bins by bilinear interpolation from the nearby grid points on the feature map and this removes the quantization of the stride. Together with FCN and RoIAlign, Mask R-CNN is able to achieve pixel-to-pixel behavior, preserving spatial orientation of features with zero loss of data.

As seen from the brief analysis of Mask R-CNN above, we believe that it is the most suitable choice for our purpose in analyzing image data to identify water level from the cement paste specimens as we are estimating pixel-level water absorption.


## Methods 

We found the manual annotation via CVAT to be very unergonomic and wasteful on our sample dataset. 
For every video, the borders of the subject doesn't change, only the height of the water.
To remedy this, we developed an alternate way to annotate using a stylus. 

We first draw the boundary of the subject (in blue) as well as a reference point (in red) to flood fill from.
![](data/fast_annotation_1.png)


Then for each frame of the video, we just need to annotate the water level (in blue), making annotation much faster.
![](data/fast_annotation_2.png)

We then use the script [flood_fill_helper.ipynb](src/flood_fill_helper.ipynb) to unionize the water level annotation 
and boundary, then flood fill from the red reference point up to the bounds of the subject and water level to create our ground truth masks.
![](data/fast_annotation_mask.png)


## Dataset

### Real & Synthetic Images 

![alt-text](https://github.com/tonyjoo974/mask-rcnn-using-synthetic-models/blob/master/data/prog_rep_img1_u.jpg)

#### Real-time Measurements 

![alt-text](https://github.com/tonyjoo974/mask-rcnn-using-synthetic-models/blob/master/data/combined_gif12.gif)

![alt-text](https://github.com/tonyjoo974/mask-rcnn-using-synthetic-models/blob/master/data/prog_rep_img2.jpg)


## Discussion 

## Conclusions

