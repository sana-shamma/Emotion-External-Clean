# from ..detectionModelAdaptor.detectionModelAdaptor import DetectionModelAdaptor
# from ...servicesHandler.servicesHandler import ServicesHandler
# import threading

# class EmotionModel(DetectionModelAdaptor):

#     def __init__(self):
#         self.__services_handler = ServicesHandler()
#         self.results = [] 


#     def run_emotion_model(self,camera_url):
#         self.__services_handler.handle_emotion_predict(camera_url)

#     def custom_emotion_predication_results(self):
#         while True:
#             if self.__services_handler.results:
#                 face_id, emotion_result, emotion_score = self.__services_handler.results.pop(0)
#                 self.results.append((face_id, emotion_result, emotion_score))

#     def predict(self, camera_url):
#         prediction_thread = threading.Thread(target=self.run_emotion_model, args=(camera_url,))
#         results_thread = threading.Thread(target=self.custom_emotion_predication_results)

#         prediction_thread.start()
#         results_thread.start()

#         prediction_thread.join()
#         results_thread.join()


from ..detectionModelAdaptor.detectionModelAdaptor import DetectionModelAdaptor
from ...servicesHandler.servicesHandler import ServicesHandler
import threading
import time

class EmotionModel(DetectionModelAdaptor):

    def __init__(self):
        super().__init__()
        self.results = []
        self.last_predication_time = None
        self.lock = threading.Lock() 


    """
    Run the emotion detection model on the specified camera URL.

    Args:
        camera_url (str): The URL of the camera feed.

    Returns:
        None
    """
    def run_emotion_model(self,camera_url):
        self.services_handler.handle_emotion_predict(camera_url)

    """
    Process the custom emotion prediction results.

    Returns:
        None
    """
    def custom_emotion_predication_results(self):
        while True:

            if len(self.services_handler.results) >= 120 :
                print("predication processing")
                for i in range(len(self.services_handler.results)):
                    face_id, emotion_result, emotion_score = self.services_handler.results[i]
                    self.results.append((face_id, emotion_result, emotion_score))


            if  self.last_predication_time :
                self.services_handler.last_analysis_time = self.last_predication_time
                self.last_predication_time = None

    """
    Perform emotion prediction on the specified camera URL.

    Args:
        camera_url (str): The URL of the camera feed.

    Returns:
        None
    """
    def predict(self, camera_url):
        prediction_thread = threading.Thread(target=self.run_emotion_model, args=(camera_url,))
        results_thread = threading.Thread(target=self.custom_emotion_predication_results)

        prediction_thread.start()
        results_thread.start()

        prediction_thread.join()
        results_thread.join()
