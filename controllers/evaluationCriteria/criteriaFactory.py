from .dressCodeDetection.uniformDetection import UniformDetection
from .emotionDetection.emotionsDetection import EmotionsDetection

class CriteriaFactory:
    
    """
    Create a criteria object based on the given criteria name.

    Args:
        criteriaName (str): The name of the criteria.

    Returns:
        object: An instance of the criteria object based on the given criteria name.
    """
     
    def createCriteria(self,criteriaName):
        if criteriaName == "emotion":
            return EmotionsDetection()

        elif criteriaName == "uniform":
            return UniformDetection()
