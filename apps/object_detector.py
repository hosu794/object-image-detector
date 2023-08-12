import os
import cv2

from typing import List, Sequence, Any
from dataclasses import dataclass
from cv2.dnn import Net
from django.conf import settings
from settings.local import CLASSES_FILE_NAME

import numpy as np


@dataclass
class ImageDetectionLabelResult:
    name: str
    confidence: float
    x: int
    y: int


class ImageObjectDetectorTask:
    CONFIDENCE_THRESHOLD: float = 0.5
    CONFIDENCE_INDEX: int = 4
    CLASSIFICATION_RESULT_INDEX: int = 5
    BOX_INFO_END_INDEX = 4
    DETECTION_CLASSES: str = CLASSES_FILE_NAME

    @staticmethod
    def process(image_bytes: bytes) -> list[ImageDetectionLabelResult]:
        """
        Process the given image bytes to detect objects using YOLOv3.

        Parameters:
            image_bytes (bytes): The image data in bytes format.

        Returns:
            List[ImageDetectionLabelResult]: A list of dictionaries containing detected object labels and their coordinates.
        """

        classes: List[str] = ImageObjectDetectorTask.__get_classes_from_file()

        image: np.ndarray = ImageObjectDetectorTask.__retrieve_image_from_bytes(image_bytes)

        height, width, _ = image.shape

        blob: np.ndarray = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)

        outputs: Sequence | Sequence[cv2.UMat] = ImageObjectDetectorTask.__perform_detection(blob)

        return ImageObjectDetectorTask.__read_labels_from_outputs(classes, height, outputs, width)

    @staticmethod
    def __get_classes_from_file() -> List[str]:
        with open(os.path.join(settings.BASE_DIR, ImageObjectDetectorTask.DETECTION_CLASSES), "r") as f:
            classes = [line.strip() for line in f.readlines()]
        return classes

    @staticmethod
    def __read_labels_from_outputs(classes: List[str], height: float, outputs: Sequence | Sequence[cv2.UMat],
                                   width: float) -> List[ImageDetectionLabelResult]:

        labels_array: List[ImageDetectionLabelResult] = []

        for output in outputs:
            for detection in output:

                scores: np.ndarray = detection[ImageObjectDetectorTask.CLASSIFICATION_RESULT_INDEX:]
                scores_without_one_dimensional_dimensions: np.ndarray = np.squeeze(scores)
                class_id_with_max_probability: Any = np.argmax(scores_without_one_dimensional_dimensions)
                confidence = detection[ImageObjectDetectorTask.CONFIDENCE_INDEX]

                if confidence > ImageObjectDetectorTask.CONFIDENCE_THRESHOLD:
                    x, y = ImageObjectDetectorTask.__create_cord_result(detection, height, width)
                    labels_array.append(ImageDetectionLabelResult(classes[class_id_with_max_probability],
                                                                  float(confidence), x, y))

        return labels_array

    @staticmethod
    def __create_cord_result(detection, height: int, width: int) -> tuple[int, int]:
        box: np.ndarray = detection[:ImageObjectDetectorTask.BOX_INFO_END_INDEX] * np.array(
            [width, height, width, height])
        (center_x, center_y, box_width, box_height) = box.astype("int")
        x: int = int(center_x - (box_width / 2))
        y: int = int(center_y - (box_height / 2))
        return x, y

    @staticmethod
    def __retrieve_image_from_bytes(image_bytes) -> np.ndarray:
        numpy_array_from_image_bytes: np.ndarray = np.frombuffer(image_bytes, np.uint8)
        return cv2.imdecode(numpy_array_from_image_bytes, cv2.IMREAD_COLOR)

    @staticmethod
    def __perform_detection(blob: np.ndarray) -> Sequence | Sequence[cv2.UMat]:

        network: Net = cv2.dnn.readNetFromDarknet("yolov3.cfg", "yolov3.weights")
        network.setInput(blob)
        layer_names: Sequence[str] = network.getLayerNames()
        output_layers: List[Sequence[int]] = [layer_names[i - 1] for i in network.getUnconnectedOutLayers()]
        return network.forward(output_layers)
