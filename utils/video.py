import cv2


def open_source(source):

    """
    Open:
    - video file
    - webcam
    - rtsp
    """

    try:

        if source == 0:
            cap = cv2.VideoCapture(0)

        else:
            cap = cv2.VideoCapture(source)

        if not cap.isOpened():
            raise Exception("Cannot open source")

        return cap

    except Exception as e:

        print("VIDEO ERROR:", e)

        return None