from pylab import *
from numpy import *
from PIL import Image

from PCV.geometry import homography, warp
from PCV.localdescriptors import sift

# 将匹配转换成齐次坐标点的函数
def convert_points(j):
    ndx = matches[j].nonzero()[0]
    fp = homography.make_homog(l[j + 1][ndx, :2].T)
    ndx2 = [int(matches[j][i]) for i in ndx]
    tp = homography.make_homog(l[j][ndx2, :2].T)

    fp = vstack([fp[1], fp[0], fp[2]])
    tp = vstack([tp[1], tp[0], tp[2]])
    return fp, tp

if __name__=='__main__':

    featname = ['dir\\test\\' + "113.849293 _30.264511 _" + str(i) + '_0.sift' for i in [0, 90, 180, 270]]
    imname = ['dir\\test\\' + "113.849293 _30.264511 _" + str(i) + '_0.png' for i in [0, 90, 180, 270]]
    im = [array(Image.open(imname[i]).convert('L')) for i in range(4)]
    l = {}
    d = {}
    for i in range(4):
        sift.process_image(imname[i], featname[i])
        l[i], d[i] = sift.read_features_from_file(featname[i])

    matches = {}
    for i in range(4):
        matches[i] = sift.match(d[i + 1], d[i])
    model = homography.RansacModel()
    fp, tp = convert_points(1)
    H_12 = homography.H_from_ransac(fp, tp, model)[0]  
    fp, tp = convert_points(0)
    H_01 = homography.H_from_ransac(fp, tp, model)[0]  
    tp, fp = convert_points(2) 
    H_32 = homography.H_from_ransac(fp, tp, model)[0]  

    tp, fp = convert_points(3) 
    H_43 = homography.H_from_ransac(fp, tp, model)[0]  
    delta = 1000  
    im1 = array(Image.open(imname[1]), "uint8")
    im2 = array(Image.open(imname[2]), "uint8")
    im_12 = warp.panorama(H_12,im1,im2,delta,delta)

    im1 = array(Image.open(imname[0]), "f")
    im_02 = warp.panorama(dot(H_12,H_01),im1,im_12,delta,delta)

    im1 = array(Image.open(imname[3]), "f")
    im_32 = warp.panorama(H_32,im1,im_02,delta,delta)

    im1 = array(Image.open(imname[4]), "f")
    im_42 = warp.panorama(dot(H_32,H_43),im1,im_32,delta,2*delta)

    figure()
    imshow(array(im_42, "uint8"))
    axis('off')
    show()
