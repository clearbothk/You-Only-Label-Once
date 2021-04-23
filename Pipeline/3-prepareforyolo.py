import splitfolders

input_folder = './labeled_images'
output_folder = './yolo_training_data'


splitfolders.ratio(input_folder, output_folder, seed=42, ratio=(.7, .2, .1), group_prefix=None)