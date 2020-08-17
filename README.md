# Yolov4 + Deep Sort with PyTorch

## remember build your own libdarknet.so and put under folder yolov4_deep_sort_pytorch/
## ref : https://github.com/ZQPei/deep_sort_pytorch

## Quick Start
0. Check all dependencies installed
```bash
pip3 install -r requirements.txt
```
for user in china, you can specify pypi source to accelerate install like:
```bash
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

1. Clone this repository
```
git clone https://github.com/derek285/yolov4_deep_sort_pytorch.git
```

2. Download YOLOv3 parameters
```
wget yolov4.weights
```

3. Download deepsort parameters ckpt.t7
```
cd deep_sort/deep/checkpoint
# download ckpt.t7 from
https://drive.google.com/drive/folders/1xhG0kRH1EX5B9_Iz8gQJb7UNnn_riXi6 to this folder
cd ../../../
```

Notice:
If compiling failed, the simplist way is to **Upgrade your pytorch >= 1.1 and torchvision >= 0.3" and you can avoid the troublesome compiling problems which are most likely caused by either `gcc version too low` or `libraries missing`.

4. Run demo
```
usage: python tracker.py VIDEO_PATH
                                [--help]
                                [--frame_interval FRAME_INTERVAL]
                                [--config_detection CONFIG_DETECTION]
                                [--config_deepsort CONFIG_DEEPSORT]
                                [--display]
                                [--display_width DISPLAY_WIDTH]
                                [--display_height DISPLAY_HEIGHT]
                                [--save_path SAVE_PATH]          
                                [--cpu]          


# yolov4 + deepsort on video file
python3 tracker.py VIDEO_PATH
# yolov4 + deepsort on webcam
python3 tracker.py /dev/video0 --camera 0

## References
- paper: [Simple Online and Realtime Tracking with a Deep Association Metric](https://arxiv.org/abs/1703.07402)
- code: [nwojke/deep_sort](https://github.com/nwojke/deep_sort)
- paper: [YOLOv3](https://pjreddie.com/media/files/papers/YOLOv3.pdf)
- code: [Joseph Redmon/yolov3](https://pjreddie.com/darknet/yolo/)
- code: [ZQPei/deep_sort_pytorch](https://github.com/ZQPei/deep_sort_pytorch)
- code:[AlexeyAB/darknet](https://github.com/AlexeyAB/darknet)
