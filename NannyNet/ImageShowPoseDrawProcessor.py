# press q to stop processing, pres space to pause/continue processing

from Processor import Processor
import Conveyor
import cv2
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

class ImageShowPoseDrawProcessor(Processor):
    def __init__(self, **kwargs):
        cv2.startWindowThread()
        cv2.namedWindow("Preview")
        
    def ProcessInput(self, conveyorResult):
        if ('PersonPoseDrawProcessor' in conveyorResult.analyzers):
            self._display_image(conveyorResult.analyzers['PersonPoseDrawProcessor']["image"], conveyorResult)
        return True

    def Clean(self):
        cv2.destroyAllWindows()
        return True

    def _display_image(self, image, conveyorResult):
        cv2.imshow('Preview', image)
        key = cv2.waitKey(1)
        if key == ord('q'):
            conveyorResult.ended = True
        if key == ord(' '):
            key = cv2.waitKey(1)
            while key == ord(' '):
                key = cv2.waitKey(1)
            while key != ord(' '):
                key = cv2.waitKey(1)
            
