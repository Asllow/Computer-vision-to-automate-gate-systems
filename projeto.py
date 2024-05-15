import cv2
import IpCameraList
from threading import Thread
from pygrabber.dshow_graph import FilterGraph

class WebcamStream :
    def __init__(self, stream_id):
        self.stream_id = stream_id

        self.vcap      = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False :
            print("[Saindo]: Erro ao acessar a gravação.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5))
        print("FPS da gravação da câmera: {}".format(fps_input_stream))

        self.grabbed , self.frame = self.vcap.read()
        if self.grabbed is False :
            print('[Saindo] Não há mais frames para ler.')
            exit(0)

        self.stopped = True

        self.t = Thread(target=self.update, args=())
        self.t.daemon = True

    def start(self):
        self.stopped = False
        self.t.start()
    def update(self):
        while True :
            if self.stopped is True :
                break
            self.grabbed , self.frame = self.vcap.read()
            if self.grabbed is False :
                print('[Saindo] Não há mais frames para ler.')
                self.stopped = True
                break
        self.vcap.release()
    def read(self):
        return self.frame
    def stop(self):
        self.stopped = True

def detectLocalCamera() :
    devices = FilterGraph().get_input_devices()
    available_cameras = len(devices)-1
    return available_cameras

def getLocalCamera(number_cam, webcam_stream, frame, cam_index = 0):
    for i in range (cam_index, number_cam):
        webcam_stream.append(WebcamStream(i))
        frame.append(0)
        webcam_stream[i - cam_index].start()

def getIpCamera(number_cam, webcam_stream, frame, ip_cam):
    if ip_cam != []:
        for a in range (len(ip_cam)):
            index = "rtsp://" + ip_cam[a]
            webcam_stream.append(WebcamStream(index))
            frame.append(0)
            webcam_stream[number_cam+a].start()

def closeAllCameras(range_all, webcam_stream, frame):
    for i in range (range_all):
        cv2.imwrite("images/[CAM" + str(i) + "]" + ".png" , frame[i])
        webcam_stream[i].stop()

def main ():
    ip_cam = IpCameraList.getNet()
    number_cam = detectLocalCamera()
    webcam_stream, frame, local_number_cam = [], [], number_cam
    if use_ip_webcam == False:
        ip_cam.clear()
    getLocalCamera(number_cam, webcam_stream, frame)
    getIpCamera(local_number_cam, webcam_stream, frame, ip_cam)
    range_all = local_number_cam + len(ip_cam)

    while True :
        num = 0
        for n in range (range_all):
            if webcam_stream[n].stopped is True :
                num = 1
                break
            else :
                frame[n] = webcam_stream[n].read()
            cv2.imshow("[CAM" + str(n) + "]", frame[n])
            key = cv2.waitKey(1)
            if key == 27:
                num = 1
                break
        if num == 1:
            break

    closeAllCameras(range_all, webcam_stream, frame)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    use_ip_webcam = True
    main()