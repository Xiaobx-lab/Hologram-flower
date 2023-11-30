import subprocess

import cv2
import numpy as np

def makeHologram(original,scale=0.5,scaleR=4,distance=0):
    '''
        Create 3D hologram from image (must have equal dimensions)
    '''
    
    height = int((scale*original.shape[0]))
    width = int((scale*original.shape[1]))
    
    image = cv2.resize(original, (width, height), interpolation = cv2.INTER_CUBIC)
    
    up = image.copy()
    down = rotate_bound(image.copy(),180)
    right = rotate_bound(image.copy(), 90)
    left = rotate_bound(image.copy(), 270)
#------------
    # brightness_value = 50
    # up = np.int16(up)
    # up = up + brightness_value
    # up = np.clip(up, 0, 255)
    # up = np.uint8(up)
#----------



    hologram = np.zeros([max(image.shape)*scaleR+distance,max(image.shape)*scaleR+distance,3], image.dtype)
    
    center_x = (hologram.shape[0])/2
    center_y = (hologram.shape[1])/2
    
    vert_x = (up.shape[0])/2
    vert_y = (up.shape[1])/2
    hologram[0:int(up.shape[0]), int(center_x-vert_x+distance):int(center_x+vert_x+distance)] = up
    hologram[ int(hologram.shape[1]-down.shape[1]):int(hologram.shape[1]) , int(center_x-vert_x+distance):int(center_x+vert_x+distance)] = down
    hori_x = (right.shape[0])/2
    hori_y = (right.shape[1])/2
    hologram[ int(center_x-hori_x) : int(center_x-hori_x+right.shape[0]) , int(hologram.shape[1]-right.shape[0]+distance) : int(hologram.shape[1]+distance)] = right
    hologram[ int(center_x-hori_x) : int(center_x-hori_x+left.shape[0]) , int(0+distance) : int(left.shape[0]+distance )] = left
    
    # cv2.imshow("up",up)
    # cv2.imshow("down",down)
    # cv2.imshow("left",left)
    # cv2.imshow("right",right)
    # cv2.imshow("hologram",hologram)
    # cv2.waitKey()
    return hologram

def process_video_holo(video,name):
    cap = cv2.VideoCapture(video)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    holo = None
    ret = False
    if(not ret):
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 640), interpolation = cv2.INTER_CUBIC)
            holo = makeHologram(frame)

    out = cv2.VideoWriter('vids/holo_{}.mp4'.format(name),fourcc, 30.0, (holo.shape[0],holo.shape[1]))
    print('output_frame_size:',holo.shape[0],holo.shape[1])
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    count = 0
    print("Processing %d frames"%(total_frames))
    while(True):
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 640), interpolation = cv2.INTER_CUBIC)
            holo = makeHologram(frame)
            # print('outpout_shape:',holo.shape[0],holo.shape[1])
            out.write(holo)
            count += 1
            # print("Total:%d of %d"%(count,total_frames))
        if(count>=total_frames-1):
            break
    # Release everything if job is finished
    cap.release()
    out.release()
    output_path = 'vids/holo_{}.mp4'.format(name)
    result = subprocess.run("ffmpeg -i "+output_path+ "-c:v libx265 -crf 26 -preset fast"+ "res/"+output_path, shell=True, capture_output=True, text=True)
    return "res"+output_path


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))
    
if __name__ == '__main__' :
    orig = cv2.imread('bear.jpg')
    orig = cv2.resize(orig, (640, 640), interpolation = cv2.INTER_CUBIC)
    holo = makeHologram(orig,scale=1)
    # process_video_holo("test.avi","test")
    cv2.imwrite("hologram.png",holo)
