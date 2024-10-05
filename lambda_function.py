#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import yt_dlp
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # URL de la vidéo YouTube codée en dur
    video_url = "https://youtu.be/H-DFVxHsSfc?si=725To3yz-qBDV4w_"
    
    # Options pour yt-dlp
    ydl_opts = {
        'outtmpl': '/tmp/%(title)s.%(ext)s',  # Enregistre la vidéo dans /tmp
        'format': 'bestvideo+bestaudio/best', # Télécharge la meilleure qualité
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_title = info.get('title', None)
            video_filename = ydl.prepare_filename(info)

        # Uploader sur S3 après téléchargement
        bucket_name = 'stockage-video-lambda'
        s3.upload_file(video_filename, bucket_name, f'youtube_videos/{os.path.basename(video_filename)}')

        return {
            'statusCode': 200,
            'body': f"Downloaded and uploaded video '{video_title}' to S3 successfully."
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Failed to download video: {str(e)}"
        }

