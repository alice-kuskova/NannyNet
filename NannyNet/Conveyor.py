class Conveyor(object):
    def __init__(self, maxResultLength):
        self.__processor_list = []
        self.Result = None
        self.__maxResultlength = maxResultLength
        
    def AddProcessor(self, processor):
        self.__processor_list.append(processor)

    def Run(self):
        self.Result = None
        while self.Result == None or self.Result.ended is False:
            self.Result = ConveyorResult(self.Result, self.__maxResultlength)
            self.Result.ended = False
            for processor in self.__processor_list:
                try:
                    print("Start module: " + processor.__class__.__name__)
                    success = processor.ProcessInput(self.Result)
                except Exception as e:
                    self.Result.errors.append("Unknown error in " + processor.__class__.__name__ + ": " + str(e))
                    return False
                if success is False:
                    return False
                if self.Result.ended:
                    return True

    def Clean(self):
        cleanResult = True
        for processor in self.__processor_list:
            try:
                if (not processor.Clean()):
                    cleanResult = False
            except:
                if (self.Result == None):
                    self.Result = ConveyorResult()
                self.Result.errors.append("Unknown error in Clean procedure of " + processor.__class__.__name__)
                cleanResult = False
        return cleanResult


class ConveyorResult(object):
    def __init__(self, prevResult=None, maxResultLength=5):
        self.camId = None;
        self.dateTime = None;
        self.frameId = None;
        self.image = None;
        self.image_converted = None;
        self.analyzers = {};
        self.errors = [];
        self.ended = True;

        if (maxResultLength < 2):
            return;
        self.previous = prevResult;
        i = maxResultLength - 1;
        res = self;
        while (i > 0) and (res != None):
            i = i - 1;
            res = res.previous;
        if res != None:
            res.previous = None;
