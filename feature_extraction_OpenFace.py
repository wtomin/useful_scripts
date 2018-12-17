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
parser.add_argument("--nomask" , action="store_true", help="whether not to mask non face region (default is to mask)")
parser.add_argument("--grey", action="store_true", help="whether to save gray image for saving space")
parser.add_argument("--hog", action="store_true", help="save hog file.")
parser.add_argument("--quiet", action="store_false", help="default stay quiet.")
parser.add_argument("--tracked_vid", action="store_true", help="save tracked video output.")
parser.add_argument("--noface_save", action="store_true", help="if true, those face images where detection is failed will be saved.")
args = parser.parse_args()
def convert_2mp4():
    input_dir = args.input_dir
    output_dir = args.output_dir
    video_input_paths, video_output_dirs = video_reader(input_dir, output_dir)
    length = len(video_input_paths)
    video_index= 0
    for video_input_file, video_output_dir in zip(video_input_paths, video_output_dirs):
        video_index +=1
        print("processing {}/{} \n".format(video_index, length), end='\r')
        video_output_path = video_output_dir+'.mp4'
        if not os.path.isdir(os.path.dirname(video_output_path)):
            os.makedirs(os.path.dirname(video_output_path))
        call = "ffmpeg -i "+ video_input_file + " "+video_output_path
        os.system(call)
        
# change to correct executable file location
OpenFace_FeatureExtraction = "C:/Users/ddeng/Documents/NISL/OpenFace_v2.1.0/OpenFace_2.1.0_win_x64/OpenFace_2.1.0_win_x64/FeatureExtraction.exe"
def video_reader(input_dir, output_dir):
    """
    params:
    input_dir: input directory with videos
    output_dir: the directory that feature will be saved in
    return:
    video_input_paths: input video file paths
    video_output_dirs: output feature storage directory
    """
    video_ext = ['.avi', '.mp4', '.MP4']
    video_input_paths = []
    video_output_dirs = []
    for dirpath, dirname, filenames in os.walk(input_dir):
        if any([ext in filename for ext in video_ext for filename in filenames]):
            video_path = [os.path.join(dirpath, filename) for filename in filenames]
            video_names = [os.path.splitext(filename)[0] for filename in filenames]
            prefix = dirpath.replace(input_dir, output_dir, 1)
            output_video_dirs = [os.path.join(prefix, video_n) for video_n in video_names]
            
            video_input_paths.extend(video_path)
            video_output_dirs.extend(output_video_dirs)
    return video_input_paths, video_output_dirs
def parse_videos():
    input_dir = args.input_dir
    output_dir = args.output_dir
    nomask = args.nomask
    grey = args.grey
    size = args.size    
    quiet_mode = args.quiet
    video_input_paths, video_output_dirs = video_reader(input_dir, output_dir)
    length = len(video_input_paths)
    video_index= 0
    for video_input_file, video_output_dir in zip(video_input_paths, video_output_dirs):
        video_index +=1
        print("processing {}/{} \n".format(video_index, length), end='\r')
        if os.path.isfile(video_input_file):
            if not os.path.isdir(video_output_dir):
                os.makedirs(video_output_dir)
            opface_option = " -f "+video_input_file + " -out_dir "+ video_output_dir +" -simsize "+ str(size)
            # by default HOG and tracked video are not stored (save disk space)
            # and by default, do not output from frames where detection failed or is unreliable (thus saving some disk space)
            opface_option += " -2Dfp -3Dfp -pdmparams -pose -aus -gaze -simalign "
            if not args.noface_save:
                opface_option +=" -nobadaligned "
            if args.hog:
                opface_option += " -hogalign"
            if args.tracked_vid:
                opface_option +=" -tracked "
            if nomask:
                opface_option+= " -nomask"
            if grey:
                opface_option += " -g"
            if quiet_mode:
                opface_option += " -q"
            # execution
            call = OpenFace_FeatureExtraction + opface_option
            os.system(call)
        else:
            print(video_input_file+'does not exist.')
        time.sleep(2)

if __name__ == "__main__":
    parse_videos()
    
