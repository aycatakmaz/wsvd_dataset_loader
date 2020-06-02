# modified from https://github.com/MohsenFayyaz89/PyTorch_Video_Dataset/blob/master/GeneralVideoDataset.py

from __future__ import print_function, division

import os
import pickle
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset


import requests
from pprint import pprint
 

class WSVD_Sequence_Generator:
    def __init__(self, root_dir='/scratch/takmaza/wsvd_sequences', extract_dir='/scratch-second/takmaza/wsvd_sequences', file_path='wsvd_list_valid.txt', 
                train_clips_list='wsvd_train_clip_frame_ids.pkl', test_clips_list='wsvd_test_clip_frame_ids.pkl',video_root_dir = '/scratch/takmaza/wsvd/wsvd'):

        self.root_dir = root_dir
        self.extract_dir = extract_dir
        self.file_path = file_path
        self.train_clips_list = train_clips_list
        self.test_clips_list = test_clips_list
        self.video_root_dir = video_root_dir
        self.names_set = set()

        with open(self.file_path) as fp:
            for cnt, line in enumerate(fp):
                self.names_set.add(line.strip())

        with open(self.train_clips_list, "rb") as fp:  # Unpickling
            self.train_clips = pickle.load(fp)
        with open(self.test_clips_list, "rb") as fp:  # Unpickling
            self.test_clips = pickle.load(fp)

        self.created_train = {}
        self.created_test = {}

        for ind in range(len(self.train_clips)):
            if self.train_clips[ind]['name'] in self.names_set:
                self.created_train[self.train_clips[ind]['name']] = self.train_clips[ind]['clips']
            elif self.train_clips[ind]['name'][:-5] in self.names_set:
                self.created_train[self.train_clips[ind]['name'][:-5]] = self.train_clips[ind]['clips']

        for ind in range(len(self.test_clips)):
            if self.test_clips[ind]['name'] in self.names_set:
                self.created_test[self.test_clips[ind]['name']] = self.test_clips[ind]['clips']
            elif self.test_clips[ind]['name'][:-5] in self.names_set:
                self.created_test[self.test_clips[ind]['name'][:-5]] = self.test_clips[ind]['clips']

        #print(self.created_train.keys())
        #print(type(self.created_train['Z7p1Qiq6SkM']))
        #print(len(self.created_train['Z7p1Qiq6SkM']))
        #print(self.created_train['Z7p1Qiq6SkM'])
        self.extract_sequences()


    def create_folder(self, directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)

    def extract_sequences(self):
        self.create_folder(self.extract_dir)
        train_dir = os.path.join(self.extract_dir, 'train')
        test_dir = os.path.join(self.extract_dir, 'test')

        self.create_folder(train_dir)
        self.create_folder(test_dir)

        
        print('Printing train sequences')
        name_flag=False
        for name in self.created_train.keys():
            print(name)
            if name=='LeU-WuUNwgc':
                name_flag=True
            if name_flag:
                seq_root_dir = os.path.join(train_dir, name)
                #self.create_folder(seq_root_dir)
                video_file = os.path.join(self.video_root_dir,(name+'.mp4'))
                cap = cv2.VideoCapture(video_file)
                number_of_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                for seq_ind, seq_frames in enumerate(self.created_train[name]):
                    #print(seq_ind)
                    seq_dir = seq_root_dir + '_' + str(seq_ind)
                    self.create_folder(seq_dir)
                    for save_frame_ind, real_frame_ind in enumerate(list(seq_frames['frames'])):
                        frame_save_path = os.path.join(seq_dir, str(save_frame_ind).zfill(5)+'.png')
                        frame=self.retrieve_frame(cap,real_frame_ind)
                        if frame == None:
                            break
                        cv2.imwrite(frame_save_path, frame) 
        

        print('Printing test sequences')

        for name in self.created_test.keys():
            print(name)
            seq_root_dir = os.path.join(test_dir, name)
            #self.create_folder(seq_root_dir)
            video_file = os.path.join(self.video_root_dir,(name+'.mp4'))
            cap = cv2.VideoCapture(video_file)
            number_of_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            for seq_ind, seq_frames in enumerate(self.created_test[name]):
                seq_dir = seq_root_dir + '_' + str(seq_ind)
                self.create_folder(seq_dir)
                for save_frame_ind, real_frame_ind in enumerate(list(seq_frames['frames'])):
                    frame_save_path = os.path.join(seq_dir, str(save_frame_ind).zfill(5)+'.png')
                    frame=self.retrieve_frame(cap,real_frame_ind)
                    cv2.imwrite(frame_save_path, frame) 


    def retrieve_frame(self, cap, frame_ind=0):
        # Open the video file
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_ind)
        ret, frame = cap.read()
        if frame == None:
            return None
        height, width, _  = frame.shape
        left = frame[:,0:int((width/2)),:]
        resized = cv2.resize(left, (0,0), fx=2, fy=1) 
        return resized


    def read_video(self,video_file):
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

new_generator =  WSVD_Sequence_Generator()

#vid_id = '-3Br2RCzmEc'#'-A_ol17l90M'
#ext = '.mp4'
#vid_path = os.path.join(video_root_dir,(vid_id+ext))
#frames,_ = read_video(vid_path)
#print('read it!')

