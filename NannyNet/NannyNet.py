from Conveyor import Conveyor;
from VideoFileProcessor import VideoFileProcessor;
from ImageShowProcessor import ImageShowProcessor;
from ObjectsRecognizerProcessor import ObjectsRecognizerProcessor;

# Create conveyor with 5 previous results cache
conv = Conveyor(5);

# Add video -> frames processor
param = {"filePath":'testvideo.webm', 
         "fromFrame":0, "toFrame":-1, "frameStep":1};
proc = VideoFileProcessor(**param);
conv.AddProcessor(proc);

# Add objects recognizer processor
proc3 = ObjectsRecognizerProcessor();
conv.AddProcessor(proc3);

# Add show image processor previous processors results
proc2 = ImageShowProcessor();
conv.AddProcessor(proc2);

# Run conveyor
print("Start processing");
if conv.Run():
    print("End processing");
else:
    for err in conv.Result.errors:
        print(err);

# Run cleaning if some analyzers and processors need to close or clear resources like temporary files, databases etc
print("Start resource cleaning");
if conv.Clean():
    print("End cleaning");
else:
    for err in conv.Result.errors:
        print(err);
