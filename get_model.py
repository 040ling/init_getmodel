"""
本文件的目的：获取摄像头所拍摄的图片
"""
import time
import cv2
import threading
import numpy as np
import queue



def show_photo(name,img):
    cv2.namedWindow(name,0)
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class CamCapture:
    def __init__(self, link, num):
        self.cap = cv2.VideoCapture(link)  # 通过link建立摄像头连接
        self.q = queue.Queue()  # 读入图片的队列
        self.ret = True
        self.num = num  # 正面：0 左侧：1 右侧：2
        self.link = link
        t = threading.Thread(target=self._reader, name="grandson" + str(num))  # 构造读图片的进程
        t.daemon = True
        t.start()
    #待分析的图片
    def _reader(self):
        global ExitFlag  # 指示是否已退出判别流程，如果是则不执行循环
        # 这里需要有一个开始判读 停止判读的按钮
        ExitFlag = 0  # 默认没有退出
        while True:
            try:
                self.ret, self.frame = self.cap.read()  # 拿到图片交给self.frame
            except:
                print("无法正常获取图片")
                r_channel = np.zeros((1920, 1080), dtype=np.uint8)
                g_channel = np.zeros((1920, 1080), dtype=np.uint8)
                b_channel = np.zeros((1920, 1080), dtype=np.uint8)
                self.frame = cv2.merge((b_channel, g_channel, r_channel))  # 显示为黑屏
                self.ret = False

            if not self.ret:  # 如果超过5s没拿到图片就播放黑屏
                r_channel = np.zeros((1920, 1080), dtype=np.uint8)
                g_channel = np.zeros((1920, 1080), dtype=np.uint8)
                b_channel = np.zeros((1920, 1080), dtype=np.uint8)
                self.frame = cv2.merge((b_channel, g_channel, r_channel))
                # break00
            if not self.q.empty():  # 如果当前有图片则取出图片
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(self.frame)  # 向队列中载入图片
            if ExitFlag:  # 如果触发flag则退出
                break
        return

    def read(self):
        self.get_start = time.time()
        while time.time() - self.get_start < 5:
            try:
                return True, self.q.get_nowait()
            except:
                time.sleep(0.01)

        print("超过5s没有拿到图片")
        return False, self.frame



def link_cam(save_path,num):

    fn = "rtsp://admin:Abcd12345678@3.1.200.189" + ":554/h265/ch33/main/av_stream?tcp"
    save_vid = './' + save_path + '/' + str(120 + num) + '.avi'
    cam = CamCapture(fn, num)
    print(save_vid)
    ret, frame = cam.read()
    if ret:
        show_photo("0.jpg",frame)
        cv2.imwrite("0.jpg",frame)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    link_cam("out",0)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
