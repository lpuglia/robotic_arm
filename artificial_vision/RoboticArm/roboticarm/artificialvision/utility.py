'''
Created on Feb 13, 2017

@author: luca
'''

import cv2
import pickle

def load_obj (name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)