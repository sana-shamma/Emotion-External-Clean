import re
import cv2
# import time
import base64
import asyncio
import threading
import numpy as np
# from .preprocessingFrame import PreprocessingFrame
from ..evaluationCriteria.criteriaFactory import CriteriaFactory


class Camera:
    def __init__(self, ID=None, camera_name=None, camera_URL=None, evaluation_criteria=None):

        self.__camera_ID = self.set_camera_ID(ID)
        self.__camera_name = self.set_camera_name(camera_name)
        self.__camera_URL = camera_URL
        self.__criteria_maker = CriteriaFactory()
        self.__evaluation_criteria = self.set_evaluation_criteria(evaluation_criteria)
        # self.__image_processor = PreprocessingFrame(0.5)
        # self.__last_analysis_time = time.time()

    """
    Sets the camera ID.

    Args:
        camera_ID (int): The ID of the camera.

    Raises:
        TypeError: If the camera ID is not an integer.

    Returns:
        int: The camera ID.
    """      
    def set_camera_ID(self, camera_ID):
        try:
            if not isinstance(camera_ID, int) and camera_ID is not None :
                raise TypeError("Invalid camera ID type. Expected string.")
            
            self.__camera_ID = camera_ID
            return self.__camera_ID
        except Exception as e:
            print(e)
            return False
        
    """
    Returns the camera ID.

    Returns:
        str: The camera ID.
    """
    def get_camera_ID(self):
        return self.__camera_ID
    

    """
    Sets the camera name.

    Args:
        camera_name (str): The name of the camera.

    Raises:
        TypeError: If the camera name is not a string.
        ValueError: If the camera name length exceeds 255 characters.

    Returns:
        str: The camera name.
    """

    def set_camera_name(self, camera_name):
        try:
            if not isinstance(camera_name, str) and camera_name is not None:
                raise TypeError("Invalid camera name type. Expected string.")

            if len(camera_name) > 255 and camera_name is not None:
                raise ValueError("Invalid camera name length. Maximum length is 255 characters.")

            self.__camera_name = camera_name
            return self.__camera_name
        except Exception as e:
            print(e)
            return False
        
    """
    Returns the camera name.

    Returns:
        str: The camera name.
    """         
    def get_camera_name(self):
        return self.__camera_name
    
    
    """
    Sets the camera URL.

    Args:
        camera_URL(str) : The URL of the camera. The URL of the camera. Must be in the format 'rtsp://<IP_ADDRESS>:<PORT>/<FILE_PATH>'.

    Raises:
        TypeError: If the camera URL is not a string.
        ValueError: If the camera URL does not match the specified format.

    Returns:
        str: The camera url.
    """
    def set_camera_URL(self, camera_URL):
        try:
            if not isinstance(camera_URL, str) and camera_URL is not None:
                raise TypeError("Invalid camera URL type. Expected string.")
            
            if camera_URL is not None:
                pattern = r'^rtsp:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\/.*$'
                if not re.match(pattern, camera_URL):
                    raise ValueError("Invalid camera URL format.")

            self.__camera_URL = camera_URL
            return self.__camera_URL
        except Exception as e:
            print(e)
            return False
    
    """
    Returns the camera URL.

    Returns:
        str: The camera URL.
    """
    def get_camera_URL(self):
        return self.__camera_URL
    
    """
    Sets the evaluation criteria for the camera.

    Args:
        evaluation_criteria (list): The list of string elements.

    Raises:
        TypeError: If the evaluation criteria is not a list .
    
    Returns:
        list(str): The camera criteria.
    """
    def set_evaluation_criteria(self, criteria_list):
        try:
            if not isinstance(criteria_list, list) and criteria_list is not None:
                raise TypeError("Invalid evaluation criteria type. Expected list.")

            self.__evaluation_criteria = criteria_list
            return self.__evaluation_criteria
        
        except Exception as e:
            print(e)
            return False
        
    """
    Returns the evaluation criteria for the camera.

    Returns:
        list(str) : The evaluation criteria.
    """
    def get_evaluation_criteria(self):
        return self.__evaluation_criteria
        
    """
    Generate frames from the camera's RTSP stream and perform streaming.

    Args:
        rtsp_url (str): The URL of the RTSP stream from which the frames will be generated.

    Yields:
        data (str): The base64-encoded JPEG frame.
    """
    
    async def generate_frame( self, rtsp_url):
        try:
            cap = cv2.VideoCapture(rtsp_url)

            while True:
                success, frame = await asyncio.get_event_loop().run_in_executor(None, cap.read)

                if not success:
                    break

                width = 400
                height = 400
                frame = cv2.resize(frame, (width, height))

                data = self.__stream_frame(frame)
                yield data

        except Exception as e:
            print(e)
            yield None

    
    """
    Perform analysis on frames from the camera.

    This function creates multiple threads to execute the detection logic for each evaluation criterion.
    Each criterion is processed in a separate thread to enable concurrent execution.

    Returns:
        None: This function does not return any value.

    Raises:
        Exception: If an error occurs during the processing of the camera frames.

    """

    async def analysis_frame(self):
        try:
            threads = []
            for criteria in self.__evaluation_criteria:
                criteria_object = self.__criteria_maker.createCriteria(criteria)
                thread = threading.Thread(target=criteria_object.detect, args=(self.get_camera_ID(), self.get_camera_URL()))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        except Exception as e:
            print("Error processing camera ID:", self.get_camera_ID(), e)
            return None
        
    
    """
    Convert a frame to JPEG format and encode it as base64.

    Args:
        frame (int []): The frame to be converted.

    Raises:
        TypeError: If the frame is not of type np.ndarray.
        Exception: If there is an error encoding the frame.

    Returns:
        str: The base64-encoded JPEG frame.
    """
    def __stream_frame( self, frame):
        try:
            if not isinstance(frame, np.ndarray):
                raise TypeError("Invalid frame type. Expected np.ndarray.")

            success, jpeg = cv2.imencode(".jpeg", frame)
            if not success:
                raise Exception("Error encoding frame.")

            frame_encoded = base64.b64encode(jpeg.tobytes()).decode("utf-8")
            return frame_encoded
        
        except Exception as e:
            print(e)
            return None