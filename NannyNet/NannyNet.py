from Conveyor import Conveyor
from VideoFileProcessor import VideoFileProcessor
from PersonPoseRecognizerProcessor2 import PersonPoseRecognizerProcessor
from DrawPosesProcessor import DrawPosesProcessor
from DrawObjectsProcessor import DrawObjectsProcessor
from ObjectsRecognizerProcessor4 import ObjectsRecognizerProcessor
from ImageShowProcessor import ImageShowProcessor
import tensorflow as tf1
import tensorflow as tf2


# Create conveyor with 5 previous results cache
conv = Conveyor(5)

# Add video -> frames processor
param = {"filePath":'demo_source_video.webm', 
         "fromFrame":200, "toFrame":-1, "frameStep":4}
proc = VideoFileProcessor(**param)
conv.AddProcessor(proc)

# Add object classification
param = {"tf":tf1}
proc2 = ObjectsRecognizerProcessor(**param)
conv.AddProcessor(proc2)


# Add human's pose recognizer processor
param = {"tf":tf2}
proc5 = PersonPoseRecognizerProcessor(**param)
conv.AddProcessor(proc5)

# Add human's poses draw
proc6 = DrawPosesProcessor()
conv.AddProcessor(proc6)

# Add objects draw
proc7 = DrawObjectsProcessor()
conv.AddProcessor(proc7)

# Show result image processor
proc9 = ImageShowProcessor()
conv.AddProcessor(proc9)


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
