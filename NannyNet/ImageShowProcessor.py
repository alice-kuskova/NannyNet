from Processor import Processor;
import Conveyor;
import cv2;

class ImageShowProcessor(Processor):
    def __init__(self, **kwargs):
        cv2.startWindowThread();
        cv2.namedWindow("Preview");

    def ProcessInput(self, conveyorResult):
        if (conveyorResult.image is not None):
            cv2.imshow('Preview', conveyorResult.image);
            if cv2.waitKey(1) == ord('q'):
                conveyorResult.ended = True;
        return True;

    def Clean(self):
        cv2.destroyAllWindows();
        return True;
