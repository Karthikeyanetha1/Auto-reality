from PIL import Image, ImageStat

def analyze_image(image_path):
    img = Image.open(image_path).convert("RGB")

    stat = ImageStat.Stat(img)
    brightness = sum(stat.mean) / 3
    contrast = sum(stat.stddev) / 3

    issues = []
    if brightness < 60:
        issues.append("Low lighting")
    if contrast < 20:
        issues.append("Blurry or low-detail image")

    if not issues:
        issues.append("No visible damage detected")

    return {
        "type": "image",
        "brightness": round(brightness, 2),
        "contrast": round(contrast, 2),
        "issues": issues
    }
