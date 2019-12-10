from Conveyor import Conveyor
from VideoFileProcessor import VideoFileProcessor

#from ImageShowProcessor import ImageShowProcessor #compatible with ObjectsRecognizerProcessor
from ImageShowProcessor2 import ImageShowProcessor #compatible with ObjectsRecognizerProcessor2 and 3

#from ObjectsRecognizerProcessor import ObjectsRecognizerProcessor #extremally fast but low quality
from ObjectsRecognizerProcessor2 import ObjectsRecognizerProcessor #golden middle
#from ObjectsRecognizerProcessor3 import ObjectsRecognizerProcessor #extremally slow but high quality

from StatisticsProcessor import StatisticsProcessor

import tensorflow as tf
tf.compat.v1.enable_eager_execution()

# Create conveyor with 5 previous results cache
conv = Conveyor(5)

# Add video -> frames processor

#first video
param = {"filePath":'demo_source_video.webm', 
         "fromFrame":100, "toFrame":-1, "frameStep":3}

#second video
#param = {"filePath":'demo_source_2.mp4', 
#         "fromFrame":0, "toFrame":-1, "frameStep":3}

proc = VideoFileProcessor(**param)
conv.AddProcessor(proc)

# Add objects recognizer processor
proc2 = ObjectsRecognizerProcessor()
conv.AddProcessor(proc2)

# Add show image processor previous processors results
proc3 = ImageShowProcessor()
conv.AddProcessor(proc3)

# Show found objects list
proc4 = StatisticsProcessor()
conv.AddProcessor(proc4)

# Run conveyor
print("Start processing")
if conv.Run():
    print("End processing")
else:
    for err in conv.Result.errors:
        print(err)

# Run cleaning if some analyzers and processors need to finalize, close or clear resources like temporary files, databases etc
print("Start resource cleaning")
if conv.Clean():
    print("End cleaning")
else:
    for err in conv.Result.errors:
        print(err)
