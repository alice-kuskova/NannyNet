# Model: cmu
from Processor import Processor
import Conveyor
import os
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

class PersonPoseRecognizerProcessor(Processor):
    def __init__(self, **kwargs):
        self._MODEL_NAME = 'mobilenet_v2_small'
        self._detector = None

    def ProcessInput(self, conveyorResult):
        if (conveyorResult.image is not None):
            if (self._detector == None):
                self._detector = TfPoseEstimator(get_graph_path(self._MODEL_NAME), target_size=(432,368))
            humans = self._detector.inference(conveyorResult.image)
            conveyorResult.image = TfPoseEstimator.draw_humans(conveyorResult.image, humans, imgcopy=False)
            resultSave = {
                "humans": humans,
            }
            conveyorResult.analyzers[self.__class__.__name__] = resultSave
        return True

    def Clean(self):
        return True

