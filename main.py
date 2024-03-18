# import threading
# import asyncio
# from controllers.camera.camera import Camera

# c1 = Camera(3, "test3", "rtsp://192.168.191.170:8080/h264_ulaw.sdp", ["uniform", "emotion"])
# c2 = Camera(2, "test2", 0, ["emotion"])

# async def process_camera(camera):
#     await camera.analysis_frame()

# def run_event_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_forever()

# def process_cameras():
#     threads = []
#     cameras = [c1,c2]

#     for camera in cameras:
#         thread = threading.Thread(target=asyncio.run, args=(process_camera(camera),))
#         thread.start()
#         threads.append(thread)

    # run_event_loop()

#     for thread in threads:
#         thread.join()

# process_cameras()

import threading
import asyncio
from controllers.camera.camera import Camera

# c1 = Camera(1, "test1", "rtsp://192.168.191.170:8080/h264_ulaw.sdp", ["uniform","emotion"])
c2 = Camera(2, "test2", 0, ["emotion"])

async def process_camera(camera):
    await camera.analysis_frame()

def run_event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

def process_cameras():
    threads = []
    cameras = [c2]

    for camera in cameras:
        thread = threading.Thread(target=asyncio.run, args=(process_camera(camera),))
        thread.start()
        threads.append(thread)

    run_event_loop()

    for thread in threads:
        thread.join()

process_cameras()



