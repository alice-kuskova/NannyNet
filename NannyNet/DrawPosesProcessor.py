from Processor import Processor
import Conveyor
import os
import cv2
import numpy as np
from enum import Enum

class DrawPosesProcessor(Processor):
    def __init__(self, **kwargs):
        self.CocoPairs = [
            (1, 2), (1, 5), (2, 3), (3, 4), (5, 6), (6, 7), (1, 8), (8, 9), (9, 10), (1, 11),
            (11, 12), (12, 13), (1, 0), (0, 14), (14, 16), (0, 15), (15, 17), (2, 16), (5, 17)
        ]

        self.CocoPairsRender = self.CocoPairs[:-2]

        self.CocoColors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0],
              [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
              [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]

    
    def ProcessInput(self, conveyorResult):
        humans = conveyorResult.analyzers["PersonPoseRecognizerProcessor"]["humans"]
        if (humans  is not None and conveyorResult.image is not None):
            if (conveyorResult.image_result is None):
                conveyorResult.image_result  = conveyorResult.image.copy()
            conveyorResult.image_result = self.draw_humans(conveyorResult.image_result, humans, human_ids=None, imgcopy=False)
            
        return True

    def Clean(self):
        return True

    def draw_humans(self, npimg, humans, human_ids, imgcopy=False):
        if imgcopy:
            npimg = np.copy(npimg)
        image_h, image_w = npimg.shape[:2]
        centers = {}
        ind = 0
        for human in humans:
            if (human_ids is not None and human_ids[ind] is not None):
                human_color = self.CocoColors[(human_ids * 3) % self.CocoColors.__len__()]
            else:
                human_color = self.CocoColors[(ind * 3) % self.CocoColors.__len__()]

            # draw point
            for i in range(CocoPart.Background.value):
                if i not in human.body_parts.keys():
                    continue

                body_part = human.body_parts[i]
                center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
                centers[i] = center
                cv2.circle(npimg, center, 3, human_color, thickness=1, lineType=8, shift=0)

            # draw line
            for pair_order, pair in enumerate(self.CocoPairsRender):
                if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
                    continue

                # npimg = cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)
                cv2.line(npimg, centers[pair[0]], centers[pair[1]], human_color, 1)
            ind += 1
        return npimg

class CocoPart(Enum):
        Nose = 0
        Neck = 1
        RShoulder = 2
        RElbow = 3
        RWrist = 4
        LShoulder = 5
        LElbow = 6
        LWrist = 7
        RHip = 8
        RKnee = 9
        RAnkle = 10
        LHip = 11
        LKnee = 12
        LAnkle = 13
        REye = 14
        LEye = 15
        REar = 16
        LEar = 17
        Background = 18
