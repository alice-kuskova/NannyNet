from Conveyor import Conveyor
from VideoFileProcessor import VideoFileProcessor
from PersonPoseRecognizerProcessor import PersonPoseRecognizerProcessor
from PersonPoseDrawProcessor import PersonPoseDrawProcessor
from ImageShowPoseDrawProcessor import ImageShowPoseDrawProcessor

# Create conveyor with 5 previous results cache
conv = Conveyor(5)

# Add video -> frames processor
param = {"filePath":'demo_source_video.webm', 
         "fromFrame":100, "toFrame":-1, "frameStep":4}
proc = VideoFileProcessor(**param)
conv.AddProcessor(proc)

# Add human's pose recognizer processor
proc5 = PersonPoseRecognizerProcessor()
conv.AddProcessor(proc5)

# Add human's poses draw
proc6 = PersonPoseDrawProcessor()
conv.AddProcessor(proc6)

# Add show image processor previous processors results
proc7 = ImageShowPoseDrawProcessor()
conv.AddProcessor(proc7)


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
