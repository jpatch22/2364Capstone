from app.models.model import Model
import random
from app.Annotation import Annotation

class Test_Model(Model):
    def __init__(self):
        super().__init__()

    def supply_annotations(self, image_list):
        super().supply_annotations(image_list)
        annotations = []

        # Generate three random annotations
        for _ in range(3):
            x1 = random.randint(0, 500)
            y1 = random.randint(0, 500)
            size = random.randint(150, 350)  # Adjust the size range as needed
            x2 = min(x1 + size, 500)
            y2 = min(y1 + size, 500)

            funny_name = self.generate_funny_name()  # You can implement this method

            # Create an Annotation object and add it to the list
            annotation = Annotation(x1, y1, x2, y2, funny_name)
            annotations.append(annotation)

        return annotations

    def generate_funny_name(self):
        # Implement your logic to generate a funny name here
        funny_names = ["Supreme Leader", "Captain Chuckle", "Sir Gigglesworth", "Laughing Llama", "Joker McJokeface"]
        return random.choice(funny_names)

