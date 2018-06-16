#!usr/python/bin
#coding=utf-8
import cv2
import numpy as np

def draw_result(img, result):
    for i in range(len(result)):
        x = int(result[i][1])
        y = int(result[i][2])
        w = int(result[i][3] / 2)
        h = int(result[i][4] / 2)
        cv2.rectangle(img, (x - w, y - h), (x + w, y + h), (0, 255, 0), 2)
        cv2.rectangle(img, (x - w, y - h - 20),
                        (x + w, y - h), (125, 125, 125), -1)
        cv2.putText(img, result[i][0] + ' : %s' % result[i][5], (x - w + 5, y - h - 7), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


def read_result_file(path):
    with open(path,'r') as f:
        for lines in f.readlines():
            line_arr = lines.split(',')
            filename = 'test-public/' + line_arr[0]
            labelname = line_arr[1]
            boxstr = line_arr[2]
            boxarr = boxstr.split(' ')
            boxarr = map(int,boxarr)
            #print(boxarr[0],boxarr[1],boxarr[2],boxarr[3])
            image = cv2.imread(filename)
            result_tmp = []
            data_tmp = [labelname,boxarr[0],boxarr[1],boxarr[2],boxarr[3],filename]
            result_tmp.append(data_tmp)
            draw_result(image,result_tmp)
            cv2.imshow('Image', image)
            key = cv2.waitKey(0)
            print(key)
            if key==27:
                break
            

if __name__ == '__main__':
    path = 'SSD84271result.txt'
    read_result_file(path)
    
            