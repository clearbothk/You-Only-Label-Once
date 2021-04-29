# clearbot
Capstone - Improve Labelling Speed


## File Structure
```
📦Root
 ┣ 📂labeled_images
 ┃ ┣ 📂images
 ┃ ┗ 📂labels
 ┣ 📂purgepy
 ┃ ┗ 📜purge_all_but_raw_data.py
 ┣ 📂raw_images
 ┃ ┗ 📜IMG_20210405_130122.jpg
 ┣ 📂unlabeled_images
 ┣ 📂yolo_training_data
 ┃ ┣ 📂test
 ┃ ┃ ┣ 📂images
 ┃ ┃ ┗ 📂labels
 ┃ ┣ 📂train
 ┃ ┃ ┣ 📂images
 ┃ ┃ ┗ 📂labels
 ┃ ┗ 📂val
 ┃ ┃ ┣ 📂images
 ┃ ┃ ┗ 📂labels
 ┣ 📜1-Convert_images.py
 ┣ 📜2-Transfer_unlabled_to_labeled.py
 ┣ 📜3-Prepare_for_yolo.py
 ┗ 📜4-Crop_by_bounding_box.py
```