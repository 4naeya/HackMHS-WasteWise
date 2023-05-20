import requests
import cv2
from pyzbar import pyzbar

def capture_image2():
    # Open the webcam
    camera = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not camera.isOpened():
        print("Failed to open webcam")
        return

    # Read an image from the webcam
    _, image = camera.read()

    # Release the webcam
    camera.release()

    return image

input = ("press enter: ")


"""def modifiedReadBarcode():
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    decoded_objects = pyzbar.decode(frame)
    #cv2.imshow("Barcode Reader", frame)

    while True:
        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')
            barcode_type = obj.type

            print("Barcode Data:", barcode_data)
            print("Barcode Type:", barcode_type)
        cv2.imshow("Barcode Reader", frame)
        break

    cap.release()
    cv2.destroyAllWindows()

def capture_image():
    video_capture = cv2.VideoCapture(0)
    image_captured = False

    while True:
        ret, frame = video_capture.read()
        cv2.imshow("Barcode Scanner", frame)

        if not image_captured and keyboard.is_pressed('q'):
            image_captured = True
            break

        if cv2.waitKey(1) == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return frame

def recognize_barcode(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)

    if len(barcodes) == 0:
        print("No barcode found in the image.")
    else:
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            print("Barcode data: " + barcode_data)
            print("Barcode type: " + barcode_type)

def capture_image2():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        cv2.imshow("Barcode Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return frame

def recognize_barcode2(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    if len(barcodes) == 0:
        print("No barcode found in the image.")
        return None
    print(barcodes[0].data.decode("utf-8"))"""

def capture_image2():
    # Open the webcam
    camera = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not camera.isOpened():
        print("Failed to open webcam")
        return

    # Read an image from the webcam
    _, image = camera.read()

    # Release the webcam
    camera.release()

    return image
