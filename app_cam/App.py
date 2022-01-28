#!/usr/bin/env python
# coding: utf-8

# In[1]:
import streamlit as st
from PIL import Image
import cv2
import pafy  # needs youtube_dl
import m3u8
#from pytube import YouTube

import warnings
warnings.filterwarnings('ignore')


import style as style
#import home as home
#import recomendation as recomendation
#import sobre as sobre

import threading
from typing import Union

import av
import numpy as np
import time

from streamlit_webrtc import VideoTransformerBase, webrtc_streamer


# ----------------------------------SIDEBAR -------------------------------------------------------------
def main():

    #style.set_background('images/bg03.jpg')
    
    #image = Image.open('images/logo_sidebar_sem_fundo.png')
    st.sidebar.image(image, use_column_width=True)
    st.sidebar.write('https://www.bixtecnologia.com/')
    
    style.spaces_sidebar(5)
    st.sidebar.header("Selecione o tipo de captura")

    captura = st.sidebar.radio(
     "Opções",
     ('Youtube ao vivo', 'Web cam', 'Câmera IP'))

    #st.image(image, use_column_width=True)  
    
# ------------------------------ INÍCIO ANÁLISE TÉCNICA E FUNDAMENTALISTA ----------------------------             

    st.title("Aplicativo de captura de câmera ao vivo")

    if captura == 'Web cam':

        #if st.button("print"):
        class VideoTransformer(VideoTransformerBase):
            frame_lock: threading.Lock  # `transform()` is running in another thread, then a lock object is used here for thread-safety.
            in_image: Union[np.ndarray, None]
            out_image: Union[np.ndarray, None]

            def __init__(self) -> None:
                self.frame_lock = threading.Lock()
                self.in_image = None
                self.out_image = None

            def transform(self, frame: av.VideoFrame) -> np.ndarray:
                in_image = frame.to_ndarray(format="bgr24")

                out_image = in_image[:, ::-1, :]  # Simple flipping for example.

                with self.frame_lock:
                    self.in_image = in_image
                    self.out_image = out_image

                return out_image




        ctx = webrtc_streamer(key="snapshot", video_transformer_factory=VideoTransformer)

        #if ctx.video_transformer:
        while ctx.video_transformer:
            #if st.button("Snapshot"):
            with ctx.video_transformer.frame_lock:
                in_image = ctx.video_transformer.in_image
                out_image = ctx.video_transformer.out_image

            if in_image is not None and out_image is not None:
                #st.write("Input image:")
                #st.image(in_image, channels="BGR")
                st.write("Output image:")
                st.image(out_image, channels="BGR")
            else:
                st.warning("No frames available yet.")
            time.sleep(10)



    if captura == 'Youtube ao vivo':
        camera_view()


    if captura == 'Câmera IP':
        
        style.spaces_sidebar(3)
        link = st.sidebar.text_input('Entre com o IP da câmera a conectar', 'Em desenvolvimento')


    
def camera_view():
    # streamlit placeholder for image/video
    image_placeholder = st.empty()

    # url for video
    # Jackson hole town square, live stream
    #video_url = "https://youtu.be/DoUOrTJbIu4" # "https://youtu.be/DDU-rZs-Ic4"

    #input link
    style.spaces_sidebar(3)
    link = st.sidebar.text_input('Cole um link do youtube pego pelo botão compartilhar', 'https://youtu.be/DoUOrTJbIu4')
    video_url = link

    streaming = st.video(link) 
    # Description
    #st.sidebar.write("Set options for processing video, then process a clip.")

    # Check for spots on temp file
    
    n_frames=30
    n_segments = st.sidebar.slider("Quantos frames por segundo?",
        n_frames, n_frames*6, n_frames, step=n_frames, key="spots", help="It comes in 7 segments, 100 frames each")
    n_segments = int(n_segments/n_frames)
    if st.sidebar.button("Capturar frames do vídeo do youtube"):
        while True:
            watch_video(video_url=video_url,
                                image_placeholder=image_placeholder,
                                n_segments=n_segments,
                                n_frames=n_frames)


