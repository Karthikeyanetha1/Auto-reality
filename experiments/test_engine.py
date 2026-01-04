from engine.image_engine import analyze_image
from engine.video_engine import analyze_video
from engine.overlay_engine import generate_overlay

# IMAGE TEST
img_result = analyze_image("sample_image.jpg")
print("\nIMAGE RESULT")
print(img_result)

overlay = generate_overlay(img_result["issues"])
print("\nACTIONS")
print(overlay)

# VIDEO TEST (dummy name-based logic)
vid_result = analyze_video("fan_vibration_test.mp4")
print("\nVIDEO RESULT")
print(vid_result)

overlay2 = generate_overlay(vid_result["issues"])
print("\nVIDEO ACTIONS")
print(overlay2)
