# from inference.core.interfaces.camera.entities import VideoFrame
# from inference import InferencePipeline

# class ServicesHandler:
#     def __init__(self):
#         self.results = []  

#     """
#     Process the predictions from the emotion detection model and store the results.

#     Args:
#         predictions (dict): A dictionary containing the emotion predictions from the model.
#         video_frame (VideoFrame): The video frame associated with the predictions.

#     Returns:
#         None

#     Side Effects:
#         Modifies the `results` list attribute of the ServicesHandler instance.

#     Description:
#         This method takes the predictions from the emotion detection model and extracts the emotion labels and confidence scores. It then iterates over each label-confidence pair, assigns a unique face ID, and appends the face ID, emotion label, and confidence score as a tuple to the `results` list attribute of the ServicesHandler instance. The method does not return any value explicitly.

#     """
#     def my_custom_sink(self, predictions: dict, video_frame: VideoFrame):
#         labels_confidence = [(p["class"], p["confidence"]) for p in predictions["predictions"]]
#         if labels_confidence:
#             for id, label_confidence in enumerate(labels_confidence):
#                 emotion_result = label_confidence[0]
#                 emotion_score = label_confidence[1]
#                 face_id = id
#                 self.results.append((face_id, emotion_result, emotion_score))

#         """
#         Handle emotion prediction for a given camera URL using an emotion detection model.

#         Args:
#             camera_url (str): The URL of the camera feed.

#         Returns:
#             None
#         """
#     def handle_emotion_predict(self, camera_url):
#         pipeline = InferencePipeline.init(
#             model_id="emotion-detection-cwq4g/1",
#             api_key="CL44RJt0AHwiczZPxMLN",
#             video_reference=camera_url,
#             on_prediction=lambda predictions, video_frame: self.my_custom_sink(predictions, video_frame),
#         )
#         pipeline.start()
#         pipeline.join()

   


from inference.core.interfaces.camera.entities import VideoFrame
from inference import InferencePipeline
import time
import threading
class ServicesHandler:
    def __init__(self):
        self.results = []
        self.last_analysis_time = time.time()
        self.__frame_count = 0

    """
    This method takes the predictions from the emotion detection model and extracts the emotion
    labels and confidence scores. It then iterates over each label-confidence pair, assigns a 
    unique face ID, and appends the face ID, emotion label, and confidence score as a tuple 
    to the `results` list attribute of the ServicesHandler instance. 

    Args:
        predictions (dict): A dictionary containing the emotion predictions from the model.
        video_frame (VideoFrame): The video frame associated with the predictions.

    Returns:
        None
    """
    def custom_emotion_prediction_result(self, predictions: dict, video_frame: VideoFrame):
        
        current_time = time.time()


        if current_time - self.last_analysis_time >= 40:
            print("pass 40" )

            labels_confidence = [(p["class"], p["confidence"]) for p in predictions["predictions"]]
            if labels_confidence:
                for id, label_confidence in enumerate(labels_confidence):
                    emotion_result = label_confidence[0]
                    emotion_score = label_confidence[1]
                    face_id = id
                    self.results.append((face_id, emotion_result, emotion_score))
                    self.__frame_count += 1

            print("count", self.__frame_count)

            if self.__frame_count == 120:
                print("get 120" )
                self.__frame_count = 0
                self.results = []


        """
        Handle emotion prediction for a given camera URL using an emotion detection model.

        Args:
            camera_url (str): The URL of the camera feed.

        Returns:
            None
        """
    def handle_emotion_predict(self, camera_url):

        pipeline = InferencePipeline.init(
            model_id="emotion-detection-cwq4g/1",
            api_key="CL44RJt0AHwiczZPxMLN",
            video_reference=camera_url,
            on_prediction=lambda predictions, video_frame: self.custom_emotion_prediction_result(predictions, video_frame),
        )
        pipeline.start()
        pipeline.join()

   