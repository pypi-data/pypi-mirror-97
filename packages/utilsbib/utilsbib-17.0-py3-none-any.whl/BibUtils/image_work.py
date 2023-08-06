from __future__ import division
from imutils import face_utils
import imutils
import numpy as np
import collections
import dlib
import cv2
import skimage.draw
import scipy as sp
import scipy.spatial
from PIL import Image
import os
from math import sqrt, ceil, floor
from PIL import Image
import json
import statistics
import cv2
import numpy as np
from numpy.linalg import eig, inv
from scipy.interpolate import interp1d, splprep, splev
from scipy.interpolate import InterpolatedUnivariateSpline
from pylab import *
from skimage import color
from scipy import misc
import time
import PIL

import numpy as np
import cv2
import colour

import dlib
import cv2
from imutils import face_utils
import numpy as np
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
from PIL import Image
from collections import defaultdict
from scipy.spatial import distance
from BibUtils import image_work
import skimage.draw
import scipy as sp


class makeup(object):
    """
    Class that handles application of color, and performs blending on image.
    Functions available for use:
        1. apply_lipstick: Applies lipstick on passed image of face.
        2. apply_liner: Applies black eyeliner on passed image of face.
        3. apply_blush: Applies blush on passed image of face.
        4. apply_eyebrow: Applies eyebrow on passed image of face.
        5. apply_foundation: Apply foundation passed image of face.
    """

    def __init__(self, img):
        """ Initiator method for class """
        self.red_l = 0
        self.green_l = 0
        self.blue_l = 0
        self.red_b = 0
        self.green_b = 0
        self.blue_b = 0
        self.image = img
        self.height, self.width = self.image.shape[:2]
        self.im_copy = self.image.copy()

        self.intensity = 0.8

        self.x = []
        self.y = []
        self.xleft = []
        self.yleft = []
        self.xright = []
        self.yright = []

    def __draw_curve(self, points, kind):
        """
        Draws a curve alone the given points by creating an interpolated path.
        """
        curvex = []
        curvey = []
        x_pts = list(np.asarray(points)[:, 0])
        y_pts = list(np.asarray(points)[:, 1])

        # Create the interpolated curve according to the x and y points.
        curve = interp1d(x_pts, y_pts, 'cubic')

        # Upper and lower curve are different in the order of points.
        if kind == 'upper':
            for i in np.arange(x_pts[0], x_pts[len(x_pts) - 1] + 1, 1):
                curvex.append(i)
                curvey.append(int(curve(i)))
        else:
            for i in np.arange(x_pts[len(x_pts) - 1] + 1, x_pts[0], 1):
                curvex.append(i)
                curvey.append(int(curve(i)))
        return curvex, curvey

    def __fill_lip_solid(self, outer, inner):
        """
        Fills solid colour inside two outlines.
        """
        outer_curve = zip(outer[0], outer[1])
        inner_curve = zip(inner[0], inner[1])
        points = []
        for point in outer_curve:
            points.append(np.array(point, dtype=np.int32))
        for point in inner_curve:
            points.append(np.array(point, dtype=np.int32))
        points = np.array(points, dtype=np.int32)
        cv2.fillPoly(self.image, [points],
                     (self.red_l, self.green_l, self.blue_l))

        # Smoothen the color.
        img_base = np.zeros((self.height, self.width))
        cv2.fillPoly(img_base, [points], 1)
        img_mask = cv2.GaussianBlur(img_base, (51, 51), 0)
        img_blur_3d = np.ndarray([self.height, self.width, 3], dtype='float')
        img_blur_3d[:, :, 0] = img_mask
        img_blur_3d[:, :, 1] = img_mask
        img_blur_3d[:, :, 2] = img_mask
        self.im_copy = (img_blur_3d * self.image +
                        (1 - img_blur_3d) * self.im_copy).astype('uint8')
        return

    def __draw_liner(self, eye, kind):
        """
        Draws eyeliner.
        """
        eye_x = []
        eye_y = []
        x_points = []
        y_points = []
        for point in eye:
            x_points.append(int(point.split()[0]))
            y_points.append(int(point.split()[1]))
        curve = interp1d(x_points, y_points, 'quadratic')
        for point in np.arange(x_points[0], x_points[len(x_points) - 1] + 1, 1):
            eye_x.append(point)
            eye_y.append(int(curve(point)))
        if kind == 'left':
            y_points[0] -= 1
            y_points[1] -= 1
            y_points[2] -= 1
            x_points[0] -= 5
            x_points[1] -= 1
            x_points[2] -= 1
            curve = interp1d(x_points, y_points, 'quadratic')
            count = 0
            for point in np.arange(x_points[len(x_points) - 1], x_points[0], -1):
                count += 1
                eye_x.append(point)
                if count < (len(x_points) / 2):
                    eye_y.append(int(curve(point)))
                elif count < (2 * len(x_points) / 3):
                    eye_y.append(int(curve(point)) - 1)
                elif count < (4 * len(x_points) / 5):
                    eye_y.append(int(curve(point)) - 2)
                else:
                    eye_y.append(int(curve(point)) - 3)
        elif kind == 'right':
            x_points[3] += 5
            x_points[2] += 1
            x_points[1] += 1
            y_points[3] -= 1
            y_points[2] -= 1
            y_points[1] -= 1
            curve = interp1d(x_points, y_points, 'quadratic')
            count = 0
            for point in np.arange(x_points[len(x_points) - 1], x_points[0], -1):
                count += 1
                eye_x.append(point)
                if count < (len(x_points) / 2):
                    eye_y.append(int(curve(point)))
                elif count < (2 * len(x_points) / 3):
                    eye_y.append(int(curve(point)) - 1)
                elif count < (4 * len(x_points) / 5):
                    eye_y.append(int(curve(point)) - 2)
                elif count:
                    eye_y.append(int(curve(point)) - 3)
        curve = zip(eye_x, eye_y)
        points = np.asarray(curve)
        cv2.fillPoly(self.im_copy, [points], 0)
        return

    def __get_points_lips(self, lips_points):
        """
        Get the points for the lips.
        """
        uol = []
        uil = []
        lol = []
        lil = []
        for i in range(0, 14, 2):
            uol.append([int(lips_points[i]), int(lips_points[i + 1])])
        for i in range(12, 24, 2):
            lol.append([int(lips_points[i]), int(lips_points[i + 1])])
        lol.append([int(lips_points[0]), int(lips_points[1])])
        for i in range(24, 34, 2):
            uil.append([int(lips_points[i]), int(lips_points[i + 1])])
        for i in range(32, 40, 2):
            lil.append([int(lips_points[i]), int(lips_points[i + 1])])
        lil.append([int(lips_points[24]), int(lips_points[25])])
        return uol, uil, lol, lil

    def __get_curves_lips(self, uol, uil, lol, lil):
        """
        Get the outlines of the lips.
        """
        uol_curve = self.__draw_curve(uol, 'upper')
        uil_curve = self.__draw_curve(uil, 'upper')
        lol_curve = self.__draw_curve(lol, 'lower')
        lil_curve = self.__draw_curve(lil, 'lower')
        return uol_curve, uil_curve, lol_curve, lil_curve

    def __fill_color(self, uol_c, uil_c, lol_c, lil_c):
        """
        Fill colour in lips.
        """
        self.__fill_lip_solid(uol_c, uil_c)
        self.__fill_lip_solid(lol_c, lil_c)
        return

    def __create_eye_liner(self, eyes_points):
        """
        Apply eyeliner.
        """
        left_eye = eyes_points[0].split('\n')
        right_eye = eyes_points[1].split('\n')
        right_eye = right_eye[0:4]
        self.__draw_liner(left_eye, 'left')
        self.__draw_liner(right_eye, 'right')
        return

    def __fitEllipse(self, x, y):
        """
        Given points of x and y, find out the most appropriate Ellipse
        """
        x = x[:, np.newaxis]
        y = y[:, np.newaxis]
        D = np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
        S = np.dot(D.T, D)
        C = np.zeros([6, 6])
        C[0, 2], C[2, 0], C[1, 1] = 2, 2, -1
        E, V = eig(np.dot(inv(S), C))
        n = np.argmax(np.abs(E))
        a = V[:, n]
        return a

    def __ellipse_center(self, a):
        """
        Find out the center of ellipse.
        """
        b, c, d, f, a = a[1]/2, a[2], a[3]/2, a[4]/2, a[0]
        num = b*b - a*c
        x0 = (c*d - b*f) / num
        y0 = (a*f - b*d) / num
        return np.array([x0, y0])

    def __ellipse_angle_of_rotation(self, a):
        """
        Find out how many angle should the ellipse rotate.
        """
        b, c, a = a[1]/2, a[2], a[0]
        return 0.5 * np.arctan(2*b / (a-c))

    def __ellipse_axis_length(self, a):
        """
        Find out the length of two axes.
        """
        b, c, d, f, g, a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
        up = 2 * (a*f*f + c*d*d + g*b*b - 2*b*d*f - a*c*g)
        down1 = (b*b - a*c) * \
            ((c-a) * np.sqrt(1 + 4*b*b/((a-c)*(a-c))) - (c+a))
        down2 = (b*b - a*c) * \
            ((a-c) * np.sqrt(1 + 4*b*b/((a-c)*(a-c))) - (c+a))
        res1 = np.sqrt(up / down1)
        res2 = np.sqrt(up / down2)
        return np.array([res1, res2])

    def __getEllipse(self, x, y):
        """
        Find out the most appropriate ellipse.
        """
        a = self.__fitEllipse(x, y)
        center = self.__ellipse_center(a)
        phi = self.__ellipse_angle_of_rotation(a)
        axes = self.__ellipse_axis_length(a)
        return (center[0], center[1]), (axes[0], axes[1]/1.3), phi

    def __univariate_plot(self, lx=[], ly=[]):
        """
        Interpolate with univariate spline.
        """
        unew = np.arange(lx[0], lx[-1]+1, 1)
        f2 = InterpolatedUnivariateSpline(lx, ly)
        return unew, f2(unew)

    def __inter_plot(self, lx=[], ly=[], k1='quadratic'):
        """
        Interpolate with interp1d.
        """
        unew = np.arange(lx[0], lx[-1]+1, 1)
        f2 = interp1d(lx, ly, kind=k1)
        return unew, f2(unew)

    def __getBoundaryPoints(self, x, y):
        """
        Given x and y, find out the boundary.
        """
        tck, u = splprep([x, y], s=0, per=1)
        unew = np.linspace(u.min(), u.max(), 10000)
        xnew, ynew = splev(unew, tck, der=0)
        tup = c_[xnew.astype(int), ynew.astype(int)].tolist()
        coord = list(set(tuple(map(tuple, tup))))
        coord = np.array([list(elem) for elem in coord])
        return coord[:, 0], coord[:, 1]

    def __getInteriorPoints(self, x, y):
        """
        Find out all points needed for interpolation.
        """
        intx = []
        inty = []

        def ext(a, b, i):
            a, b = int(a), int(b)
            intx.extend(np.arange(a, b, 1).tolist())
            temp = np.ones(b-a)*i
            inty.extend(temp.astype(int).tolist())
        x, y = np.array(x), np.array(y)
        xmin, xmax = amin(x), amax(x)
        xrang = np.arange(xmin, xmax+1, 1)
        for i in xrang:
            ylist = y[where(x == i)]
            ext(amin(ylist), amax(ylist), i)
        return intx, inty

    def __get_boundary_points(self, landmarks, flag):
        """
        Find out the boundary of blush.
        """
        if flag == 0:
            # Right Cheek
            r = (landmarks[15, 0] - landmarks[35, 0]) / 3.5
            center = (landmarks[15] + landmarks[35]) / 2.0
        elif flag == 1:
            # Left Cheek
            r = (landmarks[1, 0] - landmarks[31, 0]) / 3.5
            center = (landmarks[1] + landmarks[31]) / 2.0

        points_1 = [center[0] - r, center[1]]
        points_2 = [center[0], center[1] - r]
        points_3 = [center[0] + r, center[1]]
        points_4 = [center[0], center[1] + r]
        points_5 = points_1

        points = np.array([points_1, points_2, points_3, points_4, points_5])

        x, y = points[0:5, 0], points[0:5, 1]

        tck, u = splprep([x, y], s=0, per=1)
        unew = np.linspace(u.min(), u.max(), 1000)
        xnew, ynew = splev(unew, tck, der=0)
        tup = c_[xnew.astype(int), ynew.astype(int)].tolist()
        coord = list(set(tuple(map(tuple, tup))))
        coord = np.array([list(elem) for elem in coord])
        return np.array(coord[:, 0], dtype=np.int32), np.array(coord[:, 1], dtype=np.int32)

    def __blush(self, x_right, y_right, x_left, y_left):

        intensity = 0.3
        # Create blush shape
        mask = np.zeros((self.height, self.width))
        cv2.fillConvexPoly(mask, np.array(
            c_[x_right, y_right], dtype='int32'), 1)
        cv2.fillConvexPoly(mask, np.array(
            c_[x_left, y_left], dtype='int32'), 1)
        mask = cv2.GaussianBlur(mask, (51, 51), 0) * intensity

        # Add blush color to image
        # val = color.rgb2lab((self.im_copy / 255.))
        val = cv2.cvtColor(self.im_copy, cv2.COLOR_RGB2LAB).astype(float)
        val[:, :, 0] = val[:, :, 0] / 255. * 100.
        val[:, :, 1] = val[:, :, 1] - 128.
        val[:, :, 2] = val[:, :, 2] - 128.
        LAB = color.rgb2lab(np.array((self.red_b / 255., self.green_b /
                                      255., self.blue_b / 255.)).reshape(1, 1, 3)).reshape(3,)

        mean_val = np.mean(np.mean(val, axis=0), axis=0)
        mask = np.array([mask, mask, mask])
        mask = np.transpose(mask, (1, 2, 0))
        lab = np.multiply((LAB - mean_val), mask)

        val[:, :, 0] = np.clip(val[:, :, 0] + lab[:, :, 0], 0, 100)
        val[:, :, 1] = np.clip(val[:, :, 1] + lab[:, :, 1], -127, 128)
        val[:, :, 2] = np.clip(val[:, :, 2] + lab[:, :, 2], -127, 128)

        self.im_copy = (color.lab2rgb(val) * 255).astype(np.uint8)
        # val[:, :, 0] = (np.clip(val[:, :, 0] + lab[:,:,0], 0, 100) / 100 * 255).astype(np.uint8)
        # val[:, :, 1] = (np.clip(val[:, :, 1] + lab[:,:,1], -127, 128) + 127).astype(np.uint8)
        # val[:, :, 2] = (np.clip(val[:, :, 2] + lab[:,:,2], -127, 128) + 127).astype(np.uint8)

        # self.im_copy = cv2.cvtColor(val, cv2.COLOR_LAB2RGB)

    def __get_lips(self, landmarks, flag=None):
        """
        Find out the landmarks corresponding to lips.
        """
        if landmarks is None:
            return None
        lips = ""
        for point in landmarks[48:]:
            lips += str(point).replace('[', '').replace(']', '') + '\n'
        return lips

    def __get_upper_eyelids(self, landmarks, flag=None):
        """
        Find out landmarks corresponding to upper eyes.
        """
        if landmarks is None:
            return None
        liner = ""
        for point in landmarks[36:40]:
            liner += str(point).replace('[', '').replace(']', '') + '\n'
        liner += '\n'
        for point in landmarks[42:46]:
            liner += str(point).replace('[', '').replace(']', '') + '\n'
        return liner

    def apply_lipstick2(self, landmarks, m_color):
        img = self.im_copy
        outline = landmarks[[
            x + 48 for x in range(12)]+[48]+[x + 60 for x in range(8)]]
        xlipspoints = [x[0] for x in outline]
        ylipspoints = [x[1] for x in outline]
        print("xlipspoints", xlipspoints)
        print("ylipspoints", ylipspoints)
        print("length of xlipspoints", len(xlipspoints))
        print("length of ylipspoints", len(ylipspoints))
        maxx = max(xlipspoints)
        minx = min(xlipspoints)
        maxy = max(ylipspoints)
        miny = min(ylipspoints)
        lips_points = []
        for pointx, pointy in zip(xlipspoints, ylipspoints):
            lips_points.append([pointx, pointy])
        image = img.copy()
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        contours = [np.array(lips_points, dtype=np.int32)]
        cv2.fillPoly(image, pts=contours, color=m_color)
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        overlay = image
        output = img
        alpha = 0.5
        return cv2.addWeighted(overlay, 1 - alpha, output, 1 - alpha, 0, output)

    def apply_lipstick(self, landmarks, rlips, glips, blips):
        """
        Applies lipstick on an input image.
        ___________________________________
        Inputs:
            1. Landmarks of the face.
            2. Colors of lipstick in the order of r, g, b.
        Output:
            1. The face applied with lipstick.
        """

        self.red_l = rlips
        self.green_l = glips
        self.blue_l = blips
        lips = self.__get_lips(landmarks)
        lips = list([point.split() for point in lips.split('\n')])
        lips_points = [item for sublist in lips for item in sublist]
        uol, uil, lol, lil = self.__get_points_lips(lips_points)
        uol_c, uil_c, lol_c, lil_c = self.__get_curves_lips(uol, uil, lol, lil)
        self.__fill_color(uol_c, uil_c, lol_c, lil_c)
        return self.im_copy

    def apply_liner(self, landmarks):
        """
        Applies black liner on the input image.
        ___________________________________
        Input:
            1. Landmarks of the face.
        Output:
            1. The face applied with eyeliner.
        """
        liner = self.__get_upper_eyelids(landmarks)
        eyes_points = liner.split('\n\n')
        self.__create_eye_liner(eyes_points)
        return self.im_copy

    def apply_foundation(self, landmarks,red,green,blue):
        """
        Applies foundation on the input image.
        ___________________________________
        Input:
            1. Landmarks of the face.
        Output:
            1. The face applied with foundation.
        """

        # R, G, B = (200., 121., 46.)
        R, G, B = (red, green, blue)
        inten = 0.6

        # Get points of face.
        fileface = landmarks[0:17]
        pointsface = np.floor(fileface)
        point_face_x = np.array((pointsface[:][:, 0]))
        point_face_y = np.array(pointsface[:][:, 1])

        # Get points of lips.
        file = landmarks[48:68]
        points = np.floor(file)
        point_out_x = np.array((points[:int(len(points)/2)][:, 0]))
        point_out_y = np.array(points[:int(len(points)/2)][:, 1])

        # Get points of eyes.
        fileeye = landmarks[36:48]
        pointseye = np.floor(fileeye)
        eye_point_down_x = np.array(pointseye[:4][:, 0])
        eye_point_down_y = np.array(pointseye[:4][:, 1])
        eye_point_up_x = (pointseye[3:6][:, 0]).tolist()
        eye_point_up_y = (pointseye[3:6][:, 1]).tolist()
        eye_point_up_x.append(pointseye[0, 0])
        eye_point_up_y.append(pointseye[0, 1])
        eye_point_up_x = np.array(eye_point_up_x)
        eye_point_up_y = np.array(eye_point_up_y)
        eye_point_down_x_right = np.array(pointseye[6:10][:, 0])
        eye_point_down_y_right = np.array(pointseye[6:10][:, 1])
        eye_point_up_x_right = (pointseye[9:12][:, 0]).tolist()
        eye_point_up_y_right = (pointseye[9:12][:, 1]).tolist()
        eye_point_up_x_right.append(pointseye[6, 0])
        eye_point_up_y_right.append(pointseye[6, 1])
        eye_point_up_x_right = np.array(eye_point_up_x_right)
        eye_point_up_y_right = np.array(eye_point_up_y_right)

        x_face = []
        y_face = []
        x_aux = []
        y_aux = []

        # Get lower face from landmarks.
        lower_face = self.__univariate_plot(point_face_x[:], point_face_y[:])
        x_face.extend(lower_face[0][::-1])
        y_face.extend(lower_face[1][::-1])

        # Get upper face from approximation.
        (centerx, centery), (axesx, axesy), angel = self.__getEllipse(
            point_face_x, point_face_y)
        centerpt = (int(centerx), int(centery))
        axeslen = (int(axesx), int(axesy*1.2))
        ellippoints = np.floor(cv2.ellipse2Poly(
            centerpt, axeslen, int(angel), 180, 360, 1))
        ellipx = ellippoints[:, 0].tolist()
        ellipy = ellippoints[:, 1].tolist()
        x_face.extend(ellipx)
        y_face.extend(ellipy)
        x_face.append(x_face[0])
        y_face.append(y_face[0])
        x_face, y_face = self.__getBoundaryPoints(x_face, y_face)
        x, y = self.__getInteriorPoints(x_face, y_face)

        # Remove lips from face mask.
        l_u_l = self.__inter_plot(point_out_x[:4], point_out_y[:4])
        l_u_r = self.__inter_plot(point_out_x[3:7], point_out_y[3:7])
        l_l = self.__inter_plot([point_out_x[0]]+point_out_x[6:][::-1].tolist(), [
                                point_out_y[0]]+point_out_y[6:][::-1].tolist(), 'cubic')
        lipinteriorx, lipinteriory = self.__getInteriorPoints(l_u_l[0].tolist(
        ) + l_u_r[0].tolist() + l_l[0].tolist(), l_u_l[1].tolist() + l_u_r[1].tolist() + l_l[1].tolist())
        x_aux.extend(lipinteriorx)
        y_aux.extend(lipinteriory)

        # Remove eyes from face mask.
        e_l_l = self.__inter_plot(
            eye_point_down_x[:], eye_point_down_y[:], 'cubic')
        e_u_l = self.__inter_plot(
            eye_point_up_x[:], eye_point_up_y[:], 'cubic')
        lefteyex, lefteyey = self.__getInteriorPoints(
            e_l_l[0].tolist() + e_u_l[0].tolist(), e_l_l[1].tolist() + e_u_l[1].tolist())
        x_aux.extend(lefteyex)
        y_aux.extend(lefteyey)
        e_l_r = self.__inter_plot(
            eye_point_down_x_right[:], eye_point_down_y_right[:], 'cubic')
        e_u_r = self.__inter_plot(
            eye_point_up_x_right[:], eye_point_up_y_right[:], 'cubic')
        righteyex, righteyey = self.__getInteriorPoints(
            e_l_r[0].tolist() + e_u_r[0].tolist(), e_l_r[1].tolist() + e_u_r[1].tolist())
        x_aux.extend(righteyex)
        y_aux.extend(righteyey)

        val = (color.rgb2lab((self.im_copy[x, y]/255.).reshape(len(x), 1, 3))
                    .reshape(len(x), 3))
        vallips = (color.rgb2lab((self.im_copy[x_aux, y_aux]/255.).reshape(len(x_aux), 1, 3))
                        .reshape(len(x_aux), 3))
        L = (sum(val[:, 0])-sum(vallips[:, 0])) / \
            (len(val[:, 0])-len(vallips[:, 0]))
        A = (sum(val[:, 1])-sum(vallips[:, 1])) / \
            (len(val[:, 1])-len(vallips[:, 1]))
        bB = (sum(val[:, 2])-sum(vallips[:, 2])) / \
            (len(val[:, 2])-len(vallips[:, 2]))

        L1, A1, B1 = color.rgb2lab(
            np.array((R/255., G/255., B/255.)).reshape(1, 1, 3)).reshape(3,)
        val[:, 0] += (L1-L) * inten
        val[:, 1] += (A1-A) * inten
        val[:, 2] += (B1-bB) * inten

        self.im_copy[x, y] = color.lab2rgb(
            val.reshape(len(x), 1, 3)).reshape(len(x), 3) * 255
        return self.im_copy

    def apply_blush(self, landmarks, R, G, B):
        """
        Applies blush on the input image.
        ___________________________________
        Input:
            1. Landmarks of the face.
            2. Color of blush in the order of r, g, b.
        Output:
            1. The face applied with blush.
        """

        # Find Blush Loacations
        x_right, y_right = self.__get_boundary_points(landmarks, 0)
        x_left, y_left = self.__get_boundary_points(landmarks, 1)

        # Apply Blush
        self.red_b = R
        self.green_b = G
        self.blue_b = B
        self.__blush(x_right, y_right, x_left, y_left)

        return self.im_copy

    def apply_eyebrow(self, landmark):
        """
        Applies eyebrow on the input image.
        ___________________________________
        Input:
            1. Landmarks of the face.
        Output:
            1. The face applied with eyebrow.
        """
        # right eyebrow
        pts1 = np.array(landmark[17:22], np.int32)

        # rescale
        right_eye = misc.imread('./data/right_eyebrow.png')
        scale = float(pts1[4][0] - pts1[0][0]) / right_eye.shape[1]
        right_eye = cv2.resize(right_eye, (0, 0), fx=scale, fy=scale)

        # find location
        x_offset = pts1[0][0]
        y_offset = pts1[0][1]
        y1, y2 = y_offset - right_eye.shape[0] + 5, y_offset + 5
        x1, x2 = x_offset, x_offset + right_eye.shape[1]

        alpha_s = right_eye[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        # apply eyebrow
        for c in range(0, 3):
            self.im_copy[y1:y2, x1:x2, c] = (alpha_s * right_eye[:, :, c] +
                                             alpha_l * self.im_copy[y1:y2, x1:x2, c])

        # left eyebrow
        pts2 = np.array(landmark[22:27], np.int32)

        # rescale
        left_eye = misc.imread('./data/left_eyebrow.png')
        scale = float(pts2[4][0] - pts2[0][0]) / left_eye.shape[1]
        left_eye = cv2.resize(left_eye, (0, 0), fx=scale, fy=scale)

        # find location
        x_offset = pts2[0][0]
        y_offset = pts2[0][1]
        y1, y2 = y_offset - left_eye.shape[0] + 5, y_offset + 5
        x1, x2 = x_offset, x_offset + left_eye.shape[1]

        alpha_s = left_eye[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        # apply eyebrow
        for c in range(0, 3):
            self.im_copy[y1:y2, x1:x2, c] = (alpha_s * left_eye[:, :, c] +
                                             alpha_l * self.im_copy[y1:y2, x1:x2, c])
        return self.im_copy

    def __inter(self, lx=[], ly=[], k1='quadratic'):
        unew = np.arange(lx[0], lx[-1]+1, 1)
        f2 = interp1d(lx, ly, kind=k1)
        return (f2, unew)

    def __ext(self, a, b, i):
        self.x.extend(arange(a, b, 1).tolist())
        if(b-a == 1):
            print("okok3 ", b-a)
            self.y.extend((ones(int(b-a))*i).tolist())
        else:
            print("okok4 ", b-a)
            self.y.extend((ones(int(b-a+1))*i).tolist())

    def __extleft(self, a, b, i):
        self.xleft.extend(arange(a, b, 1).tolist())
        if(b-a == 1):
            print("okok1 ", b-a)
            self.yleft.extend((ones(int(b-a))*i).tolist())
        else:
            print("okok2 ", b-a)
            self.yleft.extend((ones(int(b-a+1))*i).tolist())

    def __extright(self, a, b, i):
        self.xright.extend(arange(a, b, 1).tolist())
        if(b-a == 1):
            self.yright.extend((ones(int(b-a))*i).tolist())
        else:
            self.yright.extend((ones(int(b-a+1))*i).tolist())

    def apply_eyeshadow(self, landmarks_array, R, G, B):

        lower_left_end = 5
        upper_left_end = 11
        lower_right_end = 16
        upper_right_end = 22
        print("plouc1 ")
        eye_left = landmarks_array[36: 40, :]
        eye_left_end = np.array([landmarks_array[39, :]])
        eyebrow_left = landmarks_array[17: 22, :]
        eyebrow_left_start = np.array([landmarks_array[17, :]])
        print("plouc2")
        left = np.concatenate(
            (eyebrow_left_start, eye_left, eyebrow_left, eye_left_end), axis=0)
        if(left[9, 0] > left[10, 0]):
            left[9, 0] = left[10, 0] - 5
        print("plouc3")
        eye_right = landmarks_array[42: 46, :]
        eye_right_start = np.array([landmarks_array[42, :]])
        eyebrow_right = landmarks_array[22: 27, :]
        eyebrow_right_end = np.array([landmarks_array[26, :]])
        print("plouc4")
        right = np.concatenate(
            (eye_right, eyebrow_right_end, eye_right_start, eyebrow_right), axis=0)
        if(right[6, 0] < right[5, 0]):
            right[6, 0] = right[5, 0] + 5
        print("plouc5")
        points = np.concatenate((left, right), axis=0)

        point_down_x = np.array((points[:lower_left_end][:, 0]))
        point_down_y = np.array(points[:lower_left_end][:, 1])
        point_up_x = np.array(points[lower_left_end:upper_left_end][:, 0])
        point_up_y = np.array(points[lower_left_end:upper_left_end][:, 1])
        point_down_x_right = np.array(
            (points[upper_left_end:lower_right_end][:, 0]))
        point_down_y_right = np.array(
            points[upper_left_end:lower_right_end][:, 1])
        point_up_x_right = np.array(
            (points[lower_right_end:upper_right_end][:, 0]))
        point_up_y_right = np.array(
            points[lower_right_end:upper_right_end][:, 1])
        print("plouc6")
        point_down_y_max = max(point_down_y)
        point_up_y_min = min(point_up_y)
        offset_left = point_down_y_max - point_up_y_min
        print("plouc7")
        point_up_y[0] += offset_left * 0.3
        point_up_y[1] += offset_left * 0.3
        point_up_y[2] += offset_left * 0.15
        point_up_y[3] += offset_left * 0.1
        point_up_y[4] += offset_left * 0.3
        point_down_y[0] += offset_left * 0.3
        print("plouc8")
        point_down_y_right_max = max(point_down_y_right)
        point_up_y_right_min = min(point_up_y_right)
        offset_right = point_down_y_right_max - point_up_y_right_min
        print("plouc9")
        point_up_y_right[-1] += offset_right * 0.3
        point_up_y_right[1] += offset_right * 0.3
        point_up_y_right[2] += offset_right * 0.1
        point_up_y_right[3] += offset_right * 0.15
        point_up_y_right[4] += offset_right * 0.3
        point_down_y_right[-1] += offset_right * 0.3
        print("plouc10")
        im = self.im_copy
        im2 = im.copy()
        height, width = im.shape[:2]
        print("plouc11")
        # bound the convex poly
        l_l = self.__inter(point_down_x[:], point_down_y[:], 'cubic')
        u_l = self.__inter(point_up_x[:], point_up_y[:], 'cubic')
        l_r = self.__inter(
            point_down_x_right[:], point_down_y_right[:], 'cubic')
        u_r = self.__inter(point_up_x_right[:], point_up_y_right[:], 'cubic')
        print("plouc12")
        for i in range(int(l_l[1][0]), int(l_l[1][-1]+1)):
            self.__ext(u_l[0](i), l_l[0](i)+1, i)
            self.__extleft(u_l[0](i), l_l[0](i)+1, i)
        print("plouc13")
        for i in range(int(l_r[1][0]), int(l_r[1][-1]+1)):
            self.__ext(u_r[0](i), l_r[0](i)+1, i)
            self.__extright(u_r[0](i), l_r[0](i)+1, i)
        print("plouc14")
        self.x.append(0.1)
        print("pp2 ", len(self.x))
        
        print("pp3 ", len(self.y))
        #print("pp1 ",im[self.x, self.y]/255.)
        # add color to eyeshadow area
        val = color.rgb2lab(
            (im[list(map(int, self.x)), list(map(int, self.y))]/255.).reshape(len(self.x), 1, 3)).reshape(len(self.x), 3)
        L, A, bB = mean(val[:, 0]), mean(val[:, 1]), mean(val[:, 2])
        print("plouc15")
        rgbmean = (im[list(map(int, self.x)), list(map(int, self.y))])
        rmean, gmean, bmean = mean(rgbmean[:, 0]), mean(
            rgbmean[:, 1]), mean(rgbmean[:, 2])
        print("plouc16")
        L, A, bB = color.rgb2lab(
            np.array((rmean/255., gmean/255., bmean/255.)).reshape(1, 1, 3)).reshape(3,)
        L1, A1, B1 = color.rgb2lab(
            np.array((R/255., G/255., B/255.)).reshape(1, 1, 3)).reshape(3,)
        print("plouc17")
        # compare the difference between the original and goal color
        val[:, 0] += (L1-L) * self.intensity
        val[:, 1] += (A1-A) * self.intensity
        val[:, 2] += (B1-bB) * self.intensity
        print("plouc18")
        image_blank = np.zeros([height, width, 3])
        image_blank[list(map(int, self.x)), list(map(int, self.y))] = color.lab2rgb(
            val.reshape(len(self.x), 1, 3)).reshape(len(self.x), 3)*255
        print("plouc19")
        original = color.rgb2lab(
            (im[list(map(int, self.x)), list(map(int, self.y))]*0/255.).reshape(len(self.x), 1, 3)).reshape(len(self.x), 3)
        tobeadded = color.rgb2lab(
            (image_blank[list(map(int, self.x)), list(map(int, self.y))]/255.).reshape(len(self.x), 1, 3)).reshape(len(self.x), 3)
        original += tobeadded
        im[list(map(int, self.x)), list(map(int, self.y))] = color.lab2rgb(original.reshape(
            len(self.x), 1, 3)).reshape(len(self.x), 3)*255
        print("plouc20")
        print("plouc201 ",len(self.yleft))
        self.xleft.append(0.0)
        print("plouc202 ",len(self.xleft))
        print("plouc203 ",len(self.yright))
        print("plouc204 ",len(self.xright))
        # Blur Filter
        filter = np.zeros((height, width))
        cv2.fillConvexPoly(filter, np.array(
            c_[self.yleft, self.xleft], dtype='int32'), 1)
        cv2.fillConvexPoly(filter, np.array(
            c_[self.yright, self.xright], dtype='int32'), 1)
        filter = cv2.GaussianBlur(filter, (31, 31), 0)
        print("plouc21")
        # Erosion to reduce blur size
        kernel = np.ones((12, 12), np.uint8)
        filter = cv2.erode(filter, kernel, iterations=1)
        alpha = np.zeros([height, width, 3], dtype='float64')
        alpha[:, :, 0], alpha[:, :, 1], alpha[:, :, 2] = filter, filter, filter
        print("plouc22")
        return (alpha * im + (1 - alpha) * im2).astype('uint8')
        # return (alpha * im + (1 - alpha) * im2)
        # imshow((alpha * im + (1 - alpha) * im2).astype('uint8'))

    def apply_makeup(self, landmarks):
        self.im_copy = self.apply_lipstick(landmarks, 170, 10, 30)
        # self.im_copy = self.apply_foundation(landmarks)
        self.im_copy = self.apply_blush(landmarks, 223., 91., 111.)
        #self.im_copy = self.apply_eyebrow(landmarks)
        #self.im_copy = self.apply_liner(landmarks)
        self.im_copy = self.apply_eyeshadow(landmarks, 102, 0, 51)
        return self.im_copy

    def apply_makeup_all(self, landmarks):
        self.im_copy = self.apply_lipstick(landmarks, 170, 10, 30)
        self.im_copy = self.apply_foundation(landmarks)
        self.im_copy = self.apply_blush(landmarks, 223., 91., 111.)
        self.im_copy = self.apply_eyebrow(landmarks)
        self.im_copy = self.apply_liner(landmarks)
        self.im_copy = self.apply_eyeshadow(landmarks, 102, 0, 51)
        return self.im_copy


def add_makeup_PIL(file, face_cropper, m_type=0, col=None):
    original_PIL = PIL.Image.open(file).convert('RGB')
    original_open_cv_image = cv2.imread(file)
    # Convert RGB to BGR
    #original_open_cv_image = original_open_cv_image[:, :, ::-1].copy()
    # Convert back
    #original_open_cv_image = cv2.cvtColor(original_open_cv_image, cv2.COLOR_BGR2RGB)

    rect = face_cropper.detector(original_open_cv_image)[0]
    sp = face_cropper.predictor(original_open_cv_image, rect)
    landmarks = np.array([[p.x, p.y] for p in sp.parts()])
    makeup_saloon = makeup(original_open_cv_image)
    if m_type == 0:  # lipstick
        img = PIL.Image.fromarray(
            np.uint8(makeup_saloon.apply_lipstick2(landmarks, [col[0], col[1], col[2]])))
    if m_type == 1:  # blush
        img = PIL.Image.fromarray(
            np.uint8(makeup_saloon.apply_blush(landmarks, col[0], col[1], col[2])))
    if m_type == 2:  # eye shadow
        print("ziak 1")
        img = PIL.Image.fromarray(
            np.uint8(makeup_saloon.apply_eyeshadow(landmarks, col[0], col[1], col[2])))
        print("ziak 2")
    img_cv = np.array(img)
    img_cv = img_cv[:, :, ::-1].copy()
    result_rgb = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
    return original_PIL, PIL.Image.fromarray(result_rgb)


class Tile(object):
    """Represents a single tile."""

    def __init__(self, image, number, position, coords, filename=None):
        self.image = image
        self.number = number
        self.position = position
        self.coords = coords
        self.filename = filename

    @property
    def row(self):
        return self.position[0]

    @property
    def column(self):
        return self.position[1]

    def generate_filename(
        self, directory=os.getcwd(), prefix="tile", format="png", path=True
    ):
        """Construct and return a filename for this tile."""
        filename = prefix + "_{col:02d}_{row:02d}.{ext}".format(
            col=self.column, row=self.row, ext=format.lower().replace("jpeg", "jpg")
        )
        if not path:
            return filename
        return os.path.join(directory, filename)

    def save(self, filename=None, format="png"):
        if not filename:
            filename = self.generate_filename(format=format)
        self.image.save(filename, format)
        self.filename = filename

    def __repr__(self):
        """Show tile number, and if saved to disk, filename."""
        if self.filename:
            return "<Tile #{} - {}>".format(
                self.number, os.path.basename(self.filename)
            )
        return "<Tile #{}>".format(self.number)


class Face_cropper:
    def __init__(self, dlib_descriptor_filepath):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(dlib_descriptor_filepath)

    def get_under_mouth_color(self,filename,nb_color = 1, pre_img =None):
        if pre_img is None:
            lips = self.crop_out_skin_under_mouth(filename,isolate_area=True)
        else:
            lips = pre_img
        colors = image_work.get_automatic_cluster_color(np.asarray(lips),nb_color)
        flatten_labels = [x[0] for x in colors[2]]
        labels_size = len(flatten_labels)
        chosen = []
        proportion_best = 0
        for i in range(len(colors[0])):
            c = colors[0][i]
            if c[0][0] > 10 and c[0][1] > 10 and c[0][2] > 10:
                candidate = [float(c[0][0]),float(c[0][1]),float(c[0][2])]
                proportion = flatten_labels.count(i)/labels_size
                print("Candidate : ",candidate, proportion)
                chosen.append([candidate, proportion,])
                #if proportion > proportion_best:
                #    chosen = candidate
                #    proportion_best = proportion
                    #return [float(i[0][0]),float(i[0][1]),float(i[0][2])]
        print("chosen : ",chosen, proportion_best)
        
        if len(chosen) < 2:
            print("only :", chosen[0])
            return [chosen[0][0],chosen[0][1]]
        
        res = []
        for i in chosen:
            somme = []
            for j in chosen:
                dist = distance.euclidean(image_work.rgb2lab(i[0]),image_work.rgb2lab(j[0]))
                if dist > 0:
                    somme.append(dist)
                    #print(i,dist)
            if len(somme) > 1:
                #print(i, statistics.stdev(somme), statistics.mean(somme))
                res.append([i[0],i[1] , statistics.stdev(somme), statistics.mean(somme)])
            else :
                #print(i, somme[0], somme[0])
                res.append([i[0],i[1] ,somme[0], somme[0]])
        if len(res) == 2:
            res = sorted(res, key=lambda x: x[1])
            print("only 2 candidates", res)
            print("chosen : ",res[-1])
            return [res[-1][0],res[-1][1] * default]
        else:
            res = sorted(res, key=lambda x: x[2]) 
            print("more than 2 candidates", res)
            print("chosen : ",res[0])
            return [res[0][0],res[0][-2]]
        
        return [res[-1][0],res[-1][-2]]
        
        return chosen

    def crop_out_skin_under_mouth(self, filename, isolate_area = False, pre_img=None, pad =40):
        if not(pre_img is None):
            img = pre_img
        else:
            img = cv2.imread(filename)
        try:
            rect = self.detector(img)[0]
            sp = self.predictor(img, rect)
            landmarks = np.array([[p.x, p.y] for p in sp.parts()])
            outline = landmarks[[8,10,58]]
            Y, X = skimage.draw.polygon(outline[:, 1], outline[:, 0])
            cropped_img = np.zeros(img.shape, dtype=np.uint8)
            cropped_img[Y, X] = img[Y, X]

            shape = sp
            if isolate_area:
                xmouthpoints = [shape.part(x).x for x in [8,10,58]]
                ymouthpoints = [shape.part(x).y for x in [8,10,58]]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)
                pos_origin = [[minx, miny], [maxx, maxy]]

                #pad = 40
                #crop_image = img.copy()
                cropped_img = cropped_img[miny + pad:maxy-pad, minx+pad:maxx-pad]

            result_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
            return Image.fromarray(result_rgb)
        except IndexError:
            return False

    def can_I_check(self, fname):
        mouth_color = self.get_under_mouth_color(fname, nb_color=1,pre_img=None)[0]

        lips_color = self.get_lipstick_color(fname,nb_color = 1)
        dist = distance.euclidean(image_work.rgb2lab(mouth_color),image_work.rgb2lab(lips_color))
        print(dist)
        return dist > 30


    def generate_json_result(self,checks, is_inside, filename = "data.json"):
        rate_up_left = checks[0][1]
        rate_up_center = checks[1][1]
        rate_up_right = checks[2][1]
        
        #rate_middle_left = checks[3][1]
        #rate_middle_center = checks[4][1]
        #rate_middle_right = checks[5][1]
        
        rate_bottom_left = checks[3][1]
        rate_bottom_center = checks[4][1]
        rate_bottom_right = checks[5][1]
        
        if not(is_inside):
            # rate_up_left score
            rate = rate_up_left
            up_left_score = 0 if rate < 0.01 else 1 if rate < 0.07 else 2

            #rate_up_center score
            rate = rate_up_center
            up_center_score = 0 if rate < 0.01 else 1 if rate < 0.07 else 2

            #rate_up_right score
            rate = rate_up_right
            up_right_score = 0 if rate < 0.01 else 1 if rate < 0.07 else 2
            #rate_middle_left score
            #rate = rate_middle_left
            #middle_left_score = 0 if rate < 0.01 else 1 if rate < 0.02 else 2 if rate < 0.04 else 3 if rate < 0.05 else 4 if rate < 0.07 else 5

            #rate_middle_center score
            #rate = rate_middle_center
            #middle_center_score = 0 if rate < 0.01 else 1 if rate < 0.02 else 2 if rate < 0.04 else 3 if rate < 0.05 else 4 if rate < 0.07 else 5

            #rate_middle_right score
            #rate = rate_middle_right
            #middle_right_score = 0 if rate < 0.01 else 1 if rate < 0.02 else 2 if rate < 0.04 else 3 if rate < 0.05 else 4 if rate < 0.07 else 5

            #rate_bottom_left score
            rate = rate_bottom_left
            bottom_left_score = 0 if rate < 0.01 else 1 if rate < 0.07 else 2

            #rate_bottom_center score
            rate = rate_bottom_center
            bottom_center_score = 0 if rate < 0.01 else 1 if rate < 0.07 else 2

            #rate_bottom_right score
            rate = rate_bottom_right
            bottom_right_score = 0 if rate < 0.01 else 1 if rate < 0.07 else 2
        else:
            rate = rate_up_left
            up_left_score = 0 if rate < 0.01 else 1 if rate < 0.05 else 2
            
            #rate_up_center score
            rate = rate_up_center
            up_center_score = 0 if rate < 0.01 else 1 if rate < 0.05 else 2
            
            #rate_up_right score
            rate = rate_up_right
            up_right_score = 0 if rate < 0.01 else 1 if rate < 0.05 else 2
            
            #rate_middle_left score
            #rate = rate_middle_left
            #middle_left_score = 0 if rate < 0.01 else 1 if rate < 0.05 else 2 if rate < 0.1 else 3 if rate < 0.12 else 4 if rate < 0.15 else 5
            
            #rate_middle_center score
            #rate = rate_middle_center
            #middle_center_score = 0 if rate < 0.01 else 1 if rate < 0.05 else 2 if rate < 0.1 else 3 if rate < 0.12 else 4 if rate < 0.15 else 5
            
            #rate_middle_right score
            #rate = rate_middle_right
            #middle_right_score = 0 if rate < 0.01 else 1 if rate < 0.05 else 2 if rate < 0.1 else 3 if rate < 0.12 else 4 if rate < 0.15 else 5
            
            #rate_bottom_left score
            rate = rate_bottom_left
            bottom_left_score = 0 if rate < 0.01 else 1 if rate < 0.05 else 2
            
            #rate_bottom_center score
            rate = rate_bottom_center
            bottom_center_score = 0 if rate < 0.01 else 1 if rate < 0.05 else 2
            
            #rate_bottom_right score
            rate = rate_bottom_right
            bottom_right_score = 0 if rate < 0.01 else 1 if rate < 0.05 else 2
            
   
    
        data_set = {"up_left": {"difference_rate":checks[0][1],"score" : up_left_score},
                    "up_center": {"difference_rate":checks[1][1],"score" : up_center_score},
                    "up_right":{"difference_rate":checks[2][1],"score" : up_right_score},
                    #"middle_left": {"difference_rate":checks[3][1],"score" : middle_left_score},
                    #"middle_center": {"difference_rate":checks[4][1],"score" : middle_center_score},
                    #"middle_right": {"difference_rate":checks[5][1],"score" : middle_right_score},
                    "bottom_left": {"difference_rate":checks[3][1],"score" : bottom_left_score},
                    "bottom_center": {"difference_rate":checks[4][1],"score" : bottom_center_score},
                    "bottom_right": {"difference_rate":checks[5][1],"score" : bottom_right_score}}
        json_dump = json.dumps(data_set)
        return json_dump
    
        


    def get_lipstick_color(self,filename,nb_color = 2):
        lips = self.crop_out_lips(filename, isolate_area = True, pre_img=None)
        colors = image_work.get_automatic_cluster_color(np.asarray(lips),nb_color)
        flatten_labels = [x[0] for x in colors[2]]
        labels_size = len(flatten_labels)
        chosen = []
        proportion_best = 0
        for i in range(len(colors[0])):
            c = colors[0][i]
            if c[0][0] > 10 and c[0][1] > 10 and c[0][2] > 10:
                candidate = [float(c[0][0]),float(c[0][1]),float(c[0][2])]
                proportion = flatten_labels.count(i)/labels_size
                print("Candidate : ",candidate, proportion)
                if proportion > proportion_best:
                    chosen = candidate
                    proportion_best = proportion
                    #return [float(i[0][0]),float(i[0][1]),float(i[0][2])]
        print("chosen : ",chosen, proportion_best)
        return chosen

    def perform_inside_check(self,fname,nb_t,m_type,m_color, color_diff, show_plot = False, diff_black=100):
        m_color = m_color[::-1]
        original_slice, makeup_slice, origins = image_work.generate_check_slices(filename=fname,faceCropper=self,nb_tiles=nb_t,makeup_type=m_type,makeup_color=m_color)
        all_checks = []
        print("pos ori :",origins)
        for i in range(nb_t[0]*nb_t[1]):
            original_slice[i].image = image_work.how_close_to_color(original_slice[i].image,[0, 0, 0],diff_black,dif_color_mark = m_color[::-1])[-1]
            makeup_slice[i].image = image_work.how_close_to_color(makeup_slice[i].image,[0, 0, 0],100,dif_color_mark = m_color[::-1])[-1]
            check = image_work.is_Too_different(color_diff,original_slice[i].image,makeup_slice[i].image) # treshold = 0 , whatever difference is marked
            check = list(check)
            check.append(original_slice[i])
            check = tuple(check)
            all_checks.append(check)
            print(i,check ,original_slice[i].coords)
        if show_plot:
            for i in range(nb_t[0]*nb_t[1]):
                tille_pos = i
                f, axarr = plt.subplots(3,1)
                axarr[0].imshow(original_slice[tille_pos].image)
                axarr[0].axis('off')
                axarr[0].set_title("original image("+str(i)+")")
                axarr[1].imshow(makeup_slice[tille_pos].image)
                axarr[1].axis('off')
                axarr[1].set_title("makeup image("+str(i)+")")
                axarr[2].imshow(all_checks[tille_pos][-2])
                axarr[2].axis('off')
                axarr[2].set_title("in green = color judged has different("+str(i)+")")
        return [origins,all_checks]

    def get_input_diff_color(self,filename,nb_color = 2):
        lips = self.crop_out_lips(filename, isolate_area = True, pre_img=None)
        colors = image_work.get_automatic_cluster_color(np.asarray(lips),nb_color)
        flatten_labels = [x[0] for x in colors[2]]
        labels_size = len(flatten_labels)
        res = []
        #proportion_best = 0
        for i in range(len(colors[0])):
            c = colors[0][i]
            proportion = flatten_labels.count(i)/labels_size
            res.append([c,proportion])
            #print("Candidate : ",candidate, proportion)
            #if proportion > proportion_best:
            #    chosen = candidate
            #    proportion_best = proportion
                    #return [float(i[0][0]),float(i[0][1]),float(i[0][2])]
        #print(res)
        return sorted(res, key=lambda x: x[1])

    

    def get_parameters_outside(self,filename,nb_color = 2, default=10):
        lips = self.crop_out_lips(filename, isolate_area = True, pre_img=None)
        colors = image_work.get_automatic_cluster_color(np.asarray(lips),nb_color)
        flatten_labels = [x[0] for x in colors[2]]
        labels_size = len(flatten_labels)
        chosen = []
        proportion_best = 0
        for i in range(len(colors[0])):
            c = colors[0][i]
            if c[0][0] > 10 and c[0][1] > 10 and c[0][2] > 10:
                candidate = [float(c[0][0]),float(c[0][1]),float(c[0][2])]
                proportion = flatten_labels.count(i)/labels_size
                if proportion > 0.2:
                    print("Candidate : ",candidate, proportion)
                    chosen.append([candidate, proportion,])
                #if proportion > proportion_best:
                #   chosen = candidate
                #   proportion_best = proportion
                    #return [float(i[0][0]),float(i[0][1]),float(i[0][2])]
        if len(chosen) < 2:
            print("only :", chosen[0])
            return [chosen[0][0],default * chosen[0][1]]
        
        res = []
        for i in chosen:
            somme = []
            for j in chosen:
                dist = distance.euclidean(rgb2lab(i[0]),rgb2lab(j[0]))
                if dist > 0:
                    somme.append(dist)
                    #print(i,dist)
            if len(somme) > 1:
                print(i,somme)
                print(i, statistics.stdev(somme), statistics.mean(somme))
                res.append([i[0],i[1] , statistics.stdev(somme), statistics.mean(somme)])
            else :
                #print(i, somme[0], somme[0])
                res.append([i[0],i[1] ,somme[0], somme[0]])
        if len(res) == 2:
            res = sorted(res, key=lambda x: x[1])
            print("only 2 candidates", res)
            print("chosen : ",res[-1])
            return [res[-1][0],res[-1][1] * default]
        else:
            res = sorted(res, key=lambda x: x[2]) 
            print("more than 2 candidates", res)
            print("chosen : ",res[0])

            if res[-1][-2] > 8:
                return [res[0][0],res[0][-2]]
            elif res[0][-1] > 10:
                return [res[0][0],res[0][-1]]
            else:
                return [res[0][0],15]
        
        return [res[-1][0],res[-1][-2]]

    def perform_outside_check(self,fname,nb_t,m_type,m_color, color_diff, pad = 100, show_plot=False,diff_black=100):
        print("tiles1 :",nb_t)
        sizes = [nb_t[0],nb_t[1]]
        ori, posi = image_work.generate_out_slices(filename=fname,faceCropper=self,nb_tiles=nb_t, part_out = 0, pad = pad)
        print("posi :",posi)
        nb_t = len(ori)
        #m_color = m_color[::-1]
        all_checks = []
        print("tiles2 :",nb_t)
        for i in range(sizes[0]*sizes[1]):
            b, g, r = ori[i].image.split()
            ori[i].image = Image.merge("RGB", (r, g, b))
            
            ori[i].image = image_work.how_close_to_color(ori[i].image,[0, 0, 0],diff_black,dif_color_mark = m_color)[-1]
        
            check = image_work.how_close_to_color(ori[i].image,m_color,color_diff) # 0 = no diffference between image color and color to check
            check = list(check)
            check.append(ori[i])
            check = tuple(check)
            all_checks.append(check)
            print(i,check[1] )
        
        if show_plot:
            for i in range(sizes[0]*sizes[1]):
                tille_pos = i
                #b, g, r = ori[tille_pos].image.split()
                #im = Image.merge("RGB", (r, g, b))

                f, axarr = plt.subplots(2,1)
                axarr[0].imshow(ori[tille_pos].image)
                axarr[0].axis('off')
                axarr[0].set_title("makeup image cropped("+str(i)+")")
                axarr[1].imshow(all_checks[tille_pos][-2])
                axarr[1].axis('off')
                axarr[1].set_title("in white = color judged has similar ("+str(i)+")")
        
        return [posi,all_checks]

  

    def get_opposed_parts(self,p, filename, preimg = None):
        mapper = {"p1":[[48,59,60],[54,55,64]],
            "p2":[[48,49,60],[53,54,64]],
            "p3":[[49,60,61],[53,63,64]],
            "p4":[[59,60,67],[64,65,55]],
            "p5":[[60,61,67],[63,64,65]],
            "p6":[[67,59,58],[55,56,65]],
            "p7":[[49,50,61],[52,53,63]],
            "p8":[[50,61,62],[52,62,63]],
            "p9":[[61,66,67],[63,65,66]],
            "p10":[[58,66,67],[56,65,66]],
            "p11":[[50,51,62],[51,52,62]],
            "p12":[[61,62,66],[62,63,66]],
            "p13":[[58,57,66],[56,57,66]]
            }
        
        if p not in mapper.keys():
            print("Part(",p,") is not referenced.")
            return 
        if preimg is None:
            img = cv2.imread(filename)
        else:
            img = preimg

        rect = self.detector(img)[0]
        sp = self.predictor(img, rect)
        pts= mapper[p]
        left_part = extract_part(pts[0], img,rect,sp)
        right_part = extract_part(pts[1], img,rect,sp)
        return left_part, right_part


    def crop_out_lips(self, filename, isolate_area = False, pre_img=None):
        if not(pre_img is None):
            img = pre_img
        else:
            img = cv2.imread(filename)
        try:
            rect = self.detector(img)[0]
            sp = self.predictor(img, rect)
            landmarks = np.array([[p.x, p.y] for p in sp.parts()])
            outline = landmarks[[
                x + 48 for x in range(12)]+[48]+[x + 60 for x in range(8)]]
            Y, X = skimage.draw.polygon(outline[:, 1], outline[:, 0])
            cropped_img = np.zeros(img.shape, dtype=np.uint8)
            cropped_img[Y, X] = img[Y, X]

            shape = sp
            if isolate_area:
                xmouthpoints = [shape.part(x).x for x in range(48, 67)]
                ymouthpoints = [shape.part(x).y for x in range(48, 67)]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)
                pos_origin = [[minx, miny], [maxx, maxy]]

                pad = 0
                #crop_image = img.copy()
                cropped_img = cropped_img[miny - pad:maxy+pad, minx-pad:maxx+pad]

            result_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
            return Image.fromarray(result_rgb)
        except IndexError:
            return False

    def crop_face_without_lips(self, filename):
        img = cv2.imread(filename)
        try:
            rect = self.detector(img)[0]
            sp = self.predictor(img, rect)
            landmarks = np.array([[p.x, p.y] for p in sp.parts()])
            outline = landmarks[[
                x + 48 for x in range(12)]+[48]+[x + 60 for x in range(8)]]
            Y, X = skimage.draw.polygon(outline[:, 1], outline[:, 0])
            img[Y, X] = 0
            result_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return Image.fromarray(result_rgb)
        except IndexError:
            return False

    def isolate_mouth_cv(self, filename, mouth_only=True, preImg=None, pre_shape=None, crop_lips=False, keep_teeh=False,lips_only = False,pad=0): #keep teeh if crop_lips
        pos_origin = []
        try:
            if preImg is None:
                img = cv2.imread(filename)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dets = self.detector(img, 1)
            else:
                #pil_image = preImg.convert('RGB')
                #open_cv_image = np.array(pil_image)
                img = preImg#open_cv_image
                dets = self.detector(img, 1)
            #print("Number of faces detected: {}".format(len(dets)))
            #result_rgb = False

            for k, d in enumerate(dets[:1]):
                # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                #   k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                if pre_shape is None:
                    shape = self.predictor(img, d)
                else:
                    shape = pre_shape
                if lips_only:
                    sp = shape
                    landmarks = np.array([[p.x, p.y] for p in sp.parts()])
                    outline = landmarks[[
                        x + 48 for x in range(12)]+[48]+[x + 60 for x in range(8)]]
                    Y, X = skimage.draw.polygon(outline[:, 1], outline[:, 0])
                    cropped_img = np.zeros(img.shape, dtype=np.uint8)
                    cropped_img[Y, X] = img[Y, X]
                    img = cropped_img

                elif crop_lips:
                    sp = shape
                    landmarks = np.array([[p.x, p.y] for p in sp.parts()])
                    if keep_teeh:
                        outline = landmarks[[
                            x + 48 for x in range(12)]+[48]+[x + 60 for x in range(8)]]
                    else:
                        outline = landmarks[[
                            x + 48 for x in range(12)]+[48]]
                    Y, X = skimage.draw.polygon(outline[:, 1], outline[:, 0])
                    img[Y, X] = 0
                elif keep_teeh:
                    sp = shape
                    landmarks = np.array([[p.x, p.y] for p in sp.parts()])
                    outline = landmarks[[x + 60 for x in range(8)]]
                    Y, X = skimage.draw.polygon(outline[:, 1], outline[:, 0])
                    img[Y, X] = 0

                # The next lines of code just get the coordinates for the mouth
                # and crop the mouth from the image.This part can probably be optimised
                # by taking only the outer most points.
                xmouthpoints = [shape.part(x).x for x in range(48, 67)]
                ymouthpoints = [shape.part(x).y for x in range(48, 67)]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)
                pos_origin = [[minx - pad, miny -pad], [maxx -pad, maxy-pad]]

                crop_image = img.copy()
                if mouth_only:
                    crop_image = crop_image[miny -
                                            pad:maxy+pad, minx-pad:maxx+pad]
                else:
                    crop_image[0:miny-pad, 0::] = 0  # haut
                    crop_image[maxy+pad::, 0::] = 0  # bas
                    crop_image[0::, 0:minx - pad] = 0  # gauche
                    crop_image[0::, maxx+pad::] = 0  # droite
                # result_rgb = cv2.cvtColor(crop_image, cv2.)
            if len(dets) > 0:
                return PIL.Image.fromarray(crop_image), shape, pos_origin
            return False
        except IndexError:
            return False
    

    def isolate_mouth(self, filename, mouth_only=True, preImg=None, pre_shape=None, crop_lips=False,pad=10):
        pos_origin = []
        try:
            if preImg is None:
                img = cv2.imread(filename)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dets = self.detector(img, 1)
            else:
                pil_image = preImg.convert('RGB')
                open_cv_image = np.array(pil_image)
                img = open_cv_image
                dets = self.detector(open_cv_image, 1)
            #print("Number of faces detected: {}".format(len(dets)))
            #result_rgb = False

            for k, d in enumerate(dets):
                # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                #   k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                if pre_shape is None:
                    shape = self.predictor(img, d)
                else:
                    shape = pre_shape

                if crop_lips:
                    sp = shape
                    landmarks = np.array([[p.x, p.y] for p in sp.parts()])
                    outline = landmarks[[
                        x + 48 for x in range(12)]+[48]+[x + 60 for x in range(8)]]
                    Y, X = skimage.draw.polygon(outline[:, 1], outline[:, 0])
                    img[Y, X] = 0
                # The next lines of code just get the coordinates for the mouth
                # and crop the mouth from the image.This part can probably be optimised
                # by taking only the outer most points.
                xmouthpoints = [shape.part(x).x for x in range(48, 67)]
                ymouthpoints = [shape.part(x).y for x in range(48, 67)]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)
                pos_origin = [[minx - pad, miny -pad], [maxx -pad, maxy-pad]]

                crop_image = img.copy()
                if mouth_only:
                    crop_image = crop_image[miny -
                                            pad:maxy+pad, minx-pad:maxx+pad]
                else:
                    crop_image[0:miny-pad, 0::] = 0  # haut
                    crop_image[maxy+pad::, 0::] = 0  # bas
                    crop_image[0::, 0:minx - pad] = 0  # gauche
                    crop_image[0::, maxx+pad::] = 0  # droite
                # result_rgb = cv2.cvtColor(crop_image, cv2.)
            if len(dets) > 0:
                return PIL.Image.fromarray(crop_image), shape, pos_origin
            return False
        except IndexError:
            return False

    def isolate_eye(self, filename, pre_shape=None, eye_only=True, preImg=None):
        try:
            if preImg is None:
                img = cv2.imread(filename)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dets = self.detector(img, 1)
            else:
                pil_image = preImg.convert('RGB')
                open_cv_image = np.array(pil_image)
                img = open_cv_image
                dets = self.detector(open_cv_image, 1)
            #print("Number of faces detected: {}".format(len(dets)))
            #result_rgb = False

            for k, d in enumerate(dets):
                # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                #   k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                if pre_shape is None:
                    shape = self.predictor(img, d)
                else:
                    shape = pre_shape
                # The next lines of code just get the coordinates for the mouth
                # and crop the mouth from the image.This part can probably be optimised
                # by taking only the outer most points.
                xmouthpoints = [shape.part(x).x for x in range(18, 27)]
                ymouthpoints = [shape.part(x).y for x in range(37, 48)]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)
                pos_origin = [[minx, miny], [maxx, maxy]]

                pad = 10
                crop_image = img.copy()
                if eye_only:
                    crop_image = crop_image[miny -
                                            pad:maxy+pad, minx-pad:maxx+pad]
                else:
                    crop_image[0:miny-pad, 0::] = 0  # haut
                    crop_image[maxy+pad::, 0::] = 0  # bas
                    crop_image[0::, 0:minx - pad] = 0  # gauche
                    crop_image[0::, maxx+pad::] = 0  # droite
                #result_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            if len(dets) > 0:
                return PIL.Image.fromarray(crop_image), shape, pos_origin
            return False
        except IndexError:
            return False

    def isolate_cheeks(self, filename, pre_shape=None, eye_only=True, preImg=None):
        try:
            if preImg is None:
                img = cv2.imread(filename)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dets = self.detector(img, 1)
            else:
                pil_image = preImg.convert('RGB')
                open_cv_image = np.array(pil_image)
                img = open_cv_image
                dets = self.detector(open_cv_image, 1)
            #print("Number of faces detected: {}".format(len(dets)))
            #result_rgb = False

            for k, d in enumerate(dets):
                # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                #   k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                if pre_shape is None:
                    shape = self.predictor(img, d)
                else:
                    shape = pre_shape
                # The next lines of code just get the coordinates for the mouth
                # and crop the mouth from the image.This part can probably be optimised
                # by taking only the outer most points.
                xmouthpoints = [shape.part(x).x for x in [1, 3, 15, 13]]
                ymouthpoints = [shape.part(x).y for x in [1, 3, 15, 13]]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)
                pos_origin = [[minx, miny], [maxx, maxy]]

                pad = 10
                crop_image = img.copy()
                if eye_only:
                    crop_image = crop_image[miny -
                                            pad:maxy+pad, minx-pad:maxx+pad]
                else:
                    crop_image[0:miny-pad, 0::] = 0  # haut
                    crop_image[maxy+pad::, 0::] = 0  # bas
                    crop_image[0::, 0:minx - pad] = 0  # gauche
                    crop_image[0::, maxx+pad::] = 0  # droite
                #result_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            if len(dets) > 0:
                return PIL.Image.fromarray(crop_image), shape, pos_origin
            return False
        except IndexError:
            return False

    def calc_columns_rows(self, n):
        """
        Calculate the number of columns and rows required to divide an image
        into ``n`` parts.
        Return a tuple of integers in the format (num_columns, num_rows)
        """

        num_columns = int(ceil(sqrt(n)))
        num_rows = int(ceil(n / float(num_columns)))
        return (num_columns, num_rows)

    def get_combined_size(self, tiles):
        """Calculate combined size of tiles."""
        # TODO: Refactor calculating layout to avoid repetition.
        columns, rows = self.calc_columns_rows(len(tiles))
        tile_size = tiles[0].image.size
        return (tile_size[0] * columns, tile_size[1] * rows)

    def join(self, tiles, width=0, height=0):
        """
        @param ``tiles`` - Tuple of ``Image`` instances.
        @param ``width`` - Optional, width of combined image.
        @param ``height`` - Optional, height of combined image.
        @return ``Image`` instance.
        """
        # Don't calculate size if width and height are provided
        # this allows an application that knows what the
        # combined size should be to construct an image when
        # pieces are missing.

        if width > 0 and height > 0:
            im = Image.new("RGBA", (width, height), None)
        else:
            im = Image.new("RGBA", self.get_combined_size(tiles), None)
        columns, rows = self.calc_columns_rows(len(tiles))
        for tile in tiles:
            try:
                im.paste(tile.image, tile.coords)
            except IOError:
                # do nothing, blank out the image
                continue
        return im

    def validate_image(self, image, number_tiles):
        """Basic sanity checks prior to performing a split."""
        TILE_LIMIT = 99 * 99

        try:
            number_tiles = int(number_tiles)
        except BaseException:
            raise ValueError("number_tiles could not be cast to integer.")

        if number_tiles > TILE_LIMIT or number_tiles < 2:
            raise ValueError(
                "Number of tiles must be between 2 and {} (you \
                            asked for {}).".format(
                    TILE_LIMIT, number_tiles
                )
            )

    def validate_image_col_row(self, image, col, row):
        """Basic checks for columns and rows values"""
        SPLIT_LIMIT = 99

        try:
            col = int(col)
            row = int(row)
        except BaseException:
            raise ValueError(
                "columns and rows values could not be cast to integer.")

        if col < 1 or row < 1 or col > SPLIT_LIMIT or row > SPLIT_LIMIT:
            raise ValueError(
                f"Number of columns and rows must be between 1 and"
                f"{SPLIT_LIMIT} (you asked for rows: {row} and col: {col})."
            )
        if col == 1 and row == 1:
            raise ValueError(
                "There is nothing to divide. You asked for the entire image.")

    def slice_img(self,
                  filename=None,
                  pre_img=None,
                  number_tiles=None,
                  col=None,
                  row=None,
                  DecompressionBombWarning=False,
                  ):
        """
        Split an image into a specified number of tiles.
        Args:
        filename (str):  The filename of the image to split.
        number_tiles (int):  The number of tiles required.
        Kwargs:
        save (bool): Whether or not to save tiles to disk.
        DecompressionBombWarning (bool): Whether to suppress
        Pillow DecompressionBombWarning
        Returns:
            Tuple of :class:`Tile` instances.
        """
        if DecompressionBombWarning is False:
            Image.MAX_IMAGE_PIXELS = None

        if pre_img is None:
            im = Image.open(filename)
        else:
            im = pre_img
        im_w, im_h = im.size

        columns = 0
        rows = 0
        if number_tiles:
            self.validate_image(im, number_tiles)
            columns, rows = self.calc_columns_rows(number_tiles)
        else:
            self.validate_image_col_row(im, col, row)
            columns = col
            rows = row

        tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))

        tiles = []
        number = 1
        # -rows for rounding error.
        for pos_y in range(0, im_h - rows, tile_h):
            for pos_x in range(0, im_w - columns, tile_w):  # as above.
                area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
                image = im.crop(area)
                position = (int(floor(pos_x / tile_w)) + 1,
                            int(floor(pos_y / tile_h)) + 1)
                coords = (pos_x, pos_y)
                tile = Tile(image, number, position, coords)
                tiles.append(tile)
                number += 1

        return tuple(tiles)

    def save_tiles(self, tiles, prefix="", directory=os.getcwd(), format="png"):
        """
        Write image files to disk. Create specified folder(s) if they
        don't exist. Return list of :class:`Tile` instance.
        Args:
        tiles (list):  List, tuple or set of :class:`Tile` objects to save.
        prefix (str):  Filename prefix of saved tiles.
        Kwargs:
        directory (str):  Directory to save tiles. Created if non-existant.
        Returns:
            Tuple of :class:`Tile` instances.
        """
        for tile in tiles:
            tile.save(
                filename=tile.generate_filename(
                    prefix=prefix, directory=directory, format=format
                ),
                format=format,
            )
        return tuple(tiles)

    def get_image_column_row(self, filename):
        """Determine column and row position for filename."""
        row, column = os.path.splitext(filename)[0][-5:].split("_")
        return (int(column) - 1, int(row) - 1)

    def open_images_in(self, directory):
        """Open all images in a directory. Return tuple of Tile instances."""

        files = [
            filename
            for filename in os.listdir(directory)
            if "_" in filename and not filename.startswith("joined")
        ]
        tiles = []
        if len(files) > 0:
            i = 0
            for file in files:
                pos = self.get_image_column_row(file)
                im = Image.open(os.path.join(directory, file))

                position_xy = [0, 0]
                count = 0
                for a, b in zip(pos, im.size):
                    position_xy[count] = a * b
                    count = count + 1
                tiles.append(
                    Tile(
                        image=im,
                        position=pos,
                        number=i + 1,
                        coords=position_xy,
                        filename=file,
                    )
                )
                i = i + 1
        return tiles


