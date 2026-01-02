import cv2
import numpy as np
from pathlib import Path

def remove_background_simple(image_path, output_path):
    """
    Simple background removal using color-based segmentation.
    Works best with uniform backgrounds.
    """
    # Read image
    img = cv2.imread(str(image_path))
    
    # Convert to HSV for better color segmentation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define range for background color (adjust based on your images)
    # This assumes a light/white background
    lower_bg = np.array([0, 0, 200])  # Light colors
    upper_bg = np.array([180, 30, 255])  # Very light colors
    
    # Create mask for background
    bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)
    
    # Invert mask to get foreground (car)
    fg_mask = cv2.bitwise_not(bg_mask)
    
    # Apply some morphology to clean up the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    
    # Create 4-channel image (BGRA)
    b, g, r = cv2.split(img)
    rgba = cv2.merge((b, g, r, fg_mask))
    
    # Save as PNG with transparency
    cv2.imwrite(str(output_path), rgba)
    
    return True

# Main processing
input_dir = Path("car_frames")
output_dir = Path("car_frames_nobg")
output_dir.mkdir(exist_ok=True)

frame_files = sorted(input_dir.glob("frame_*.jpg"))

print(f"Processing {len(frame_files)} frames...")
print("This uses simple color-based background removal.")
print("Adjust color thresholds if results aren't good.\n")

success_count = 0
for i, frame_path in enumerate(frame_files, 1):
    output_path = output_dir / (frame_path.stem + ".png")
    
    try:
        remove_background_simple(frame_path, output_path)
        print(f"✓ {i}/{len(frame_files)}: {frame_path.name}")
        success_count += 1
    except Exception as e:
        print(f"✗ {i}/{len(frame_files)}: {frame_path.name} - Error: {e}")

print(f"\n✅ Processed {success_count}/{len(frame_files)} frames")
print(f"Output: {output_dir}")
print("\nNote: Results may vary. For best quality, use remove.bg or similar AI tools.")
