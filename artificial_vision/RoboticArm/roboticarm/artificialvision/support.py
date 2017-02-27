import pickle
from time import sleep

def load_obj (name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
def save_obj (obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
def pxTOcm (toConv, ratioIndex):
    return toConv/ratioIndex

def calibParam ():
    mtx = load_obj("mtx")
    dist = load_obj("dist")
    newcameramtx = load_obj("newcameramtx")
    roi = load_obj("roi")
    return mtx, dist, newcameramtx, roi

def getConvIndex ():
    convIndex = load_obj("convIndex")
    return convIndex