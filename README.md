# Clearbot 
[Clearbot](https://www.clearbot.dev/ "Clearbot")

* Clearbot is a swarm of trash collecting robots that use AI-Vision to detect and collect trash from water bodies. These robots are fully autonomous, solar-powered and work as a team to remove trash. In comparison to any current solution, Clearbot is 15x cheaper, has 5x more reach and removes 2x more trash daily (24x7x365).


# Capstone Project - 
* To help Clearbot improve labelling speed


## Project Aim
* Collaborate with Clearbot to produce a lightweight and efficient auto labelling tool for increased labelling speed. 
* Create an effective model (~80% accuracy) for identifying types of trash on the Clearbot machine.

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

## Data Collection
* Due to limited testing data, our team scraped Google images
* LabelImg was used to annotate images with bounding boxes

## YOLOv5 Modelling
* Experimented with various YOLOv5 models (s/m/l/xl)
* The final model was trained on Large
* The model produced promising results in identifying the object however the material could not be differentiated. This led us to creating a second model to identify material, given an object category.

## CNN Modelling
* Using the same images (cropped) used in the YOLO Model Training, we trained our CNN model to classify the material given an object category. Eg. This a bottle, is it a plastic or glass bottle.
* Material prediction accuracy varied depending on the object category.

**Final CNN Model**
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
* Tkinter GUI being developed to provide simple interface for all the basic functions

## Presentation
[PowerPoint](https://github.com/azwinlam/beerpricechecker/blob/main/Beer%20Price%20Checker.pptx)
^ Link to be updated

## File Structure
```
📦Prediction_Pipeline
 ┣ 📂main_function
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

