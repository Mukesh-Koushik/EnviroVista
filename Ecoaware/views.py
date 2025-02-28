from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from Ecoaware.templates import *
from .models import *
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from PIL import Image
import piexif
from django.http import JsonResponse
from PIL.ExifTags import TAGS, GPSTAGS
import exifread
import datetime
import ffmpeg
import json

def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()  # Get EXIF metadata

        if not exif_data:
            return None, None, None

        gps_info = {}
        timestamp = None

        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for gps_tag in value:
                    gps_info[GPSTAGS.get(gps_tag, gps_tag)] = value[gps_tag]
            elif decoded == "DateTimeOriginal":
                timestamp = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

        if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
            lat = convert_to_degrees(gps_info["GPSLatitude"])
            lon = convert_to_degrees(gps_info["GPSLongitude"])
            if gps_info.get("GPSLatitudeRef") == "S":
                lat = -lat
            if gps_info.get("GPSLongitudeRef") == "W":
                lon = -lon
            return lat, lon, timestamp

    except Exception as e:
        print(f"Error extracting EXIF: {e}")

    return None, None, None

def convert_to_degrees(value):
    """Convert GPS coordinates to degrees format."""
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def get_video_metadata(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        creation_time = None

        for stream in probe["streams"]:
            if "tags" in stream and "creation_time" in stream["tags"]:
                creation_time = stream["tags"]["creation_time"]
                creation_time = datetime.datetime.strptime(creation_time, "%Y-%m-%dT%H:%M:%S.%fZ")

        return creation_time

    except Exception as e:
        print(f"Error extracting video metadata: {e}")
        return None

def save_file_and_extract_metadata(file, category):
    """Handles file saving, metadata extraction, and database entry."""
    if not file:
        return None  # Skip if no file was uploaded

    original_filename = file.name  # Preserve the original filename
    file_path = os.path.join("uploads/", original_filename)

    # Save the file with its original name
    saved_path = default_storage.save(file_path, ContentFile(file.read()))

    # Create metadata entry
    metadata = MediaMetadata(file=saved_path, filename=original_filename)
    metadata.save()

    # Extract metadata
    absolute_file_path = metadata.file.path
    print(absolute_file_path)
    if category == "image":
        lat, lon, timestamp = get_exif_data(absolute_file_path)
    elif category == "video":
        timestamp = get_video_metadata(absolute_file_path)
        lat, lon = None, None  # GPS data is usually absent in videos

    # Save extracted metadata
    metadata.latitude = lat
    metadata.longitude = lon
    metadata.timestamp = timestamp
    metadata.save()

    return metadata.filename  # Return filename for response message

def upload_task(request):
    if request.method == "POST":
        response_data = {}  # Store filenames for confirmation

        # Handle images
        for i in range(1, 7):  # Image1 to Image6
            file = request.FILES.get(f"image{i}")
            filename = save_file_and_extract_metadata(file, "image")
            if filename:
                response_data[f"Image {i}"] = filename

        # Handle video
        video_file = request.FILES.get("video")
        filename = save_file_and_extract_metadata(video_file, "video")
        if filename:
            response_data["Video"] = filename

        return render(request, "EV_Ideaforge.html")

    return render(request, "EV_Ideaforge.html")


def ecoaware_display(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    return render(request, 'EV_TaskUploadPage.html', {"task_no": task})
    pass


def taskshome(request):
    grps=Tasks.objects.filter(mode="2")
    inds=Tasks.objects.filter(mode="1")
    return render(request, 'EV_EcoawareHomePage.html', {"grps":grps, "inds": inds})

def submit_task(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)

    return render(request, 'EV_TaskUploadPage.html', {'task': task})

def submission(request):
    return render(request, 'EV_TaskUploadPage.html')

def ideaforge(request):
    return render(request, 'EV_IdeaForge.html')

def ideaforgeconf(request):
    name = request.POST.get("name")
    desc = request.POST.get("desc")
    video = request.FILES.get("video_file")

    sub = IdeaForge(task_name = name, task_description = desc, task_video = video)
    sub.save()

    return redirect(taskshome)
    pass
# Create your views here.
