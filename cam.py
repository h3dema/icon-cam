import cv2
import threading
import time
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

#
# Global variables
#
is_recording = False
stop_signal = False
motion_cooldown = 5  # seconds to wait before stopping recording after motion ends
video_format = "avi"
video_format = "mp4"

assert video_format in ["avi", "mp4"]


def create_icon_image():
    image = Image.new('RGB', (64, 64), 'black')
    d = ImageDraw.Draw(image)
    d.ellipse((16, 16, 48, 48), fill='red')
    return image


def detect_motion(prev_frame, curr_frame, threshold=25):
    diff = cv2.absdiff(prev_frame, curr_frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
    motion = cv2.countNonZero(thresh)
    return motion > 5000  # tweak this based on sensitivity


def record_video():
    global is_recording, stop_signal
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    ret, prev_frame = cap.read()
    if not ret:
        cap.release()
        return

    prev_frame = cv2.resize(prev_frame, (640, 480))

    out = None
    last_motion_time = 0
    recording_active = False

    while cap.isOpened() and not stop_signal:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        motion = detect_motion(prev_frame, frame)
        curr_time = time.time()

        if motion:
            last_motion_time = curr_time
            if not recording_active:
                # Start new video file
                if video_format == "avi":
                    filename = f"video_{int(curr_time)}.avi"
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                else:
                    filename = f"video_{int(curr_time)}.mp4"
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
                recording_active = True
                print(f"Motion detected. Recording to {filename}...")

        if recording_active:
            out.write(frame)
            if curr_time - last_motion_time > motion_cooldown:
                # Stop recording
                print("Motion ended. Stopping recording.")
                out.release()
                recording_active = False

        prev_frame = frame.copy()

    if out and recording_active:
        out.release()
    cap.release()
    is_recording = False


def start_recording(icon, item):
    global is_recording, stop_signal
    if not is_recording:
        stop_signal = False
        is_recording = True
        threading.Thread(target=record_video).start()

def stop_recording(icon, item):
    global stop_signal
    stop_signal = True

def exit_program(icon, item):
    global stop_signal
    stop_signal = True
    icon.stop()


if __name__ == "__main__":
    print("Starting CamSurv...")
    icon = Icon("CamSurv", create_icon_image(), menu=Menu(
        MenuItem("Start Recording", start_recording),
        MenuItem("Stop Recording", stop_recording),
        MenuItem("Exit", exit_program)
    ))
    icon.run()
