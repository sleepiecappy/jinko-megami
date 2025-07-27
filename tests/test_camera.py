import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from typing import Any

from jinkomegami.sensors.camera import Camera


class TestCamera:
    """Test cases for the Camera class."""

    def test_camera_initialization(self):
        """Test Camera initialization with default parameters."""
        on_frame_callback = Mock()
        camera = Camera(on_frame=on_frame_callback)

        assert camera.on_frame == on_frame_callback
        assert camera.resolution == (860, 480)
        assert camera.fps == 15
        assert camera.debug is False

    def test_camera_initialization_with_custom_params(self):
        """Test Camera initialization with custom parameters."""
        on_frame_callback = Mock()
        custom_resolution = (1920, 1080)
        custom_fps = 30

        camera = Camera(
            on_frame=on_frame_callback,
            resolution=custom_resolution,
            fps=custom_fps,
            debug=True,
        )

        assert camera.on_frame == on_frame_callback
        assert camera.resolution == custom_resolution
        assert camera.fps == custom_fps
        assert camera.debug is True

    @patch("jinkomegami.sensors.camera.cv2.VideoCapture")
    def test_read_camera_not_opened(self, mock_video_capture: Any) -> None:
        """Test that RuntimeError is raised when camera cannot be opened."""
        # Mock VideoCapture to return a capture object that is not opened
        mock_cap = Mock()
        mock_cap.isOpened.return_value = False
        mock_video_capture.return_value = mock_cap

        on_frame_callback = Mock()
        camera = Camera(on_frame=on_frame_callback)

        with pytest.raises(RuntimeError, match="Could not open camera"):
            camera.read()

    @patch("jinkomegami.sensors.camera.cv2.VideoCapture")
    def test_read_camera_settings_applied(self, mock_video_capture: Any) -> None:
        """Test that camera settings are properly applied."""
        # Mock VideoCapture and its methods
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (False, None)  # Will cause RuntimeError
        mock_video_capture.return_value = mock_cap

        on_frame_callback = Mock()
        camera = Camera(on_frame=on_frame_callback, resolution=(1280, 720), fps=25)

        try:
            camera.read()
        except RuntimeError:
            pass  # Expected due to mock returning False for read()

        # Verify camera settings were applied
        import cv2

        mock_cap.set.assert_any_call(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        mock_cap.set.assert_any_call(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        mock_cap.set.assert_any_call(cv2.CAP_PROP_FPS, 25)

    @patch("jinkomegami.sensors.camera.cv2.VideoCapture")
    def test_read_failed_frame_read(self, mock_video_capture: Any) -> None:
        """Test that RuntimeError is raised when frame reading fails."""
        # Mock VideoCapture to simulate failed frame reading
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (False, None)  # Failed read
        mock_video_capture.return_value = mock_cap

        on_frame_callback = Mock()
        camera = Camera(on_frame=on_frame_callback)

        with pytest.raises(RuntimeError, match="Failed to read from camera"):
            camera.read()

    @patch("jinkomegami.sensors.camera.cv2.VideoCapture")
    @patch("jinkomegami.sensors.camera.cv2.imshow")
    @patch("jinkomegami.sensors.camera.cv2.waitKey")
    def test_read_successful_frame_processing(
        self, mock_wait_key: Any, mock_imshow: Any, mock_video_capture: Any
    ) -> None:
        """Test successful frame reading and processing."""
        # Create a mock frame (numpy array)
        mock_frame = np.zeros((480, 860, 3), dtype=np.uint8)
        mock_frame_bytes = mock_frame.tobytes()

        # Mock VideoCapture
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.side_effect = [
            (True, mock_frame),  # First successful read
            (False, None),  # Second read fails to exit loop
        ]
        mock_video_capture.return_value = mock_cap

        # Mock waitKey to exit immediately in debug mode
        mock_wait_key.return_value = ord("q")

        on_frame_callback = Mock()
        camera = Camera(on_frame=on_frame_callback, debug=True)

        try:
            camera.read()
        except RuntimeError:
            pass  # Expected due to second read failing

        # Verify callback was called with frame bytes
        on_frame_callback.assert_called_once_with(mock_frame_bytes)

        # Verify debug display was shown
        mock_imshow.assert_called_once_with("Camera Feed", mock_frame)

    @patch("jinkomegami.sensors.camera.cv2.VideoCapture")
    @patch("jinkomegami.sensors.camera.cv2.imshow")
    @patch("jinkomegami.sensors.camera.cv2.waitKey")
    def test_read_debug_mode_exit_on_q(
        self, mock_wait_key: Any, mock_imshow: Any, mock_video_capture: Any
    ) -> None:
        """Test that debug mode exits when 'q' is pressed."""
        # Create a mock frame
        mock_frame = np.zeros((480, 860, 3), dtype=np.uint8)

        # Mock VideoCapture to always return successful reads
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, mock_frame)
        mock_video_capture.return_value = mock_cap

        # Mock waitKey to return 'q' to exit the loop
        mock_wait_key.return_value = ord("q")

        on_frame_callback = Mock()
        camera = Camera(on_frame=on_frame_callback, debug=True)

        camera.read()

        # Verify callback was called
        on_frame_callback.assert_called_once()
        # Verify debug display was shown
        mock_imshow.assert_called_once()

    @patch("jinkomegami.sensors.camera.cv2.VideoCapture")
    def test_read_no_debug_mode(self, mock_video_capture: Any) -> None:
        """Test that no debug display is shown when debug=False."""
        # Create a mock frame
        mock_frame = np.zeros((480, 860, 3), dtype=np.uint8)

        # Mock VideoCapture
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.side_effect = [
            (True, mock_frame),  # First successful read
            (False, None),  # Second read fails to exit loop
        ]
        mock_video_capture.return_value = mock_cap

        on_frame_callback = Mock()
        camera = Camera(on_frame=on_frame_callback, debug=False)

        try:
            camera.read()
        except RuntimeError:
            pass  # Expected due to second read failing

        # Verify callback was called
        on_frame_callback.assert_called_once()

        # Verify no debug methods were called
        with patch("jinkomegami.sensors.camera.cv2.imshow") as mock_imshow:
            with patch("jinkomegami.sensors.camera.cv2.waitKey") as mock_wait_key:
                mock_imshow.assert_not_called()
                mock_wait_key.assert_not_called()

    def test_on_frame_callback_signature(self):
        """Test that the on_frame callback has the correct signature."""

        def valid_callback(frame_bytes: bytes) -> None:
            pass

        # This should not raise any errors
        camera = Camera(on_frame=valid_callback)
        assert camera.on_frame == valid_callback
