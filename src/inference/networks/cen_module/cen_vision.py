import cv2 as cv

#VLA, CV2 soon

cam = cv.VideoCapture(0)


if not cam.isOpened():
    print("Cannot open camera")

grayscale_active = False

while cam.isOpened() is True:

    ret, frame = cam.read()
    key_listen = cv.waitKey(35) & 0xFF

    if ret:

        pass
#soon


def vision(self, text: str):

        vla_model = None

