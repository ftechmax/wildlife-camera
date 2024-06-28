#!/usr/bin/python3

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality, LibavH264Encoder
from picamera2.outputs import FfmpegOutput
from libcamera import controls
import os, time

cam1 = Picamera2(0)
#cam2 = Picamera2(1)
frame_rate = 30

# 2304x1296
# max resolution is (3280, 2464) for full FoV at 15FPS
video_config = cam1.create_video_configuration(main={"size": (1280, 720), "format": "YUV420"}, #, # YUV420, RGB888, XBGR8888
                                                 #lores={"size": (640, 480), "format": "YUV420"},
                                                # controls={'FrameRate': frame_rate})
                                                )

cam1.align_configuration(video_config)
cam1.configure(video_config)
#cam1.set_controls({"AfMode": controls.AfModeEnum.Manual})

# YouTube Stream URL and Key
#YOUTUBE_URL = "rtmps://a.rtmps.youtube.com/live2"
YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
#YOUTUBE_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
YOUTUBE_KEY = "86g2-b8cm-j27w-4uzc-5k0h"

# Construct the FFmpeg command for streaming
#stream_cmd = f'ffmpeg -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -c:a aac -f flv {YOUTUBE_URL}/{YOUTUBE_KEY}'

# FFMPEG output config

#-g 60 -use_wallclock_as_timestamps 1 -max_muxing_queue_size 400 -pix_fmt yuv420p -strict experimental
# -pix_fmt yuv420p -c:v libx264 -g 60 -max_muxing_queue_size 400
#-pix_fmt yuv420p -profile:v baseline -level 3.0 -acodec libfaac -ar 44100 -ac 2 -ab 192k -aspect 16:9 -r 24000/1001 -movflags +faststart
# -reorder_queue_size 4000 -max_delay 10000000 
#YToutput = FfmpegOutput(f'-loglevel debug -f flv {YOUTUBE_URL}/{YOUTUBE_KEY}', audio=False)
YToutput = FfmpegOutput(f'-loglevel debug -force_key_frames expr:gte(t,n_forced*2) -g 60 -bf 2 -coder 1 -pix_fmt yuv420p -f flv {YOUTUBE_URL}/{YOUTUBE_KEY}', audio=False)
#YToutput = FfmpegOutput('-loglevel debug /home/niels/wildlife-camera/test.h264', audio=False)
#HQoutput = FfmpegOutput("-f rtsp -rtsp_transport udp rtsp://myuser:mypass@localhost:8554/hqstream", audio=False)
##LQoutput = FfmpegOutput("-f rtsp -rtsp_transport udp rtsp://myuser:mypass@localhost:8554/lqstream", audio=False)

# Encoder settings
#encoder_HQ = H264Encoder(repeat=True, iperiod=30, framerate=frame_rate) #, enable_sps_framerate=True
encoder_HQ = H264Encoder( repeat=True, iperiod=30, framerate=frame_rate, profile="high", qp=30) #bitrate=3000000,
#encoder_HQ = LibavH264Encoder( repeat=True, iperiod=30, framerate=frame_rate, profile="high", qp=30) #bitrate=3000000,
##encoder_LQ = H264Encoder(repeat=True, iperiod=30, framerate=frame_rate, enable_sps_framerate=True)

try:
    print("trying to start camera streams")
    cam1.start_recording(encoder=encoder_HQ, output=YToutput, name="main") #, config=video_config, name="main" #, quality=Quality.MEDIUM
    #cam1.start_recording(encoder_HQ, HQoutput, quality=Quality.LOW)
    #cam1.start_recording(encoder_LQ, LQoutput, quality=Quality.LOW, name="lores")
    print("Started camera streams")
    while True:
        time.sleep(5)
        # still = cam1.capture_request()
        # still.save("main", "/dev/shm/camera-tmp.jpg")
        # still.release()
        # os.rename('/dev/shm/camera-tmp.jpg', '/dev/shm/camera.jpg') # make image replacement atomic operation
except :
    print("exiting picamera2 streamer")
    #cam1.stop_recording()
finally:
    print("stopping")
    cam1.stop_recording()