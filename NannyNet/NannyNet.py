from Conveyor import Conveyor;
from VideoFileProcessor import VideoFileProcessor;
from ImageShowProcessor import ImageShowProcessor;

conv = Conveyor(5);
param = {"filePath":'D:\\ai\\NannyNet\\test_images\\Голый романтик_2019_WEB-DLRip.avi', 
         "fromFrame":1, "toFrame":1000, "frameStep":2};
proc = VideoFileProcessor(**param);
conv.AddProcessor(proc);

proc2 = ImageShowProcessor();
conv.AddProcessor(proc2);

print("Start processing");
if conv.Run():
    print("End processing");
else:
    for err in conv.Result.errors:
        print(err);


print("Start resource cleaning");
if conv.Clean():
    print("End cleaning");
else:
    for err in conv.Result.errors:
        print(err);
