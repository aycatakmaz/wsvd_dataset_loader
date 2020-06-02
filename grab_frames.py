  
import cv2
import os
import numpy as np

def read_video(video_file):
    # Open the video file
    cap = cv2.VideoCapture(video_file)
    print(video_file)
    failed_clip = False
    frames = []
    for f in range(21000):
        ret, frame = cap.read()
        #print('shape: ', frame.shape)
        if ret:
            # HWC2CHW
            #frame = np.transpose(frame,(2, 0, 1))
            if f==8500:
                #col_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                col_img = frame
                height, width, _  = col_img.shape
                print(col_img.shape)
                left = col_img[:,0:int((width/2)),:]
                resized = cv2.resize(left, (0,0), fx=2, fy=1) 
                cv2.imwrite('buraya.jpg', resized ) 
        else:
            print(f)
            print("Skipped!")
            failed_clip = True
            break
    return np.asarray(frames), failed_clip

def read_video2(video_file):
    # Open the video file
    cap = cv2.VideoCapture(video_file)
    number_of_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 260)
    failed_clip = False
    frames = []
    ret, frame = cap.read()
    col_img = frame
    height, width, _  = col_img.shape
    print(col_img.shape)
    left = col_img[:,0:int((width/2)),:]
    resized = cv2.resize(left, (0,0), fx=2, fy=1) 
    cv2.imwrite('yenifoto.jpg', resized ) 
    return frame

video_root_dir = '/scratch/takmaza/wsvd/wsvd'
vid_id = '-3Br2RCzmEc'#'-A_ol17l90M'
ext = '.mp4'
vid_path = os.path.join(video_root_dir,(vid_id+ext))
frames= read_video2(vid_path)
print('read it!')

