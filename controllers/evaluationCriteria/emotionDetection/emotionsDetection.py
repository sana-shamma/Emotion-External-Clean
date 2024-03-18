# from models.DB_management.DBFaced import DBFacade
# from ..criteriaDetectionBehavior.detectionBehavior import DetectionBehavior
# from .faceDetection import FaceDetection
# from ..emotionModel.emotionModel import EmotionModel
# from collections import defaultdict
# from inference.core.interfaces.camera.entities import VideoFrame
# from inference import InferencePipeline
# from datetime import datetime
# import threading

# class EmotionsDetection(DetectionBehavior):
#     def __init__(self):
#         self.__db_facade = DBFacade()
#         self.__emotion_predictor = EmotionModel()
#         self.DB_result = []
        

        
#     def detect_emotion(self,camera_url): 
#         self.__emotion_predictor.predict(camera_url)


#     def process_results(self, cameraID):
#         frames_result = []
#         combined_result = []
#         DB_result = []

#         while True:
#             if self.__emotion_predictor.results:
#                 face_id, emotion_result, emotion_score = self.__emotion_predictor.results.pop(0)
#                 frames_result.append({"id": face_id, "emotion": emotion_result, "score": emotion_score})
        
#             current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#             grouped_results = {}
#             if len(frames_result) > 30:
#                 for frame_result in frames_result:
#                     id = frame_result["id"]
#                     if id not in grouped_results:
#                         grouped_results[id] = []
#                     grouped_results[id].append(frame_result)
                
#                 frame_result = []

#                 for id, results in grouped_results.items():
#                     combined_result.append({"id": id, "emotion": self.__guess_emotion_with_weights(results)})
                
#                 grouped_results = {}

#                 emotion_count = []
#                 for entry in combined_result:
#                     emotion = entry["emotion"]
#                     found = False
#                     for item in emotion_count:
#                         if item["emotion"] == emotion:
#                             item["amount"] += 1
#                             found = True
#                             break
#                     if not found:
#                         emotion_count.append({"emotion": emotion, "amount": 1})

#                 combined_result = []

#                 for entry in emotion_count:
#                     emotion = entry["emotion"]
#                     amount = entry["amount"]
#                     DB_result.append({"cameraID": cameraID, "emotion": emotion,
#                                     "amount": amount, "time": current_time})
        
#                 emotion_count = []
           


#                 for result in DB_result:
#                     self.__db_facade.set_emotion_data(
#                         result["time"], result["emotion"], result["amount"], result["cameraID"])
#                 print("result in DB", DB_result)
#                 DB_result = []

#     def detect(self,cameraID,camera_url):
#         prediction_thread = threading.Thread(target=self.detect_emotion, args=(camera_url,))
#         results_thread = threading.Thread(target=self.process_results, args=(cameraID,))

#         prediction_thread.start()
#         results_thread.start()

#         prediction_thread.join()
#         results_thread.join()

#     def __guess_emotion_with_weights(self, emotion_results):
#         emotion_stats = defaultdict(lambda: {'total_score': 0, 'count': 0})

#         for result in emotion_results:
#             emotion = result['emotion']
#             score = result['score']
#             if emotion is not None and score is not None:
#                 emotion_stats[emotion]['total_score'] += score
#                 emotion_stats[emotion]['count'] += 1

#         weighted_emotions = {}
#         for emotion, stats in emotion_stats.items():
#             if stats['count'] > 0:
#                 weighted_score = stats['total_score'] / \
#                     stats['count']  # Weighted by the frequency
#                 weighted_emotions[emotion] = weighted_score

#         guessed_emotion = max(
#             weighted_emotions, key=weighted_emotions.get) if weighted_emotions else None
#         return guessed_emotion


from ..criteriaDetectionBehavior.detectionBehavior import DetectionBehavior
from ..emotionModel.emotionModel import EmotionModel
from collections import defaultdict
from inference.core.interfaces.camera.entities import VideoFrame
from datetime import datetime
import threading
import time 
class EmotionsDetection(DetectionBehavior):
    def __init__(self):
        super().__init__()
        self.model = EmotionModel()
        self.DB_result = []
        

        
    def detect_emotion(self,camera_url): 
        self.model.predict(camera_url)

    
    def process_results(self, cameraID):
        frames_result = []
        combined_result = []
        DB_result = []

        while True:
            
            if len(self.model.results) >= 120:
                print("detect prossing for id", cameraID)

                for i in range(len(self.model.results)):
                    face_id, emotion_result, emotion_score = self.model.results[i]
                    frames_result.append({"id": face_id, "emotion": emotion_result, "score": emotion_score})
            
                current_time = time.time()

                self.model.last_predication_time  = current_time

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                grouped_results = {}
                # if len(frames_result) > 30:
                for frame_result in frames_result:
                    id = frame_result["id"]
                    if id not in grouped_results:
                        grouped_results[id] = []
                    grouped_results[id].append(frame_result)
                
                frame_result = []

                for id, results in grouped_results.items():
                    combined_result.append({"id": id, "emotion": self.__guess_emotion_with_weights(results)})
                
                grouped_results = {}

                emotion_count = []
                for entry in combined_result:
                    emotion = entry["emotion"]
                    found = False
                    for item in emotion_count:
                        if item["emotion"] == emotion:
                            item["amount"] += 1
                            found = True
                            break
                    if not found:
                        emotion_count.append({"emotion": emotion, "amount": 1})

                combined_result = []

                for entry in emotion_count:
                    emotion = entry["emotion"]
                    amount = entry["amount"]
                    DB_result.append({"cameraID": cameraID, "emotion": emotion,
                                    "amount": amount, "time": current_time})
        
                emotion_count = []
        

                for result in DB_result:
                    self.db_facade.set_emotion_data(
                        result["time"], result["emotion"], result["amount"], result["cameraID"])
                print("result in DB", DB_result)
                DB_result = []


    def detect(self,cameraID,camera_url):
        prediction_thread = threading.Thread(target=self.detect_emotion, args=(camera_url,))
        results_thread = threading.Thread(target=self.process_results, args=(cameraID,))

        prediction_thread.start()
        results_thread.start()

        prediction_thread.join()
        results_thread.join()

    def __guess_emotion_with_weights(self, emotion_results):
        emotion_stats = defaultdict(lambda: {'total_score': 0, 'count': 0})

        for result in emotion_results:
            emotion = result['emotion']
            score = result['score']
            if emotion is not None and score is not None:
                emotion_stats[emotion]['total_score'] += score
                emotion_stats[emotion]['count'] += 1

        weighted_emotions = {}
        for emotion, stats in emotion_stats.items():
            if stats['count'] > 0:
                weighted_score = stats['total_score'] / \
                    stats['count']  # Weighted by the frequency
                weighted_emotions[emotion] = weighted_score

        guessed_emotion = max(
            weighted_emotions, key=weighted_emotions.get) if weighted_emotions else None
        return guessed_emotion
