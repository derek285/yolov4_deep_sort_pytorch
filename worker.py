import paho.mqtt.client as mqtt
import uuid
import json
import cv2
import time
import struct
import threading
import numpy as np
import signal


sigint_catched = False
def sigint_handler(sig, frame):
    global sigint_catched
    sigint_catched = True

class Worker:
    def __init__(self, ip, port, sub='jwai/camera/0001', pub='jwai/track/0001', timeout=30):
        id = str(uuid.uuid4())
        self.mqtt_client = mqtt.Client(id, userdata=self, clean_session=True)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_message = self.on_message
        self.ip = ip
        self.port = port
        self.sub_topic = sub
        self.pub_topic = pub
        self.timeout = timeout
        self.callback_mutex = threading.RLock()
        self.on_new_image = None
    def connect(self):
        self.mqtt_client.connect(self.ip, self.port, self.timeout)
        self.mqtt_client.loop_start()

    def disconnect(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        
    # def loop(self):
    #     self.mqtt_client.loop_forever()
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        
        print(self.sub_topic)
        self.mqtt_client.subscribe(self.sub_topic, 0)
    
    def on_disconnect(self, client, userdata, rc):
        print("disconnected with result code "+str(rc))
    
    def on_message(self, client, userdata, msg):
        stamp = struct.unpack('LL', msg.payload[-16:])
        img = cv2.imdecode(np.fromstring(msg.payload, dtype='uint8'), cv2.IMREAD_UNCHANGED)
        print('Worker::on_message: ', stamp, time.clock_gettime(time.CLOCK_MONOTONIC))
        
        if(self.on_new_image != None):
            self.on_new_image(stamp, img)
            
    def publish(self, stamp, data):
        if(self.mqtt_client.is_connected() == False):
            return
        
        msg = bytes()
        #pack stamp & data into msg
        self.mqtt_client.publish(self.pub_topic, msg)
        
    @property
    def on_new_image(self):
        return self.on_new_image
    
    def on_new_image(self, func):
        with self.callback_mutex:
            self.on_new_image = func
        
def on_new_image(stamp, img):
    print(stamp)
    print(img.shape)
    cv2.imshow("img", img)
    cv2.waitKey(1)


'''
{
    "stamp": stamp,
    "data": [
        {"cls_id": 2, "track_id": 3, "bbox": "4,5,6,7"},
        {"cls_id": 3, "track_id": 5, "bbox": "6,7,8,9"}]
}
stamp: 时间戳
cls_id：检测物体类别id
track_id：跟踪结果id
bbox：左上右下，x1, y1, x2, y2

另其线程做检测跟踪，
无检测跟踪结果，publish
{"stamp": "stamp", "data": None}
丢帧无返回
'''


if __name__ == "__main__":
    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, sigint_handler)
    
    worker = Worker('192.168.1.24', 1883)
    worker.on_new_image = on_new_image
    worker.connect()
    
    while sigint_catched == False:
        time.sleep(0.1)
    
    signal.signal(signal.SIGINT, original_handler)
    
    worker.disconnect()

