from ..detectionModelAdaptor.detectionModelAdaptor import DetectionModelAdaptor
from models.DB_management.DBFaced import DBFacade

class DetectionBehavior:

    def __init__(self):
        self.db_facade = DBFacade()
        self.model = None

    """
    Perform detection using the assigned model on frames from the specified camera.

    Args:
        camera_ID (str): The ID of the camera.
        camera_url (str): The URL of the camera feed.

    Returns:
        None

    """
    def detect(self, camera_ID, camera_url):
        pass