def PIL_to_CV(pilImg, isLab=False):
    open_cv_image = np.array(pilImg)
    if isLab:
        image1_lab = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2Lab)
        return image1_lab
    return open_cv_image


def original_and_makeup_slices(filename, faceCropper, nb_tiles, makeup_type, makeup_color):
    # list with original and makeup version of the image
    print("ok1")
    fc = faceCropper
    print("ok2")
    pp = add_makeup_PIL(filename, fc, m_type=makeup_type, col=makeup_color)
    print("ok3")
    if makeup_type == 0:  # Lipstick
        mouth_original, m_o_shape, origine = fc.isolate_mouth(
            "", preImg=pp[0])  # .convert("RGB")
        mouth_target, m_t_shape, origine2 = fc.isolate_mouth(
            "", preImg=pp[1], pre_shape=m_o_shape)
        m_o_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_original)
        m_t_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_target)
        return m_o_slices, m_t_slices, origine
    if makeup_type == 1:  # blush
        #print( "HMMMM ", pp)
        mouth_original, m_o_shape, origine = fc.isolate_cheeks(
            "", preImg=pp[0])  # .convert("RGB")
        mouth_target, m_t_shape, origine2 = fc.isolate_cheeks(
            "", preImg=pp[1], pre_shape=m_o_shape)
        m_o_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_original)
        m_t_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_target)
        return m_o_slices, m_t_slices, origine
    if makeup_type == 2:  # eye shadow
        print("HMMMM 2", pp)
        mouth_original, m_o_shape, origine = fc.isolate_eye(
            "", preImg=pp[0])  # .convert("RGB")
        mouth_target, m_t_shape, origine2 = fc.isolate_eye(
            "", preImg=pp[1], pre_shape=m_o_shape)
        m_o_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_original)
        m_t_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_target)
        return m_o_slices, m_t_slices, origine
    else:
        return False



