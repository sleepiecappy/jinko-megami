from typing import Callable, Tuple

import cv2


class Camera:
    def __init__(
        self,
        on_frame: Callable[[bytes], None],
        resolution: Tuple[int, int] = (860, 480),
        fps: int = 15,
        debug: bool = False,
    ):
        self.on_frame = on_frame
        self.resolution = resolution
        self.fps = fps
        self.debug = debug

    def read(self):
        """Capture the image feed from the camera."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Could not open camera")

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        cap.set(cv2.CAP_PROP_FPS, self.fps)

        while True:
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("Failed to read from camera")

            # Process the frame (e.g., convert to bytes)
            frame_bytes = frame.tobytes()
            # Call the on_frame callback with the processed frame
            self.on_frame(frame_bytes)

            if self.debug:
                cv2.imshow("Camera Feed", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
