# Model: openimages_v4/ssd/mobilenet_v2
from Processor import Processor
import Conveyor
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

class ObjectsRecognizerProcessor(Processor):
    def __init__(self, **kwargs):
        module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
        self._detector = hub.load(module_handle).signatures['default']

    def ProcessInput(self, conveyorResult):
        if (conveyorResult.image is not None):
            conveyorResult.image_converted = tf.image.convert_image_dtype(conveyorResult.image, tf.float32)[tf.newaxis, ...]
            # Perform the detection
            result = self._detector(conveyorResult.image_converted)
            result = {key:value.numpy() for key,value in result.items()}
            
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
        return True

