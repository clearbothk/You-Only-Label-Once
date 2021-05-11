# Clearbot 
[Clearbot](https://www.clearbot.dev/ "Clearbot")

* Clearbot is a swarm of trash collecting robots that use AI-Vision to detect and collect trash from water bodies. These robots are fully autonomous, solar-powered and work as a team to remove trash. In comparison to any current solution, Clearbot is 15x cheaper, has 5x more reach and removes 2x more trash daily (24x7x365).

## Project Aim
* Create a model that can label images of trash at ~80% precision & recall to improve on manual label speed.
* Collect and output statistical information about distribution of input images.

## Business Value
* Our solution will allow Clearbot to significantly reduce annotation time.
* Countless man hours saved via the tool will mean long term cost savings and allow more efficient deployment of manpower.

## Project Overview
* Over 4500 photos scraped and labelled to train YOLOv5
* Acheived 92% Precision and 88% Recall on training dataset
* Categories Detected: Bottle, Can, Cup, Box Drink, Face Mask, Plastic Bag

## Code and Resources
**Python Version:** Python 3.7.10 (Google Colab)

**Tensorflow** 2.4.1

**Opencv-python** 4.1.2

**split-folders** 0.4.3

**LabelImg** 1.8.5
 
**Packages:** selenium, tkinter, glob

**Teammates**: [Alex Li's GitHub](https://github.com/ahhhlexli "Alex Li's GitHub") & [lhwj0619's GitHub](https://github.com/lhwj0619 "lhwj0619's GitHub")

# Process

## System Architecture
![alt text](https://github.com/ahhhlexli/clearbot/blob/main/Github%20Images/system_architecture.png "Title")


## Data Collection
* Due to limited testing data, our team scraped images from the following sources:
    * Google Images
    * [TACO Dataset](http://tacodataset.org/ "Taco Dataset")
    * [Kaggle Dataset](https://www.kaggle.com/asdasdasasdas/garbage-classification "Kaggle Dataset") - Plastic 
    * [Trashnet Dataset](https://github.com/garythung/trashnet "Thung & Yang") - Thung & Yang
* Python script used to remove duplicate images and images with low resolutions
* LabelImg was used to annotate images with bounding boxes

## Data Overview
* 6 Classes Bottle, Can, Cup, Box Drink, Face Mask, Plastic Bag
* 5,210 Unique Images
* 9,675 Labels

![alt text](https://github.com/ahhhlexli/clearbot/blob/main/Github%20Images/Distribution%20of%20Training%20Data%20Labels.jpg "Distribution")

## YOLOv5 Modelling
* Experimented with various YOLOv5 models (s/m/l/xl).
* The final model was trained on M after considering accuracy, recall, and training/predicting time.
* The model produced promising results in identifying objects, however object material could not be differentiated. 
    * Our solution was to create a GUI to assign material classes quickly and accurately by human eye instead of having a model mislabel material classes.
![alt text](https://github.com/ahhhlexli/clearbot/blob/main/Github%20Images/YOLO%20Model.jpg "YOLOv5 Model")

![alt text](https://github.com/ahhhlexli/clearbot/blob/main/Github%20Images/YOLO%20Results.jpg "YOLO Results")
## CNN Modelling (Experimented, not implemented)
* Using the same images (cropped) used in the YOLO Model Training, we trained our CNN model to classify the material given an object category. Eg. This a bottle, is it a plastic or glass bottle.
* Material prediction accuracy varied depending on the object category.
* Poor results from this method led us to go with the GUI methodology.

**CNN Model Experimented**
```
model = tf.keras.Sequential([data_augmentation])
model.add(Conv2D(input_shape=(img_height,img_width,3),filters=64,kernel_size=(3,3),padding="same", activation="relu", kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)))
model.add(MaxPooling2D(pool_size=2,)) 
model.add(Dropout(0.2))
model.add(Conv2D(kernel_size = 2, filters = 64, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)))
model.add(Conv2D(kernel_size = 2, filters = 64, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(Conv2D(kernel_size = 2, filters = 128, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)))
model.add(Conv2D(kernel_size = 2, filters = 128, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(Conv2D(kernel_size = 2, filters = 256, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)))
model.add(Conv2D(kernel_size = 2, filters = 256, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)))
model.add(MaxPooling2D(pool_size = 2))
model.add(Dropout(0.2))
model.add(GlobalMaxPooling2D())
#model.add(GlobalAveragePooling2D())
model.add(Dense(num_classes, activation = 'softmax', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)))
```
## Production
* Python scripts created to streamline pipeline process of converting Raw images to images and labels in folders ready for YOLO training.
* Tkinter GUI developed to provide simple interface for quick object and material classifications
* 
![Alt Text](https://github.com/ahhhlexli/clearbot/blob/main/Github%20Images/gui_architecture.png "GUI Architecture")

![Alt Text](https://github.com/ahhhlexli/clearbot/blob/main/Github%20Images/Main%20GUI.jpg "GUI Main")

![Alt Text](https://github.com/ahhhlexli/clearbot/blob/main/Github%20Images/YOLO%20Detection.png "Yolo Detection")

![Alt Text](https://github.com/ahhhlexli/clearbot/blob/main/Github%20Images/Correct.jpg "GUI Correct")

![Alt Text](https://github.com/ahhhlexli/clearbot/blob/main/Github%20Images/Materials.jpg "GUI Materials")

![Alt Text](https://github.com/ahhhlexli/clearbot/blob/main/Github%20Images/stats.jpg "GUI Stats")



## Main Challenges
* Data - Difficult to find quality images of trash in sufficient volume. Limitations on variety of images found via search engines. 
* Model - Material detection is not a mature technology yet.  A lot of theoretical approaches that are difficult to replicate.
* Workflow - Branching into software/UX solution implementation

## Future Improvements
* Alternative Model - Material detection currently done manually. Develop, test and integrate a proven detection model.
* Given more information about the trash found in HK Waters, we can expand the current (6) YOLO object detection to include other object classes
* Relabelling tool relies on LabelImg for incorrect YOLO image predictions. An in-house solution would increase the efficiency and streamline the process.
* Future data capture by Clearbot can be re-fed into the model for improved overall performance.

## Presentation
[PowerPoint](https://github.com/azwinlam/beerpricechecker/blob/main/Beer%20Price%20Checker.pptx)
^ Link to be updated

## File Structure
```
📦Prediction_Pipeline
 ┣ 📂main_functions
 ┃ ┣ 📜main_combine_stats.py
 ┃ ┣ 📜main_convert_images.py
 ┃ ┣ 📜main_correct_check.py
 ┃ ┣ 📜main_crop_images.py
 ┃ ┣ 📜main_filter_app.py
 ┃ ┣ 📜main_image_bound.py
 ┃ ┣ 📜main_load_source.py
 ┃ ┣ 📜main_read_stats.py
 ┃ ┣ 📜main_yolo_check.py
 ┃ ┗ 📜__init__.py
 ┣ 📂relabel_functions
 ┃ ┣ 📜relabel_combine_stats.py
 ┃ ┣ 📜relabel_correct_check.py
 ┃ ┣ 📜relabel_crop_images.py
 ┃ ┣ 📜relabel_filter_app.py
 ┃ ┣ 📜relabel_image_bound.py
 ┃ ┣ 📜relabel_read_stats.py
 ┃ ┗ 📜__init__.py
 ┣ 📜best.pt
 ┣ 📜clearbot.png
 ┣ 📜item_classes.json
 ┣ 📜main_gui.py
 ┣ 📜predefined_classes.txt
 ┣ 📜relabel_gui.py
 ┗ 📜requirements.txt
```

## References
Modelling
* YOLOv5: https://github.com/ultralytics/yolov5

Webscraping
* Image Scraper: https://github.com/debadridtt/Scraping-Google-Images-using-Python

Labelling
* LabelImg: https://github.com/tzutalin/labelImg 

Datasets
* Plastic Images: https://www.kaggle.com/nandinibagga/plastic-images
* Waste Classification Data: https://www.kaggle.com/techsash/waste-classification-data
* Taco Dataset: http://tacodataset.org/ 
* TrashNet Dataset: https://github.com/garythung/trashnet

Research Papers
* Material Recognition: https://openaccess.thecvf.com/content_cvpr_2015/papers/Bell_Material_Recognition_in_2015_CVPR_paper.pdf 