def add_makeup_check(file, face_cropper, m_type=0, col=None):
    original_open_cv_image = cv2.imread(file)
    # Convert RGB to BGR
    #original_open_cv_image = original_open_cv_image[:, :, ::-1].copy()
    # Convert back
    #original_open_cv_image = cv2.cvtColor(original_open_cv_image, cv2.COLOR_BGR2RGB)

    rect = face_cropper.detector(original_open_cv_image)[0]
    sp = face_cropper.predictor(original_open_cv_image, rect)
    landmarks = np.array([[p.x, p.y] for p in sp.parts()])
    makeup_saloon = makeup(original_open_cv_image)
    if m_type == 0:  # lipstick
        img = np.uint8(makeup_saloon.apply_lipstick2(landmarks, [col[0], col[1], col[2]]))
    if m_type == 1:  # blush
        img = np.uint8(makeup_saloon.apply_blush(landmarks, col[0], col[1], col[2]))
    if m_type == 2:  # eye shadow
        print("ziak 1")
        img = np.uint8(makeup_saloon.apply_eyeshadow(landmarks, col[0], col[1], col[2]))
        print("ziak 2")
    #img_cv = np.array(img)
    #img_cv = img_cv[:, :, ::-1].copy()
    result_rgb = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return cv2.cvtColor(original_open_cv_image, cv2.COLOR_RGB2BGR), result_rgb

