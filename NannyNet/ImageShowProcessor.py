from Processor import Processor
import Conveyor
import cv2;
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import numpy as np

LINE_THICKNESS = 2
MIN_SCORE = 0.12

class ImageShowProcessor(Processor):
    def __init__(self, **kwargs):
        cv2.startWindowThread()
        cv2.namedWindow("Preview")
        

    def ProcessInput(self, conveyorResult):
        if (conveyorResult.image is not None):
           image_copy = conveyorResult.image.copy();
           vis_util.visualize_boxes_and_labels_on_image_array(
                image_copy,
                np.squeeze(conveyorResult.analyzers['ObjectsRecognizerProcessor']['boxes']),
                np.squeeze(conveyorResult.analyzers['ObjectsRecognizerProcessor']['classes']).astype(np.int32),
                np.squeeze(conveyorResult.analyzers['ObjectsRecognizerProcessor']['scores']),
                conveyorResult.analyzers['ObjectsRecognizerProcessor']['category_index'],
                use_normalized_coordinates=True,
                line_thickness=LINE_THICKNESS,
                min_score_thresh=MIN_SCORE
           )
           cv2.imshow('Preview', image_copy)
           if cv2.waitKey(1) == ord('q'):
               conveyorResult.ended = True
        return True

    def Clean(self):
        cv2.destroyAllWindows()
        return True
