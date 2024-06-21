#!/usr/bin/python3

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
from libcamera import controls
import os, time

cam1 = Picamera2(0)
#cam2 = Picamera2(1)
frame_rate = 30

# 2304x1296
# max resolution is (3280, 2464) for full FoV at 15FPS
video_config = cam1.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"}, # YUV420, RGB888
                                                 #lores={"size": (640, 480), "format": "YUV420"},
                                                 controls={'FrameRate': frame_rate})
cam1.align_configuration(video_config)
cam1.configure(video_config)
#cam1.set_controls({"AfMode": controls.AfModeEnum.Manual})

# YouTube Stream URL and Key
#YOUTUBE_URL = "rtmps://a.rtmps.youtube.com/live2"
YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
YOUTUBE_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxx"

# Construct the FFmpeg command for streaming
#stream_cmd = f'ffmpeg -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv {YOUTUBE_URL}/{YOUTUBE_KEY}'

# FFMPEG output config

#-g 60 -use_wallclock_as_timestamps 1 -max_muxing_queue_size 400

#YToutput = FfmpegOutput(f'-loglevel debug -f flv {YOUTUBE_URL}/{YOUTUBE_KEY}', audio=False)
YToutput = FfmpegOutput(f'-loglevel debug -pix_fmt yuv420p -f flv {YOUTUBE_URL}/{YOUTUBE_KEY}', audio=False)
#YToutput = FfmpegOutput('-loglevel debug -use_wallclock_as_timestamps 1 -strict experimental /home/niels/wildlife-camera/test.h264', audio=False)
#HQoutput = FfmpegOutput("-f rtsp -rtsp_transport udp rtsp://myuser:mypass@localhost:8554/hqstream", audio=False)
##LQoutput = FfmpegOutput("-f rtsp -rtsp_transport udp rtsp://myuser:mypass@localhost:8554/lqstream", audio=False)

# Encoder settings
#encoder_HQ = H264Encoder(repeat=True, iperiod=30, framerate=frame_rate) #, enable_sps_framerate=True
encoder_HQ = H264Encoder(bitrate=3000000, repeat=True, iperiod=30, framerate=frame_rate)
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