def generate_check_slices(filename, faceCropper, nb_tiles, makeup_type, makeup_color):
    # list with original and makeup version of the image
    print("ok11")
    fc = faceCropper
    print("ok22")
    pp = add_makeup_check(filename, fc, m_type=makeup_type, col=makeup_color)
    print("ok33")
    if makeup_type == 0:  # Lipstick
        mouth_original, m_o_shape, origine = fc.isolate_mouth_cv(
            "", preImg=pp[0],lips_only = True)  # .convert("RGB")
        mouth_target, m_t_shape, origine2 = fc.isolate_mouth_cv(
            "", preImg=pp[1], pre_shape=m_o_shape,lips_only = True)
        m_o_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_original)
        m_t_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_target)
        return m_o_slices, m_t_slices, origine
    if makeup_type == 1:  # blush
        #print( "HMMMM ", pp)
        mouth_original, m_o_shape, origine = fc.isolate_cheeks(
            "", preImg=pp[0])  # .convert("RGB")
        mouth_target, m_t_shape, origine2 = fc.isolate_cheeks(
            "", preImg=pp[1], pre_shape=m_o_shape)
        m_o_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_original)
        m_t_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_target)
        return m_o_slices, m_t_slices, origine
    if makeup_type == 2:  # eye shadow
        print("HMMMM 2", pp)
        mouth_original, m_o_shape, origine = fc.isolate_eye(
            "", preImg=pp[0])  # .convert("RGB")
        mouth_target, m_t_shape, origine2 = fc.isolate_eye(
            "", preImg=pp[1], pre_shape=m_o_shape)
        m_o_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_original)
        m_t_slices = fc.slice_img(
            "", row = nb_tiles[0], col =nb_tiles[1], pre_img=mouth_target)
        return m_o_slices, m_t_slices, origine
    else:
        return False




