from Processor import Processor
import Conveyor
import numpy as np
import tensorflow as tf
import os
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


class ObjectsRecognizerProcessor(Processor):
    def __init__(self, **kwargs):
        # Get current working directory
        CWD_PATH = os.getcwd()
        RESEARCH_PATH = os.path.join(CWD_PATH, "tensorflow", "models", "research")
        MODEL_NAME = 'ssd_inception_v2_coco_2018_01_28'
        # Path to frozen detection graph .pb file
        PATH_TO_CKPT = os.path.join(RESEARCH_PATH, MODEL_NAME, 'frozen_inference_graph.pb')
        # Path to label map file
        PATH_TO_LABELS = os.path.join(RESEARCH_PATH,'object_detection', 'data', 'mscoco_label_map.pbtxt')
        # Max number of classes the object detector can identify
        NUM_CLASSES = 10000

        ## Load the label map.
        # Label maps map indices to category names, so that when our convolution
        # network predicts `5`, we know that this corresponds to `king`.
        # Here we use internal utility functions, but anything that returns a
        # dictionary mapping integers to appropriate string labels would be fine
        self._label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        self._categories = label_map_util.convert_label_map_to_categories(self._label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        self._category_index = label_map_util.create_category_index(self._categories)

        # Load the Tensorflow model into memory.
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            self._sess = tf.Session(graph=detection_graph)


        # Define input and output tensors (i.e. data) for the object detection classifier

        # Input tensor is the image
        self._image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

        # Output tensors are the detection boxes, scores, and classes
        # Each box represents a part of the image where a particular object was detected
        self._detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

        # Each score represents level of confidence for each of the objects.
        # The score is shown on the result image, together with the class label.
        self._detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        self._detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

        # Number of objects detected
        self._num_detections = detection_graph.get_tensor_by_name('num_detections:0')


    def ProcessInput(self, conveyorResult):
        if (conveyorResult.image is not None):
            conveyorResult.image_converted = np.expand_dims(conveyorResult.image, axis=0)
            # Perform the detection
            (boxes, scores, classes, num) = self._sess.run(
                [self._detection_boxes, self._detection_scores, self._detection_classes, self._num_detections],
                feed_dict={self._image_tensor: conveyorResult.image_converted})
            result = {
                "boxes": boxes,
                "scores": scores,
                "classes": classes,
                "num_detections": num,
                "category_index": self._category_index
            }
            conveyorResult.analyzers[self.__class__.__name__] = result
        return True;

    def Clean(self):
        return True;

