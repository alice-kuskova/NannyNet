from Processor import Processor
import Conveyor
import cv2;
import numpy as np

class ImageShowProcessor(Processor):
    def __init__(self, **kwargs):
        cv2.startWindowThread()
        cv2.namedWindow("Preview")
        
    def ProcessInput(self, conveyorResult):
        if (conveyorResult.image_result is not None):
            image_copy = conveyorResult.image_result
        else:
            image_copy = conveyorResult.image
        if (image_copy is not None):
           cv2.imshow('Preview', image_copy)
           key = cv2.waitKey(1)
           if key == ord('q'):
               conveyorResult.ended = True
           if key == ord(' '):
               key = cv2.waitKey(1)
               while key == ord(' '):
                   key = cv2.waitKey(1)
               while key != ord(' '):
                   key = cv2.waitKey(1)
        return True

    def Clean(self):
        cv2.destroyAllWindows()
        return True
