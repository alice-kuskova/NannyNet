from Processor import Processor;
import Conveyor;
import cv2;

class VideoFileProcessor(Processor):
    def __init__(self, **kwargs):
        self.__filePath = kwargs["filePath"];
        self.__fromFrame = kwargs["fromFrame"] if kwargs["fromFrame"] >= 2 else 1;
        self.__toFrame = None if kwargs["toFrame"] is None or kwargs["toFrame"] < self.__fromFrame else kwargs["toFrame"];
        self.__frameStep = kwargs["frameStep"] if kwargs["frameStep"] >= 1 else 1;
        self.__lastFrame = None;
        self.__videoStream = None;

    def ProcessInput(self, conveyorResult):
        if self.__videoStream == None:
            if self.__InitVideo() is False:
                conveyorResult.errors.append("VideoFileProcessor can not read file "+self.__filePath);
                return False;
        if self.__lastFrame == None:
            self.__lastFrame = self.__fromFrame;
        else:
            self.__lastFrame = self.__lastFrame + self.__frameStep;
            if self.__lastFrame > self.__toFrame:
                conveyorResult.ended = True;
                return True;
        if not self.__GetFrame(self.__lastFrame, conveyorResult):
            conveyorResult.errors.append("VideoFileProcessor can not get frame " + str(self.__lastFrame) + " from file " + self.__filePath);
            return False;
        return True;

    def Clean(self):
        return self.__CloseStream();

    def __InitVideo(self):
        result = self.__OpenSream();
        if not result:
            conveyorResult.errors.append("VideoFileProcessor can not open video stream from file " + self.__filePath);
            return False;
        frames = self.__CountFrames();
        self.__fromFrame = min(self.__fromFrame, frames);
        if self.__toFrame == None:
            self.__toFrame = frames;
        else:
            self.__toFrame = min(self.__toFrame, frames);
        if self.__toFrame < self.__fromFrame:
            self.__toFrame = self.__fromFrame;
        return True;

    def __OpenSream(self):
        self.__videoStream = cv2.VideoCapture(self.__filePath);
        if self.__videoStream.isOpened() is False:
            conveyorResult.errors.append("VideoFileProcessor found that the stream is unexpectedly closed " + self.__filePath);
            return False;
        return True;

    def __CloseStream(self):
        if (self.__videoStream is not None and self.__videoStream.isOpened()):
            try:
                self.__videoStream.release();
            except:
                return False;
        return True;

    def __GetFrame(self, frame, conveyorResult):
        self.__videoStream.set(1, frame);
        ret, conveyorResult.image = self.__videoStream.read(1);
        print("get frame "+str(frame));
        return ret;
    
    def __CountFrames(self):
        return int(self.__videoStream.get(cv2.CAP_PROP_FRAME_COUNT));
