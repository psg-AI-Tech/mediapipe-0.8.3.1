#!/usr/bin/env python3

import os
import sys
# sys.path.append("../")

sys.path.append("/home/zj/_github_/folder_python/mediapipe-0.8.3.1")
sys.path.append("/home/zj/_github_/folder_python/mediapipe-0.8.3.1/mediapipe/python")


import cv2
import numpy as np

import json
import mediapipe as mp


from skeleton_data import skeleton_data
# import trans
from communicate import SocketServer

mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose



inputDataPathBase = "../data/"
absPathBase =os.path.abspath( os.path.join(os.getcwd(),inputDataPathBase))

imageDataPath = absPathBase+"/testData/"
videoPath = absPathBase+ "/video/"

# print("videoPath：",videoPath)
# VIDEO_FILES=[videoPath+"wudao.mp4"]
# VIDEO_FILES=[videoPath+"yujia.mp4"]
VIDEO_FILES=["/media/zj/4CAC1612AC15F764/psg_temp/video_/dance2.mp4"]


# For static images:
IMAGE_FILES = [imageDataPath+"js.webp",
            # "/home/zj/_github_/folder_proj/gesture_recognition_proj/data/testData/js1.webp",
            # "/home/zj/_github_/folder_proj/gesture_recognition_proj/data/testData/js2.webp",
            # "/home/zj/_github_/folder_proj/gesture_recognition_proj/data/testData/js3.jpeg",
            # "/home/zj/_github_/folder_proj/gesture_recognition_proj/data/testData/js4.jpeg",
            ]
BG_COLOR = (192, 192, 192) # gray

def list2dic(list,dic):
    keysList =dic.keys()
    print("keysList",keysList)
    # minLen= min(len(keysList),len(list))
    # TODO 判断大小，防止溢出
    for index, key in enumerate( keysList):
        if(index>=len(list)):
            break
        dic[key]=list[index]



def sendData(sock,list):
    '''
    根据list数据，得到要发送的字典数据
    Args:
        list: 输入，list

    '''
    dic = skeleton_data
    list2dic(list,dic)
    data = json.dumps(dic)
    try:
        sock.send((data.encode('utf-8')))
        return True
    except:
        return False
    

def predict(pose,image):
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.pose_landmarks:
        print("-------error-------")
        return 0,0
    
    # 得到骨骼数据
    skeletonData_list=[]
    # skeletonData_list.clear()
    for i in mp_pose.PoseLandmark:
        # print("===",i)
        width = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width
        heigth = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height
        skeletonData_list.append([width,heigth])
    # print("results: ",type(mp_pose.PoseLandmark.NOSE))
    # print(
    #     f'Nose coordinates: ('
    #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
    #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
    #     f'({results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE_INNER].x * image_width},'
    #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE_INNER].y * image_height})'
    # )

    annotated_image = image.copy()
    mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                # landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                )
    return annotated_image,skeletonData_list



def process():
    #  获取视频输入
    socketserver= SocketServer.SocketServer(SocketServer.PORT)
    # while True:
    #     socketserver.accept() 
    #     # 建立连接后处理数据
    #     handleData(socketserver)
    #     # socketserver.clientConnection.close()
    handleData(socketserver)
        
def handleData(sock):
    
    videoName =VIDEO_FILES[0]

    cap =cv2.VideoCapture(videoName)
    print("inputData: ",videoName)
    # sock=trans.connect() # 客户端
    with mp_pose.Pose(
        static_image_mode=True,
        # model_complexity=1,
        # enable_segmentation=True,
        min_detection_confidence=0.5) as pose:

        # 循环处理 输入图片
        # for idx, file in enumerate(IMAGE_FILES):
        #     print("image file: ",file)
        #     image = cv2.imread(file)
        
        # 循环处理输入视频帧
        while cap.isOpened():
            ret,frame =cap.read()
            # if ret:
            # print("annotated_image",type(annotated_image)) 
            if ret:
                annotated_image,datalist=predict(pose,frame)   
                if isinstance(annotated_image,np.ndarray):
                    print("skeletonData_list: ", len(datalist))            
                    cv2.imshow("videoShow",annotated_image)

                    key =cv2.waitKey(1)
                    if key==27:
                        cap.release()
                        break
                    if not sendData(sock,datalist):
                        break;                     
            else:
                continue
        print("video cap failed!")
        cv2.destroyAllWindows()
        cap.release()


            
            # image_height, image_width, _ = image.shape
            # # Convert the BGR image to RGB before processing.
            # results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            # if not results.pose_landmarks:
            #     continue
            # print(
            #     f'Nose coordinates: ('
            #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
            #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
            #     f'({results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE_INNER].x * image_width},'
            #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE_INNER].y * image_height})'
            # )

            # annotated_image = image.copy()
            # # Draw segmentation on the image.
            # # To improve segmentation around boundaries, consider applying a joint
            # # bilateral filter to "results.segmentation_mask" with "image".
            # condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            # bg_image = np.zeros(image.shape, dtype=np.uint8)
            # bg_image[:] = BG_COLOR
            # annotated_image = np.where(condition, annotated_image, bg_image)
            # Draw pose landmarks on the image.
            # mp_drawing.draw_landmarks(
            #     annotated_image,
            #     results.pose_landmarks,
            #     mp_pose.POSE_CONNECTIONS,
            #     # landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            #     )
            # cv2.imwrite('/home/zj/_github/proj_folder/action_recogniztion/gesture_recognition_proj/output/' + str(idx) + '.png', annotated_image)
    # cv2.imshow(annotated_image)
    # # Plot pose world landmarks.
    # mp_drawing.plot_landmarks(
    #     results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

# # For webcam input:
# cap = cv2.VideoCapture(0)
# with mp_pose.Pose(
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5) as pose:
#   while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#       print("Ignoring empty camera frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       continue

#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image.flags.writeable = False
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = pose.process(image)

#     # Draw the pose annotation on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     mp_drawing.draw_landmarks(
#         image,
#         results.pose_landmarks,
#         mp_pose.POSE_CONNECTIONS,
#         landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
#     # Flip the image horizontally for a selfie-view display.
#     cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap.release()
def getInputData():
    videoName =VIDEO_FILES[0]
    cap =cv2.VideoCapture(videoName)

    while cap.isOpened():
        ret,frame =cap.read()
        if ret:
            cv2.imshow("videoShow",frame)
            key =cv2.waitKey(25)

            if key==27:
                # if key==ord("q"):
                cap.release()
                break
        else:
            break
    cv2.destroyAllWindows()


def main():
    process()
    # getInputData()

if __name__ =="__main__":
  main()