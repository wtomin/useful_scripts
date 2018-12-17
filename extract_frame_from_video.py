import os
import numpy as np
import glob
import argparse

parser = argparse.ArgumentParser(description='arguments for video face detection and face feature extraction.')
parser.add_argument("-i", "--input_dir", type=str, default=None)
parser.add_argument("-o", "--output_dir", type=str, default=None)
parser.add_argument("--ext", type=str, default = '.jpg')
parser.add_argument("--fps", type=int, default = 30)
args = parser.parse_args()

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
    video_input_paths, video_output_dirs = video_reader(input_dir, output_dir)
    length = len(video_input_paths)
    video_index= 0
    for video_input_file, video_output_dir in zip(video_input_paths, video_output_dirs):
        video_index +=1
        print("processing {}/{} \n".format(video_index, length), end='\r')
        des = os.path.join(video_output_dir, '%06d'+args.ext)
        if not os.path.isdir(os.path.dirname(des)):
            os.makedirs(os.path.dirname(des))
        cmd = 'ffmpeg -i '+video_input_file+' -filter:v fps=fps='+str(args.fps)+' '+des
        os.system(cmd)
if __name__ == "__main__":
    parse_videos()
           
       
