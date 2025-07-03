import cv2
import os
import requests
from tqdm import tqdm
import sys
import time

# === CONFIGURATION ===
VIDEO_PATH = "Videos"
FRAME_OUTPUT = "frames/"
FRAME_EVERY_SECONDS = 1
ROBOFLOW_API_KEY = "PhuuoxIe8aebkVbYkV2U"
ROBOFLOW_WORKSPACE = "projectcamera"
ROBOFLOW_PROJECT = "traffic-control-managment"
ROBOFLOW_VERSION = 1
UPLOAD_LIMIT = 200
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# === ERROR HANDLING CLASS ===
class FrameExtractionError(Exception):
    pass

class RoboflowUploadError(Exception):
    pass

# === FRAME EXTRACTION WITH ERROR HANDLING ===
def extract_frames_from_videos():
    try:
        # Directory validation
        if not os.path.exists(VIDEO_PATH): # Si the directory does not exist
            raise FrameExtractionError(f"Video directory not found: {VIDEO_PATH}")
        
        if not os.access(VIDEO_PATH, os.R_OK): # No read permissions
            raise FrameExtractionError(f"No read permissions for: {VIDEO_PATH}")

        os.makedirs(FRAME_OUTPUT, exist_ok=True) # Create output directory if it doesn't exist
        if not os.access(FRAME_OUTPUT, os.W_OK): # No write permissions
            raise FrameExtractionError(f"No write permissions for: {FRAME_OUTPUT}")

        video_files = [f for f in os.listdir(VIDEO_PATH) if f.endswith(".mp4")] # List all MP4 files f in os.listdir(VIDEO_PATH) listdir video directory
        if not video_files:
            raise FrameExtractionError(f"No MP4 files found in {VIDEO_PATH}") 

        count = 0
        processed_files = 0

        for video_file in video_files:
            video_path = os.path.join(VIDEO_PATH, video_file)
            
            try:
                # Video file validation
                if not os.path.exists(video_path):
                    print(f"⚠️ Warning: File not found, skipping: {video_file}")
                    continue

                cap = cv2.VideoCapture(video_path) # Open video file
                if not cap.isOpened():
                    print(f"⚠️ Warning: Could not open video, skipping: {video_file}")
                    continue

                # Frame processing
                fps = cap.get(cv2.CAP_PROP_FPS) # Get frames per second
                if fps <= 0:
                    print(f"⚠️ Warning: Invalid FPS ({fps}) in {video_file}, using default 30 FPS")
                    fps = 30.0

                frame_interval = max(1, int(fps * FRAME_EVERY_SECONDS))  # Ensure at least 1
                i = 0
                frames_extracted = 0

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    if i % frame_interval == 0:
                        filename = os.path.join(FRAME_OUTPUT, f"frame_{count:05d}.jpg")
                        try:
                            if not cv2.imwrite(filename, frame):
                                raise FrameExtractionError(f"Failed to write frame {count} to {filename}")
                            count += 1
                            frames_extracted += 1
                        except Exception as e:
                            print(f"⚠️ Warning: Error saving frame {count}: {str(e)}")
                    i += 1

                processed_files += 1
                print(f"✓ Processed {video_file}: Extracted {frames_extracted} frames")

            except Exception as e:
                print(f"⚠️ Warning: Error processing {video_file}: {str(e)}")
            finally:
                if 'cap' in locals() and cap.isOpened():
                    cap.release()

        if count == 0:
            raise FrameExtractionError("No frames were extracted from any video")
            
        print(f"\n✅ Successfully extracted {count} frames from {processed_files}/{len(video_files)} videos")

    except Exception as e:
        raise FrameExtractionError(f"Frame extraction failed: {str(e)}")

# === ROBUST UPLOAD FUNCTION ===
def upload_to_roboflow():
    try:
        # Output directory validation
        if not os.path.exists(FRAME_OUTPUT):
            raise RoboflowUploadError(f"Frame directory not found: {FRAME_OUTPUT}")

        frame_files = [f for f in os.listdir(FRAME_OUTPUT) if f.endswith(".jpg")]
        if not frame_files:
            raise RoboflowUploadError(f"No JPG files found in {FRAME_OUTPUT}")

        url = f"https://api.roboflow.com/dataset/{ROBOFLOW_PROJECT}/upload"
        headers = {"Authorization": f"Bearer {ROBOFLOW_API_KEY}"}
        uploaded_count = 0
        failed_count = 0

        for file_name in tqdm(frame_files[:UPLOAD_LIMIT], desc="Uploading to Roboflow"):
            image_path = os.path.join(FRAME_OUTPUT, file_name)
            
            if not os.path.exists(image_path):
                print(f"⚠️ Warning: File not found, skipping: {file_name}")
                failed_count += 1
                continue

            for attempt in range(MAX_RETRIES):
                try:
                    with open(image_path, "rb") as f:
                        response = requests.post(
                            url,
                            headers=headers,
                            params={"name": file_name, "split": "train"},
                            files={"file": f},
                            timeout=30
                        )

                    if response.status_code == 200:
                        uploaded_count += 1
                        break
                    else:
                        if attempt == MAX_RETRIES - 1:
                            print(f"⚠️ Warning: Failed to upload {file_name} after {MAX_RETRIES} attempts. Status: {response.status_code}, Response: {response.text}")
                            failed_count += 1
                        time.sleep(RETRY_DELAY)
                
                except (requests.exceptions.RequestException, IOError) as e:
                    if attempt == MAX_RETRIES - 1:
                        print(f"⚠️ Warning: Failed to upload {file_name}: {str(e)}")
                        failed_count += 1
                    time.sleep(RETRY_DELAY)

        if uploaded_count == 0:
            raise RoboflowUploadError("No files were successfully uploaded")
            
        print(f"\n✅ Uploaded {uploaded_count} files to Roboflow ({failed_count} failures)")

    except Exception as e:
        raise RoboflowUploadError(f"Upload failed: {str(e)}")

# === YAML GENERATION ===
def generate_yolov8_yaml(class_list):
    try:
        os.makedirs("dataset", exist_ok=True)
        yaml_path = os.path.join("dataset", "data.yaml")
        
        with open(yaml_path, "w") as f:
            f.write("train: images/train\n")
            f.write("val: images/val\n")
            f.write(f"nc: {len(class_list)}\n")
            f.write(f"names: {class_list}\n")
        
        print(f"✅ Created YOLOv8 config at {yaml_path}")

    except Exception as e:
        print(f"⚠️ Warning: Failed to create YAML file: {str(e)}")
        sys.exit(1)

# === MAIN FLOW WITH ERROR HANDLING ===
if __name__ == "__main__":
    try:
        print("[1] Extracting frames...")
        extract_frames_from_videos()

        print("\n[2] Uploading to Roboflow...")
        upload_to_roboflow()

        print("\n[3] Generating YOLOv8 config...")
        classes = [
            "Car", "Truck", "Bus", "Motorcycle",
            "Pedestrian",
            "TrafficLightRed", "TrafficLightGreen", "TrafficLightYellow"
        ]
        generate_yolov8_yaml(classes)

        print("\n✅ All operations completed successfully!")

    except FrameExtractionError as e:
        print(f"\n❌ Frame extraction error: {str(e)}")
        sys.exit(1)
    except RoboflowUploadError as e:
        print(f"\n❌ Roboflow upload error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)