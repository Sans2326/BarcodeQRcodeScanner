import cv2
import numpy as np
from pyzbar.pyzbar import decode

with open('venv/data') as f:
    lists = f.read().splitlines()

def read_qrbar(frame):
    codes = decode(frame)
    for code in codes:
        info = code.data.decode('utf-8')
        print(info)
        # authentication
        if info in lists:
            data = 'Authorized'
            fcolor = (0, 255, 0)
        else:
            data = 'Unauthorized'
            fcolor = (0, 0, 255)
        print(data)

        # Make Boundary
        pts = np.array([code.polygon], np.int32)
        pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, fcolor, 5)
        pts2 = code.rect
        cv2.putText(frame, data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_DUPLEX, 0.9, fcolor, 2)

        # write recognized text into the file
        with open("barcode_result.txt", mode='w') as fp:
            fp.write("Recognized Barcode/QR Code:" + info)

    return frame

# capturing frames

def main():
    cap = cv2.VideoCapture(0)
    success, frame = cap.read()
    while success:
        success, frame = cap.read()
        frame = read_qrbar(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        # Press esc to stop scanning
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
