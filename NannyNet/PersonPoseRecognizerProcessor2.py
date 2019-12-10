from Processor import Processor
import Conveyor
import os
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

class PersonPoseRecognizerProcessor(Processor):
    def __init__(self, **kwargs):
        self.tf = kwargs['tf']
        self._MODEL_NAME = 'mobilenet_thin' 
        #'cmu'
        self._detector = TfPoseEstimator(get_graph_path(self._MODEL_NAME))
        

    def ProcessInput(self, conveyorResult):
        tf = self.tf
        if (conveyorResult.image is not None):
            humans = self._detector.inference(conveyorResult.image, resize_to_default=True, upsample_size=2)
            #conveyorResult.image = TfPoseEstimator.draw_humans(conveyorResult.image, humans, imgcopy=False)
            resultSave = {
                "humans": humans,
            }
            conveyorResult.analyzers[self.__class__.__name__] = resultSave
        return True

    def Clean(self):
        return True

