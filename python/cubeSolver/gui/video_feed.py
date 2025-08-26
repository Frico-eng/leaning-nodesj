import cv2
import threading
import time

class VideoFeed:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.callback = None
        
    def start(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            return False
            
        self.is_running = True
        self.thread = threading.Thread(target=self._capture_loop)
        self.thread.daemon = True
        self.thread.start()
        return True
        
    def _capture_loop(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                if self.callback:
                    self.callback(frame)
            time.sleep(0.03)  # ~30 FPS
            
    def set_callback(self, callback):
        self.callback = callback
        
    def get_frame(self):
        return self.current_frame
        
    def stop(self):
        self.is_running = False
        if self.cap:
            self.cap.release()