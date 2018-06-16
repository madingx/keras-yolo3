#!usr/python/bin
#coding=utf-8
import cv2
import numpy as np
import xml.etree.ElementTree as ET

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


def calcu_IOU(Reframe,GTframe):
    """
    自定义函数，计算两矩形 IOU，传入为均为矩形对角线，（x,y）  坐标。
    """
    x1 = Reframe[0]
    y1 = Reframe[1]
    width1 = Reframe[2]-Reframe[0]
    height1 = Reframe[3]-Reframe[1]

    x2 = GTframe[0]
    y2 = GTframe[1]
    width2 = GTframe[2]-GTframe[0]
    height2 = GTframe[3]-GTframe[1]

    endx = max(x1+width1,x2+width2)
    startx = min(x1,x2)
    width = width1+width2-(endx-startx)

    endy = max(y1+height1,y2+height2)
    starty = min(y1,y2)
    height = height1+height2-(endy-starty)

    if width <=0 or height <= 0:
        ratio = 0 # 重叠率为 0 
    else:
        Area = width*height # 两矩形相交面积
        Area1 = width1*height1
        Area2 = width2*height2
        ratio = Area*1./(Area1+Area2-Area)
    # return IOU
    return ratio,Reframe,GTframe

VOCpath = "Satellite"    
classes = ["airport", "bridge", "harbor"]
myIOU = 0.7
def calcu_F1():
    with open(path,'r') as f:
        TP = 0
        FP = 0
        TN = 0
        FN = 0


        for lines in f.readlines():
            line_arr = lines.split(',')
            imgname = line_arr[0]
            preclass = line_arr[1]
            prebox = line_arr[0].split(' ')   
            prexy = [int(prebox[0]),int(prebox[1]),int(prebox[2])+int(prebox[0]),int(prebox[3])+int(prebox[1])]  

            in_file = open(VOCpath+'/Annotations/%s.xml'%(imgname[:-4]))
            tree=ET.parse(in_file)
            root = tree.getroot()
            for obj in root.iter('object'):
                difficult = obj.find('difficult').text
                cls = obj.find('name').text
                if cls not in classes or int(difficult)==1:
                    continue
                if cls != preclass:
                    continue

                xmlbox = obj.find('bndbox')
                b = [int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text)]

                if calcu_IOU(b,prexy) > myIOU:
                    TP += 1
                else:
                    FP += 1

        xml_names = sorted(os.listdir(VOCpath+'/Annotations/'))
        Tcnt = 0
        for i in xml_names:
            if i[:-3] != 'xml':continue
            in_file = open(VOCpath+'/Annotations/'+i)
            tree=ET.parse(in_file)
            root = tree.getroot()
            Tcnt += len(root.findall('object'))

        FN = Tcnt - TP
        scoreR = TP/(TP+FN)
        scoreP = TP/(TP+FP)
        scoreF1 = 2.0*scoreP*scoreR/(scoreR+scoreP)
        print(scoreF1)
        return 


if __name__ == '__main__':
    path = 'SSD84271result.txt'
    calcu_F1(path)
    
            