def watch_video(video_url, image_placeholder, n_segments=1, n_frames=100000, n_frames_per_segment=60):
    """Gets a video clip, uses stored parkingspot boundaries OR makes new ones,
        counts how many spots exist in each frame, then displays a graph about it
        force_new_boxes: will force creation of new parking spot boundary boxes
        video_url: YouTube video URL"""


    skip_n_frames=10
    video_warning = st.warning("showing a clip from youTube...")

    # Use pafy to get the 360p url
    url=video_url
    video = pafy.new(url)

    # best = video.getbest(preftype="mp4")  #  Get best resolution stream available
    medVid = video.streams[2]

    #  load a list of current segments for live stream
    playlist = m3u8.load(medVid.url)

    # will hold all frames at the end
    # can be memory intestive, so be careful here
    frame_array = []

    # Speed processing by skipping n frames, so we need to keep track
    frame_num = 0

    #  Clip to total size if key word used
    if n_segments == "all":
        n_segments = int(len(playlist.segments))

    # Loop over each frame of video
    #  Loop through all segments
    for i in  playlist.segments[0:n_segments]: #playlist.segments[0:n_segments]:

        capture = cv2.VideoCapture(i.uri)

        # go through every frame in segment
        for i in range(n_frames_per_segment):

            success, frame = capture.read()
            
            if not success:
                break

            # Skip every nth frame to speed processing up
            if (frame_num % skip_n_frames != 0):
                frame_num += 1
                pass
            else:
                frame_num += 1

                # Convert the image from BGR color (which OpenCV uses) to RGB color
                #rgb_image = frame[:, :, ::-1]

                #print(f"Processing frame: #{frame_num}")
                # Run the image through the Mask R-CNN model to get results.

                image_placeholder.image(frame, channels="BGR")
                time.sleep(0.5)

                # Append frame to outputvideo
                frame_array.append(frame)

              

    # Clean up everything when finished
    capture.release()  # free the video
    # writeFramesToFile(frame_array=frame_array, fileName=video_save_file) #save the file

    # total_frames = display_video(image_placeholder, single_segment_url, frame_sleep=0.01)
    video_warning.empty()
    #st.write("Done with clip, frame length", frame_num)
    # replay the image you processed like the demo, options for downloading
    # if st.button("Play processed live video"):
    #     display_video(image_placeholder, image_array, show_chart = chart_placeholder,
    #                  vacancy_per_frame_df = vacancy_per_frame_df)

    return None
    



 
        
if __name__ == '__main__':
    main()


    # from pytube import Playlist
    # pl = Playlist("https://youtu.be/DoUOrTJbIu4")


    # run2 = st.checkbox('Run2')

    # if run2:

    #     from pytube import Playlist
    #     pl = Playlist("https://youtu.be/DoUOrTJbIu4")
    #     pl.segments[0].uri


    #     for video in pl.videos:
    #         medVid = video.streams[1] # .first().download()
    #         medVid = yt.streams[2]
            

    #         #  load a list of current segments for live stream
    #         playlist = m3u8.load(medVid.url)

    #         # will hold all frames at the end
    #         # can be memory intestive, so be careful here
    #         frame_array = []

    #         # Speed processing by skipping n frames, so we need to keep track
    #         frame_num = 0

    #         #  Clip to total size if key word used
    #         if n_segments == "all":
    #             n_segments = int(len(playlist.segments))

    #         # Loop over each frame of video
    #         #  Loop through all segments
    #         for i in playlist.segments[0:n_segments]:

    #             capture = cv2.VideoCapture(i.uri)

    #             # go through every frame in segment
    #             for i in range(n_frames_per_segment):

    #                 success, frame = capture.read()
    #                 if not success:
    #                     break

    #                 # Skip every nth frame to speed processing up
    #                 if (frame_num % skip_n_frames != 0):
    #                     frame_num += 1
    #                     pass
    #                 else:
    #                     frame_num += 1

    #                     # Convert the image from BGR color (which OpenCV uses) to RGB color
    #                     #rgb_image = frame[:, :, ::-1]

    #                     print(f"Processing frame: #{frame_num}")
    #                     # Run the image through the Mask R-CNN model to get results.

    #                     image_placeholder.image(frame, channels="BGR")
    #                     time.sleep(0.5)

    #                     # Append frame to outputvideo
    #                     frame_array.append(frame)

                    

    #         # Clean up everything when finished
    #         capture.release()  # free the video
    #         # writeFramesToFile(frame_array=frame_array, fileName=video_save_file) #save the file

    #         # total_frames = display_video(image_placeholder, single_segment_url, frame_sleep=0.01)
    #         video_warning.empty()
    #         st.write("Done with clip, frame length", frame_num)
    #         # replay the image you processed like the demo, options for downloading
    #         # if st.button("Play processed live video"):
    #         #     display_video(image_placeholder, image_array, show_chart = chart_placeholder,
    #         #                  vacancy_per_frame_df = vacancy_per_frame_df)


    #run = st.checkbox('Run')
    # FRAME_WINDOW = st.image([])
    # camera = cv2.VideoCapture(0)

    # while run:
    #     _, frame = camera.read()
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     FRAME_WINDOW.image(frame)
    # else:
    #     st.write('Stopped')


        # class VideoTransformer(VideoTransformerBase):
    #     frame_lock: threading.Lock  # `transform()` is running in another thread, then a lock object is used here for thread-safety.
    #     in_image: Union[np.ndarray, None]
    #     out_image: Union[np.ndarray, None]

    #     def __init__(self) -> None:
    #         self.frame_lock = threading.Lock()
    #         self.in_image = None
    #         self.out_image = None

    #     def transform(self, frame: av.VideoFrame) -> np.ndarray:
    #         in_image = frame.to_ndarray(format="bgr24")

    #         out_image = in_image[:, ::-1, :]  # Simple flipping for example.

    #         with self.frame_lock:
    #             self.in_image = in_image
    #             self.out_image = out_image

    #         return out_image

    # #if st.button("streaming video youtube"):
    
    # from pytube import YouTube

    # youtube = YouTube('https://www.youtube.com/watch?v=9q-QtBMjlR8')

    #for stream in youtube.streams:
    #    stream
    #    youtube.streams.get_highest_resolution().download()
    