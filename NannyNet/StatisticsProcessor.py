from Processor import Processor
import Conveyor

MIN_SCORE = 0.12

class StatisticsProcessor(Processor):
    def __init__(self, **kwargs):
        self._found_objects = set()

    def ProcessInput(self, conveyorResult):
        result = conveyorResult.analyzers['ObjectsRecognizerProcessor']
        for i in range(result['num_detections']):
            if result['scores'][i] >= MIN_SCORE:
                self._found_objects = self._found_objects | set(result['classes'])
        return True

    def Clean(self):
        print("Found objects:")
        print(self._found_objects)
        return True