def original_and_lips_makeup_slices(filename, faceCropper, makeup_color):
    # list with original and makeup version of the image
    fc = faceCropper
    pp = add_makeup_PIL(filename, fc, m_type=0, col=makeup_color)
    print("Done ici")
    mouth_original = PIL_to_CV(pp[0])
    mouth_target = PIL_to_CV(pp[1])
    dict_original = {}
    dict_target = {}
    for i in range(13):
        if i+1 not in [1,2,5,9,12]:
            part = "p"+str(i+1)
            opposed_part_original = fc.get_opposed_parts(part,filename,preimg=mouth_original)
            opposed_part_target = fc.get_opposed_parts(part,filename,preimg=mouth_target)
            dict_original[part] = opposed_part_original
            dict_target[part] = opposed_part_target
    return dict_original,dict_target
    
def generate_out_slices(filename, faceCropper, nb_tiles, part_out=0, pad = 40):
    fc = faceCropper
    original_PIL = cv2.imread(filename)#PIL.Image.open(filename).convert('RGB')
    if part_out == 0:  # Isolate mouth without lips
        mouth_original, m_o_shape, origine = fc.isolate_mouth_cv(
            "", preImg=original_PIL, crop_lips=True, pad = pad)
    m_o_slices = fc.slice_img(
        "",row = nb_tiles[0], col =nb_tiles[1] , pre_img=mouth_original)
    return m_o_slices, origine

