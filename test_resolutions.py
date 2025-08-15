import cv2

# Common camera resolutions to test
COMMON_RESOLUTIONS = [
    (1920, 1080),  # Full HD
    (1280, 720),   # HD
    (1024, 576),
    (960, 540),
    (800, 600),
    (640, 480),    # VGA
    (320, 240),    # QVGA
]

def test_camera_resolutions(camera_index=0, verbose=False):
    supported = []
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Cannot open camera.")
        return supported

    for width, height in COMMON_RESOLUTIONS:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if int(actual_width) == width and int(actual_height) == height:
            supported.append((width, height))
            if verbose:
                print(f"Supported: {width}x{height}")
        elif verbose:
            print(f"Not supported: {width}x{height} (got {int(actual_width)}x{int(actual_height)})")

    cap.release()
    return supported


if __name__ == "__main__":
    # Run it
    print("Testing camera resolutions...")
    supported = test_camera_resolutions()
    for width, height in supported:
        print(f"Supported: {width}x{height}")
