import os
import numpy as np
import glob
import argparse
import time
"""
feature extraction with OpenFace., when input files are video files.
given input_dir and outpu_dir, generating OpenFace features with same saving structure (meaning same subdirectory names)

"""
parser = argparse.ArgumentParser(description='arguments for video face detection and face feature extraction.')
parser.add_argument("-i", "--input_dir", type=str, default=None)
parser.add_argument("-o", "--output_dir", type=str, default=None)
parser.add_argument("--size", type=int, default = 112)
parser.add_argument('--bbox_dir', type=str, default='')
parser.add_argument("--nomask" , action="store_true", help="whether not to mask non face region (default is to mask)")
parser.add_argument("--grey", action="store_true", help="whether to save gray image for saving space")
parser.add_argument("--hog", action="store_true", help="save hog file.")
parser.add_argument("--quiet", action="store_false", help="default stay quiet.")
parser.add_argument("--noface_save", action="store_true", help="if true, those face images where detection is failed will be saved.")
args = parser.parse_args()
# change to correct executable file location
OpenFace_FeatureExtraction = "D:/DDD/OpenFace_2.2.0_win_x64/FaceLandmarkImg.exe"
def read_txt(txt_file): # the format of this txt file: FILE_NAME LEFT_OF_FACE1 TOP_OF_FACE1 WIDTH_OF_FACE1 HEIGHT_OF_FACE1 LEFT_OF_FACE2 TOP_OF_FACE2 WIDTH_OF_FACE2 HEIGHT_OF_FACE2 
    with open(txt_file, 'r') as f:
        lines = f.readlines()
    contents = [x.strip() for x in lines]
    file_names = [x.split(' ')[0] for x in contents]
    bboxes = [x.split(" ")[1:9] for x in contents]
    bboxes = [[max(0, int(t)) for t in x] for x in bboxes]
    bboxes0 = [[x[1], x[0], x[1]+x[3], x[0]+x[2]] for x in bboxes] # (min_x min_y max_x max_y)\
    bboxes1 = [[x[5], x[4], x[5]+x[7], x[4]+x[6]] for x in bboxes]
    data_left = {k:v for k,v in zip(file_names, bboxes0)}
    data_right = {k:v for k, v in zip(file_names, bboxes1)}
    return data_left, data_right
def save_bbox_to_file(save_dir, data_dict):
    for file_name, bbox in data_dict.items():
        save_path = os.path.join(save_dir, file_name.split(".")[0]+".txt")
        with open(save_path, 'w') as f:
            string = ' '.join(['{:d}'.format(x) for x in bbox])
            f.write(string)

def prepare_bbox_dir():
    training_txt = 'D:/DDD/interpersonal_relationship/training.txt'
    testing_txt = 'D:/DDD/interpersonal_relationship/testing.txt'
    save_dir = 'D:/DDD/interpersonal_relationship/bboxes'
    data_left, data_right = read_txt(training_txt)
    test_left, test_right = read_txt(testing_txt)
    data_left.update(test_left)
    data_right.update(test_right)
    save_dir_left = save_dir+"_left"
    save_dir_right = save_dir+"_right"
    if not os.path.exists(save_dir_left):
        os.makedirs(save_dir_left)
    if not os.path.exists(save_dir_right):
        os.makedirs(save_dir_right)
    save_bbox_to_file(save_dir_left, data_left)
    save_bbox_to_file(save_dir_right, data_right)
def prepare_bbox_dir_same():
    training_txt = 'D:/DDD/interpersonal_relationship/training.txt'
    testing_txt = 'D:/DDD/interpersonal_relationship/testing.txt'
    save_dir = 'D:/DDD/interpersonal_relationship/bboxes'
    data_left, data_right = read_txt(training_txt)
    test_left, test_right = read_txt(testing_txt)
    data_left.update(test_left)
    data_right.update(test_right)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for file_name, bbox in data_left.items():
        save_path = os.path.join(save_dir, file_name.split(".")[0]+".txt")
        with open(save_path, 'w') as f:
            string = ' '.join(['{:d}'.format(x) for x in bbox])
            f.write(string+'\n')
    for file_name, bbox in data_right.items():
        save_path = os.path.join(save_dir, file_name.split(".")[0]+".txt")
        with open(save_path, 'a') as f:
            string = ' '.join(['{:d}'.format(x) for x in bbox])
            f.write(string+'\n')

def parse_images():
    input_dir = args.input_dir # input dir contains a lot of images
    output_dir = args.output_dir
    bbox_dir = args.bbox_dir #
    nomask = args.nomask
    grey = args.grey
    size = args.size    
    quiet_mode = args.quiet
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    opface_option = " -fdir "+ args.input_dir + " -out_dir "+ args.output_dir +" -simsize "+ str(size)
    # by default HOG and tracked video are not stored (save disk space)
    # and by default, do not output from frames where detection failed or is unreliable (thus saving some disk space)
    opface_option += " -2Dfp -3Dfp -pdmparams -pose -aus -gaze -simalign"
    if len(bbox_dir)>0:
        opface_option += '-bboxdir '+os.path.abspath(bbox_dir)
    if not args.noface_save:
        opface_option +=" -nobadaligned "
    if args.hog:
        opface_option += " -hogalign"
    if nomask:
        opface_option+= " -nomask"
    if grey:
        opface_option += " -g"
    if quiet_mode:
        opface_option += " -q"
    # execution
    call = OpenFace_FeatureExtraction + opface_option
    os.system(call)

if __name__ == "__main__":

    #prepare_bbox_dir_same()
    parse_images()
    