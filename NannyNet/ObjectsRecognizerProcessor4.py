# Model: openimages_v4/ssd/mobilenet_v2
# Use participated Tensorflow
from Processor import Processor
import Conveyor
import numpy as np
#import tensorflow as tf
import tensorflow_hub as hub

class ObjectsRecognizerProcessor(Processor):
    def __init__(self, **kwargs):
        self.tf = kwargs['tf'];
        self.tf.executing_eagerly()
        module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
        self._detector = hub.load(module_handle).signatures['default']
        self._session = self.tf.compat.v1.InteractiveSession()
        self._session.run(self.tf.compat.v1.tables_initializer(name='hub_input'))
        
    def ProcessInput(self, conveyorResult):
        tf = self.tf
        if (conveyorResult.image is not None):
            conveyorResult.image_converted = tf.image.convert_image_dtype(conveyorResult.image, tf.float32)[tf.newaxis, ...]
            # Perform the detection
            result = self._detector(conveyorResult.image_converted)
            for key,value in result.items():
                result[key] = value.eval()

            boxes = result["detection_boxes"]
            scores = result["detection_scores"] 
            classes = result["detection_class_entities"]
            num = len(scores)
            
            resultSave = {
                "boxes": boxes,
                "scores": scores,
                "classes": classes,
                "num_detections": num,
                "category_index": {}
            }
            conveyorResult.analyzers[self.__class__.__name__] = resultSave
        return True

    def Clean(self):
        self._session.close()
        return True