def original_out_slices(filename, faceCropper, nb_tiles, part_out=0):
    fc = faceCropper
    original_PIL = PIL.Image.open(filename).convert('RGB')
    if part_out == 0:  # Isolate mouth without lips
        mouth_original, m_o_shape, origine = fc.isolate_mouth(
            "", preImg=original_PIL, crop_lips=True)
    m_o_slices = fc.slice_img(
        "", row = nb_tiles[0], col =nb_tiles[1] , pre_img=mouth_original)
    return m_o_slices, origine


def compute_deltaE_matrix(img1, img2):
    imgLab_o = PIL_to_CV(img1, isLab=True)
    imgLab_t = PIL_to_CV(img2, isLab=True)
    delta_E = colour.delta_E(imgLab_o, imgLab_t)
    return delta_E


def is_Too_different(treshold, img1, img2):
    delta_E = compute_deltaE_matrix(img1, img2)
    pos = []
    imtmp = np.array(img1.copy())
    for x in range(len(delta_E)):
        for y in range(len(delta_E[0])):
            if delta_E[x][y] > treshold:
                #print(x," and ",y)
                pos.append([x, y])
                imtmp[x, y] = [0, 255, 0]
    return len(pos), len(pos) / (len(delta_E) * len(delta_E[0])), PIL.Image.fromarray(imtmp)


