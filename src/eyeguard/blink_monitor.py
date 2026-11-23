"""Opt-in, in-memory blink-rate measurement for a short webcam reading task."""

from __future__ import annotations

import statistics
import threading
import time
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "face_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)
CALIBRATION_SECONDS = 5
READING_SECONDS = 60
WAIT_FOR_FACE_SECONDS = 20

RIGHT_EYE = (33, 160, 158, 133, 153, 144)
LEFT_EYE = (362, 385, 387, 263, 373, 380)


def ensure_model_file(model_path: Path = MODEL_PATH) -> Path:
    """Download the official face-landmarker model once, without storing camera frames."""
    model_path.parent.mkdir(parents=True, exist_ok=True)
    if model_path.exists() and model_path.stat().st_size > 1_000_000:
        return model_path

    temporary_path = model_path.with_suffix(".download")
    request = urllib.request.Request(
        MODEL_URL,
        headers={"User-Agent": "EyeGuardAI/1.0 (face-landmarker model setup)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            model_bytes = response.read()
        if len(model_bytes) < 1_000_000:
            raise RuntimeError("The downloaded face-landmarker model was unexpectedly small.")
        temporary_path.write_bytes(model_bytes)
        temporary_path.replace(model_path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise
    return model_path


def _eye_aspect_ratio(landmarks, indices: tuple[int, int, int, int, int, int], width: int, height: int) -> float:
    points = [
        (float(landmarks[index].x) * width, float(landmarks[index].y) * height)
        for index in indices
    ]

    def distance(first: int, second: int) -> float:
        x1, y1 = points[first]
        x2, y2 = points[second]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    eye_width = distance(0, 3)
    if eye_width <= 1e-6:
        return 0.0
    return (distance(1, 5) + distance(2, 4)) / (2.0 * eye_width)


class BlinkMonitor:
    """Keep one live measurement in memory for a single Streamlit session."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._landmarker = None
        self._mp = None
        self._last_timestamp_ms = 0
        self.reset()

    def initialize(self) -> None:
        if self._landmarker is not None:
            return

        import mediapipe as mp

        model_path = ensure_model_file()
        options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self._landmarker = mp.tasks.vision.FaceLandmarker.create_from_options(options)
        self._mp = mp

    def reset(self) -> None:
        with self._lock:
            self.phase = "idle"
            self.phase_started_at: float | None = None
            self.phase_deadline: float | None = None
            self.wait_started_at: float | None = None
            self.last_error: str | None = None
            self.calibration_samples: list[float] = []
            self.threshold: float | None = None
            self.blink_count = 0
            self.frame_count = 0
            self.face_frame_count = 0
            self.valid_seconds = 0.0
            self.previous_valid_frame_at: float | None = None
            self.eye_closed_since: float | None = None
            self.last_ear: float | None = None

    def start_test(self) -> None:
        with self._lock:
            self.phase = "waiting_for_face"
            self.phase_started_at = None
            self.phase_deadline = None
            self.wait_started_at = time.monotonic()
            self.last_error = None
            self.calibration_samples = []
            self.threshold = None
            self.blink_count = 0
            self.frame_count = 0
            self.face_frame_count = 0
            self.valid_seconds = 0.0
            self.previous_valid_frame_at = None
            self.eye_closed_since = None
            self.last_ear = None

    def _advance_locked(self, now: float) -> None:
        if self.phase == "waiting_for_face" and self.wait_started_at is not None:
            if now - self.wait_started_at > WAIT_FOR_FACE_SECONDS:
                self.phase = "camera_timeout"

        elif self.phase == "calibrating" and self.phase_deadline is not None:
            if now >= self.phase_deadline:
                if len(self.calibration_samples) < 10:
                    self.phase = "calibration_failed"
                    return
                open_eye_median = statistics.median(self.calibration_samples)
                self.threshold = max(0.12, min(0.25, open_eye_median * 0.72))
                self.phase = "reading"
                self.phase_started_at = now
                self.phase_deadline = now + READING_SECONDS
                self.previous_valid_frame_at = None
                self.eye_closed_since = None

        elif self.phase == "reading" and self.phase_deadline is not None:
            if now >= self.phase_deadline:
                self.phase = "complete"
                self.phase_deadline = None
                self.previous_valid_frame_at = None

    def process_frame(self, frame):
        """Analyze a WebRTC frame and return it unchanged for the preview."""
        now = time.monotonic()
        with self._lock:
            self._advance_locked(now)
            should_process = self.phase in {"waiting_for_face", "calibrating", "reading"}
        if not should_process or self._landmarker is None or self._mp is None:
            return frame

        try:
            rgb = frame.to_ndarray(format="rgb24")
            height, width = rgb.shape[:2]
            image = self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=rgb)
            timestamp_ms = max(int(now * 1000), self._last_timestamp_ms + 1)
            self._last_timestamp_ms = timestamp_ms
            result = self._landmarker.detect_for_video(image, timestamp_ms)
            face = result.face_landmarks[0] if result.face_landmarks else None
            ear = None
            if face is not None and len(face) > max(RIGHT_EYE + LEFT_EYE):
                right_ear = _eye_aspect_ratio(face, RIGHT_EYE, width, height)
                left_ear = _eye_aspect_ratio(face, LEFT_EYE, width, height)
                ear = (right_ear + left_ear) / 2.0
        except Exception as error:
            with self._lock:
                self.last_error = str(error)
                self.phase = "camera_timeout"
            return frame

        with self._lock:
            self._advance_locked(now)
            if self.phase == "waiting_for_face":
                if ear is not None:
                    self.phase = "calibrating"
                    self.phase_started_at = now
                    self.phase_deadline = now + CALIBRATION_SECONDS

            if ear is not None and self.phase == "calibrating":
                if ear > 0.08:
                    self.calibration_samples.append(ear)

            if self.phase == "reading":
                self.frame_count += 1
                if ear is None:
                    self.previous_valid_frame_at = None
                    self.eye_closed_since = None
                else:
                    self.face_frame_count += 1
                    if self.previous_valid_frame_at is not None:
                        delta = now - self.previous_valid_frame_at
                        if 0 < delta <= 0.25:
                            self.valid_seconds += delta
                    self.previous_valid_frame_at = now
                    self.last_ear = ear
                    threshold = self.threshold if self.threshold is not None else 0.2
                    if ear < threshold:
                        if self.eye_closed_since is None:
                            self.eye_closed_since = now
                    elif self.eye_closed_since is not None:
                        closed_duration = now - self.eye_closed_since
                        if 0.06 <= closed_duration <= 0.8:
                            self.blink_count += 1
                        self.eye_closed_since = None

        return frame

    def snapshot(self) -> dict:
        now = time.monotonic()
        with self._lock:
            self._advance_locked(now)
            if self.phase == "calibrating" and self.phase_deadline is not None:
                phase_duration = CALIBRATION_SECONDS
            elif self.phase == "reading" and self.phase_deadline is not None:
                phase_duration = READING_SECONDS
            else:
                phase_duration = 1

            remaining = (
                max(0, int(self.phase_deadline - now))
                if self.phase_deadline is not None
                else 0
            )
            progress = 1.0 - min(1.0, remaining / phase_duration)
            coverage = (
                100.0 * self.face_frame_count / self.frame_count
                if self.frame_count
                else 0.0
            )
            enough_data = self.valid_seconds >= 40 and coverage >= 50
            blink_rate = (
                self.blink_count * 60.0 / self.valid_seconds
                if enough_data and self.valid_seconds > 0
                else None
            )
            if coverage >= 80:
                quality = "Good tracking coverage"
            elif coverage >= 50:
                quality = "Limited tracking coverage"
            else:
                quality = "Low tracking coverage"

            return {
                "phase": self.phase,
                "seconds_remaining": remaining,
                "progress": progress,
                "blink_count": self.blink_count,
                "blink_rate": blink_rate,
                "coverage_percent": coverage,
                "valid_seconds": self.valid_seconds,
                "quality": quality,
                "threshold": self.threshold,
                "error": self.last_error,
            }
