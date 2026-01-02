import cv2
import numpy as np
from pathlib import Path

# Configuration
INPUT_FOLDER = 'car_frames_nobg'
OUTPUT_FOLDER = 'car_frames_aligned'
CANVAS_SIZE = (1200, 900)  # Fixed canvas size (width, height)
CAR_CENTER_POSITION = (600, 450)  # Where to center the car

def find_car_center(image):
    """Find the center of the car (non-transparent pixels)"""
    if image.shape[2] == 4:  # Has alpha channel
        # Use alpha channel to find car
        alpha = image[:, :, 3]
        non_zero = cv2.findNonZero(alpha)
    else:
        # Convert to grayscale and threshold
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        non_zero = cv2.findNonZero(binary)
    
    if non_zero is not None:
        # Calculate centroid
        moments = cv2.moments(non_zero)
        if moments['m00'] != 0:
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
            return (cx, cy)
    
    # Fallback to image center
    return (image.shape[1] // 2, image.shape[0] // 2)

def align_frame(input_path, output_path):
    """Align a single frame to center the car"""
    # Read image with alpha channel
    img = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)
    
    if img is None:
        print(f"Failed to load: {input_path}")
        return False
    
    # Find car center in current frame
    car_center = find_car_center(img)
    
    # Calculate offset to center the car
    offset_x = CAR_CENTER_POSITION[0] - car_center[0]
    offset_y = CAR_CENTER_POSITION[1] - car_center[1]
    
    # Create canvas with transparency
    if img.shape[2] == 4:
        canvas = np.zeros((CANVAS_SIZE[1], CANVAS_SIZE[0], 4), dtype=np.uint8)
    else:
        canvas = np.zeros((CANVAS_SIZE[1], CANVAS_SIZE[0], 3), dtype=np.uint8)
    
    # Calculate paste position
    paste_x = offset_x
    paste_y = offset_y
    
    # Calculate source and destination regions
    src_x1 = max(0, -paste_x)
    src_y1 = max(0, -paste_y)
    src_x2 = min(img.shape[1], CANVAS_SIZE[0] - paste_x)
    src_y2 = min(img.shape[0], CANVAS_SIZE[1] - paste_y)
    
    dst_x1 = max(0, paste_x)
    dst_y1 = max(0, paste_y)
    dst_x2 = dst_x1 + (src_x2 - src_x1)
    dst_y2 = dst_y1 + (src_y2 - src_y1)
    
    # Paste image onto canvas
    if src_x2 > src_x1 and src_y2 > src_y1:
        canvas[dst_y1:dst_y2, dst_x1:dst_x2] = img[src_y1:src_y2, src_x1:src_x2]
    
    # Save aligned frame
    cv2.imwrite(str(output_path), canvas)
    return True

def main():
    input_folder = Path(INPUT_FOLDER)
    output_folder = Path(OUTPUT_FOLDER)
    output_folder.mkdir(exist_ok=True)
    
    # Get all PNG files
    frame_files = sorted(input_folder.glob('frame_*.png'))
    
    if not frame_files:
        print(f"No frame files found in {INPUT_FOLDER}")
        return
    
    print(f"Aligning {len(frame_files)} frames...")
    print(f"Canvas size: {CANVAS_SIZE[0]}x{CANVAS_SIZE[1]}")
    print(f"Car will be centered at: {CAR_CENTER_POSITION}")
    
    success_count = 0
    for i, input_path in enumerate(frame_files, 1):
        output_path = output_folder / input_path.name
        
        if align_frame(input_path, output_path):
            success_count += 1
            if i % 10 == 0:
                print(f"Processed {i}/{len(frame_files)} frames...")
        else:
            print(f"Failed to process: {input_path.name}")
    
    print(f"\nAlignment complete!")
    print(f"Successfully aligned {success_count}/{len(frame_files)} frames")
    print(f"Output saved to: {output_folder}")

if __name__ == '__main__':
    main()
