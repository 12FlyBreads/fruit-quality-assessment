# camera.py
from picamera2 import Picamera2
import threading
import time
import io
from utils import RESOLUTION

class Camera:
    def __init__(self, resolution=RESOLUTION) -> None:
        """
        Initialize the camera with the given resolution.
        :param resolution: Tuple (width, height)
        :return: None
        """

        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(
            main={"size": resolution}
        )
        self.picam2.configure(config)
        self.frame = None
        self.frame_lock = threading.Lock()

        print("Initializing Camera...")
        self.picam2.start()
        time.sleep(2.0)
        print("CCamera ready.")

        # Start the frame grab thread
        self.capture_thread = threading.Thread(target=self._frame_grab_thread,
                                               daemon=True)
        self.capture_thread.start()

    def _frame_grab_thread(self) -> None:
        """
        Internal thread that continuously captures frames from the camera.
        :return: None
        """
        while True:
            stream = io.BytesIO()
            # Capture in JPEG format directly
            self.picam2.capture_file(stream, format='jpeg')
            
            with self.frame_lock:
                self.frame = stream.getvalue()

            # Control the capture rate
            time.sleep(1/15) # ~15 FPS

    def get_jpeg_frame(self) -> bytes | None:
        """
        Returns the last captured JPEG frame.
        :return: JPEG byte data or None if no frame is available
        """
        with self.frame_lock:
            if self.frame is not None:
                return self.frame
            return None

    def stream_generator(self) -> None:
        """
        Generator for Flask streaming (multipart).
        """
        while True:
            with self.frame_lock:
                if self.frame is None:
                    continue
                frame_copy = self.frame
            
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_copy + b'\r\n'
            )
            # Reduce sleep time for smoother streaming
            time.sleep(1/30)

    def stop(self) -> None:
        """ Stop the camera. """
        print("Stopping camera.")
        self.picam2.stop()
        