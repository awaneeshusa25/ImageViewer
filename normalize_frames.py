import cv2
import numpy as np
from pathlib import Path

# Configuration
INPUT_FOLDER = 'car_frames_nobg'
OUTPUT_FOLDER = 'car_frames_normalized'
OUTPUT_SIZE = (800, 600)  # Final output size (width, height)

def get_car_bbox(image):
    """Get bounding box of the car"""
    if image.shape[2] == 4:
        alpha = image[:, :, 3]
        coords = cv2.findNonZero(alpha)
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        coords = cv2.findNonZero(binary)
    
    if coords is not None:
        return cv2.boundingRect(coords)
    return None

def main():
    input_folder = Path(INPUT_FOLDER)
    output_folder = Path(OUTPUT_FOLDER)
    output_folder.mkdir(exist_ok=True)
    
    frame_files = sorted(input_folder.glob('frame_*.png'))
    
    if not frame_files:
        print(f"No frames found in {INPUT_FOLDER}")
        return
    
    print("Step 1: Finding maximum car dimensions across all frames...")
    
    # Find maximum bounding box
    max_width = 0
    max_height = 0
    bboxes = []
    
    for frame_path in frame_files:
        img = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
        bbox = get_car_bbox(img)
        if bbox:
            x, y, w, h = bbox
            max_width = max(max_width, w)
            max_height = max(max_height, h)
            bboxes.append(bbox)
        else:
            bboxes.append(None)
    
    print(f"Maximum car dimensions: {max_width}x{max_height}")
    
    # Calculate scale to fit in output size with padding
    padding = 50
    scale_w = (OUTPUT_SIZE[0] - 2 * padding) / max_width
    scale_h = (OUTPUT_SIZE[1] - 2 * padding) / max_height
    scale = min(scale_w, scale_h)
    
    print(f"Scale factor: {scale:.3f}")
    
    # Calculate final car size
    final_car_w = int(max_width * scale)
    final_car_h = int(max_height * scale)
    
    # Calculate center position on canvas
    center_x = OUTPUT_SIZE[0] // 2
    center_y = OUTPUT_SIZE[1] // 2
    
    print(f"\nStep 2: Normalizing {len(frame_files)} frames...")
    print(f"All cars will be {final_car_w}x{final_car_h} pixels")
    print(f"Centered at: ({center_x}, {center_y})")
    
    success = 0
    for i, (frame_path, bbox) in enumerate(zip(frame_files, bboxes), 1):
        img = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
        
        if img is None or bbox is None:
            print(f"Skipping {frame_path.name}")
            continue
        
        x, y, w, h = bbox
        
        # Crop car from original image
        car_crop = img[y:y+h, x:x+w]
        
        # Resize to normalized size maintaining aspect ratio
        car_scaled = cv2.resize(car_crop, (int(w * scale), int(h * scale)), 
                               interpolation=cv2.INTER_LANCZOS4)
        
        # Create output canvas
        canvas = np.zeros((OUTPUT_SIZE[1], OUTPUT_SIZE[0], 4), dtype=np.uint8)
        
        # Calculate paste position (center the scaled car)
        paste_x = center_x - car_scaled.shape[1] // 2
        paste_y = center_y - car_scaled.shape[0] // 2
        
        # Paste car onto canvas
        canvas[paste_y:paste_y+car_scaled.shape[0], 
               paste_x:paste_x+car_scaled.shape[1]] = car_scaled
        
        # Save normalized frame
        output_path = output_folder / frame_path.name
        cv2.imwrite(str(output_path), canvas)
        success += 1
        
        if i % 10 == 0:
            print(f"Processed {i}/{len(frame_files)} frames...")
    
    print(f"\nNormalization complete!")
    print(f"Successfully normalized {success}/{len(frame_files)} frames")
    print(f"All frames are now {OUTPUT_SIZE[0]}x{OUTPUT_SIZE[1]} pixels")
    print(f"Car is perfectly centered in every frame")

if __name__ == '__main__':
    main()
