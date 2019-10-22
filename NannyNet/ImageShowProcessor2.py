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

MAX_BOXES = 20
MIN_SCORE = 0.12

class ImageShowProcessor(Processor):
    def __init__(self, **kwargs):
        cv2.startWindowThread()
        cv2.namedWindow("Preview")
        
    def ProcessInput(self, conveyorResult):
        if (conveyorResult.image is not None):
           image_copy = conveyorResult.image.copy()
           
           image_boxes = self._draw_boxes(
               conveyorResult.image, 
               conveyorResult.analyzers['ObjectsRecognizerProcessor']['boxes'],
               conveyorResult.analyzers['ObjectsRecognizerProcessor']['classes'],
               conveyorResult.analyzers['ObjectsRecognizerProcessor']['scores'],
               max_boxes=MAX_BOXES, min_score=MIN_SCORE)

           self._display_image(image_boxes, conveyorResult)
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
            

    def _draw_bounding_box_on_image(self, image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
          draw = ImageDraw.Draw(image)
          im_width, im_height = image.size
          (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                        ymin * im_height, ymax * im_height)
          draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
                     (left, top)],
                    width=thickness,
                    fill=color)

          # If the total height of the display strings added to the top of the bounding
          # box exceeds the top of the image, stack the strings below the bounding box
          # instead of above.
          display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
          # Each display_str has a top and bottom margin of 0.05x.
          total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

          if top > total_display_str_height:
              text_bottom = top
          else:
              text_bottom = bottom + total_display_str_height
          # Reverse list and print from bottom to top.
          for display_str in display_str_list[::-1]:
              text_width, text_height = font.getsize(display_str)
              margin = np.ceil(0.05 * text_height)
              draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                              (left + text_width, text_bottom)],
                              fill=color)
              draw.text((left + margin, text_bottom - text_height - margin),
                          display_str,
                          fill="black",
                          font=font)
              text_bottom -= text_height - 2 * margin


    def _draw_boxes(self, image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
        """Overlay labeled boxes on an image with formatted scores and label names."""
        colors = list(ImageColor.colormap.values())

        font = ImageFont.load_default()
        image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
        for i in range(min(boxes.shape[0], max_boxes)):
            if scores[i] >= min_score:
                ymin, xmin, ymax, xmax = tuple(boxes[i])
                display_str = "{}: {}%".format(class_names[i].decode("ascii"),
                                                int(100 * scores[i]))
                color = colors[hash(class_names[i]) % len(colors)]
                self._draw_bounding_box_on_image(
                    image_pil,
                    ymin,
                    xmin,
                    ymax,
                    xmax,
                    color,
                    font,
                    display_str_list=[display_str])
        return np.array(image_pil)