def how_close_to_color(imgPIL, color, treshold, isPil=True,dif_color_mark = [255, 255, 255]):
    if isPil:
        open_cv_image = np.array(imgPIL)
    else:
        open_cv_image = imgPIL

    all_color = open_cv_image.copy()
    all_color[:, :] = color
    delta_E = compute_deltaE_matrix(open_cv_image, all_color)
    pos = []
    imtmp = open_cv_image.copy()
    for x in range(len(delta_E)):
        for y in range(len(delta_E[0])):
            test = delta_E[x][y]
            if test < treshold and test > 0:
                pos.append([x, y, delta_E[x][y]])
                imtmp[x, y] = dif_color_mark
    return len(pos), len(pos) / (len(delta_E) * len(delta_E[0])), all_color, pos, PIL.Image.fromarray(imtmp)


def get_parts_symmetry(left_part, right_part,nb_cluster,color_distance_treshold):
    left_slice = get_automatic_cluster_color(np.asarray(left_part),nb_cluster)
    right_slice = get_automatic_cluster_color(np.asarray(right_part),nb_cluster)
    res = get_similarity_insight(left_slice,right_slice,color_distance_treshold)


def extract_part(pts, img,rect,sp):
    
    shape = sp
    pts2 = np.array([[shape.part(x).x,shape.part(x).y] for x in pts])

    #pad = 0
    #crop_image = img.copy()
    #cropped_img = cropped_img[miny - pad:maxy+pad, minx-pad:maxx+pad]
    rect = cv2.boundingRect(pts2)
    x,y,w,h = rect
    croped = img[y:y+h, x:x+w].copy()
    pts2 = pts2 - pts2.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts2], -1, (255, 255, 255), -1, cv2.LINE_AA)
    dst = cv2.bitwise_and(croped, croped, mask=mask)
    
    result_rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    return Image.fromarray(result_rgb)


