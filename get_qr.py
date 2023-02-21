import cv2
import numpy as np


def capture_qr(camera):
    cam = camera
    ROI = []
    while True:
        try:
            check, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (7, 7), 0)
            thresh = cv2.threshold(
                blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            close = cv2.morphologyEx(
                thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
            cnts = cv2.findContours(
                close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.04 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                area = cv2.contourArea(c)
                ar = w / float(h)
                if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (36, 255, 12), 3)
                    ROI = frame[y:y+h, x:x+w]
                    cv2.imwrite('ROI.png', ROI)
            # cv2.imshow("capturing", frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            try:
                if ROI != []:
                    cv2.imwrite("ROI", ROI)
                    ret, buffer = cv2.imencode('.jpg', ROI)
                    ROI = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + ROI + b'\r\n')
            except:
                print("Scan fails")
                # cv2.imshow("ROI", ROI)
        #     key = cv2.waitKey(1)
        #     if key == ord('s'):
        #         cv2.imwrite(filename="QR.jpg", img=frame)
        #         cv2.imwrite(filename="ROI_QR.jpg", img=ROI)
        #         cam.release()
        #         break
        #     if key == ord('q'):
        #         cam.release()
        #         cv2.destroyAllWindows()
        #         break
        except (KeyboardInterrupt):
            print("Turning off camera")
            cam.release()
            cv2.destroyAllWindows()
            break