def get_clusters_color(img, k):
    Z = np.float32(img) 
    Z1 = Z/255.0

    Z2 = cv2.cvtColor(Z1,44)
    Z3 = Z2.reshape((-1,3))
    Z3 = np.asarray([x for x in Z3 if x[0] > 1], dtype=np.float32)
    #print(Z3.shape)

    K = k

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    #print("Calculting Centers for Lab space ......\n")
    ret,label,center=cv2.kmeans(Z3,K,None,criteria,100,cv2.KMEANS_PP_CENTERS)  #distance function for CIE Lab : E76 similar to euclidean distance


    #print("Centers in Lab space : \n",center)
    center2 = (cv2.cvtColor(center.reshape((K,1,3)),56))*255.0  #convert center coordinates to rgb
    #print("Centers in rgb space based on lab k-means : \n",center2)
    # Now convert back into uint8, and make original image
    center3 = np.uint8(center2)
    #res = center3[label.flatten()]

    #print(res.shape)
    #res2 = res.reshape((img.shape))
    return center3, center, label



def replace_img_part(original_img, substitutes):
    #print("min x =",origin)
    #print("subtitute = ", substitute[0][-2])
    for substitute in substitutes:
        for i in range(len(substitute[0])):
            origin = substitute[1]
            tile = substitute[0][i][-1]
        #   print("tile ",tile.coords)
            pos = (origin[0]+ tile.coords[0],origin[1]+tile.coords[1])
        #  print(pos)
        #  print(substitute[i])#.coords)
            mask = substitute[0][i][-2].convert('L')#.resize(im1.size)
            original_img.paste(substitute[0][i][-2], pos,mask)
    return original_img

def apply_errors_on_image(fname, results):
    img = cv2.imread(fname)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)

    substitutes = []
    for i in results:
        substitutes.append([i[1], i[0][0]])
    return replace_img_part(img,substitutes)


def get_automatic_cluster_color(img,k):
    treshold = (1/k) / 2.3
    rgb_colors,lab_colors,labels = get_clusters_color(img,k)
    centroid_to_keep = []
    flatten_labels = [x[0] for x in labels]#.count(2)
    labels_size = len(labels)
    for i in range(k):
        proportion = flatten_labels.count(i)/labels_size
        if flatten_labels.count(i)/labels_size > treshold-treshold:
            centroid_to_keep.append(i)
        else:
            print("centroid",i,"removed. (",proportion,")")
    res_rgb = [rgb_colors[j] for j in centroid_to_keep]
    res_lab = [lab_colors[j] for j in centroid_to_keep]
    return res_rgb,res_lab,labels
    

def get_similarity_insight(kmean_result_1,kmean_result_2,treshold_color):
    similar_dict, different_1,different_2 = get_associations2(kmean_result_1[1],kmean_result_2[1], treshold_color)#[0]
    nb_color_c1 = len(kmean_result_1[1])
    nb_color_c2 = len(kmean_result_2[1])
    if len(different_1) == len(different_2) == 0:
        print("Symmetrical:",similar_dict,"\n\n\n")
        return True
    else:
        print("Not symmetrical\nleft colors with no acceptable match:",different_1,"\nRight colors with no acceptable match:",different_2,"\n\n")
        return False


def get_associations2(l1,l2, dist_min):
    res_dict=defaultdict(list)
    res_not_attributed_dict_1 = defaultdict(list)
    res_not_attributed_dict_2 = defaultdict(list)
    attributed_i = []
    attributed_j = []
    for i in range(len(l1)):
        for j in range(len(l2)):
            #if j not in attributed_j:
            dist = distance.euclidean(l1[i], l2[j])
            if dist < dist_min:
                #print("ok",dist)
                res_dict[i].append((j,dist))
                attributed_j.append(j)
                attributed_i.append(i)
            #else:
                #print("not ok",dist)
                    
    index_l1 = range(len(l1))
    index_l2 = range(len(l2))
    non_attributed_l1 = [i for j, i in enumerate(index_l1) if j not in attributed_i]
    non_attributed_l2 = [i for j, i in enumerate(index_l2) if j not in attributed_j]
    for i in non_attributed_l1:
        for j in l2:
            distt = distance.euclidean(l1[i], j)
            res_not_attributed_dict_1[i].append((distt,l1[i]))
    
    for i in non_attributed_l2:
        for j in l1:
            distt = distance.euclidean(l2[i], j)
            res_not_attributed_dict_2[i].append((distt,l2[i]))
    #print(non_attributed_l1)
    #print(non_attributed_l2)
    #print(set(attributed_i))
    #print(set(attributed_j))
    return res_dict, res_not_attributed_dict_1,res_not_attributed_dict_2

def rgb2lab (inputColor ) :
    num = 0
    RGB = [0, 0, 0]

    for value in inputColor :
        value = float(value) / 255

        if value > 0.04045 :
            value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
        else :
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0,]

    X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
    Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
    Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
    XYZ[ 0 ] = round( X, 4 )
    XYZ[ 1 ] = round( Y, 4 )
    XYZ[ 2 ] = round( Z, 4 )

    XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
    XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ :

        if value > 0.008856 :
            value = value ** ( 0.3333333333333333 )
        else :
            value = ( 7.787 * value ) + ( 16 / 116 )

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = ( 116 * XYZ[ 1 ] ) - 16
    a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
    b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

    Lab [ 0 ] = round( L, 4 )
    Lab [ 1 ] = round( a, 4 )
    Lab [ 2 ] = round( b, 4 )

    return Lab

# Change version number and run :
# python3 setup.py sdist bdist_wheel (build it all)
# python3 -m twine upload --repository-url https://upload.pypi.org/legacy/  dist/* (launch to web)
