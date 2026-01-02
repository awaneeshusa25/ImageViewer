import cv2
import numpy as np
from pathlib import Path

INPUT_FOLDER = 'car_frames_nobg'
OUTPUT_FOLDER = 'car_frames_final'
CANVAS_SIZE = (800, 600)
EXACT_CAR_SIZE = (480, 360)  # Every car will be EXACTLY this size
EXACT_CAR_POSITION = (160, 120)  # Every car top-left corner at this exact position

def get_car_bbox(image):
    """Get tight bounding box"""
    if image.shape[2] != 4:
        return None
    
    alpha = image[:, :, 3]
    coords = cv2.findNonZero(alpha)
    
    if coords is None:
        return None
    
    return cv2.boundingRect(coords)

def main():
    input_folder = Path(INPUT_FOLDER)
    output_folder = Path(OUTPUT_FOLDER)
    output_folder.mkdir(exist_ok=True)
    
    frame_files = sorted(input_folder.glob('frame_*.png'))
    
    print(f"Creating FINAL frames with ABSOLUTE positioning...")
    print(f"Canvas: {CANVAS_SIZE}")
    print(f"EVERY car will be: {EXACT_CAR_SIZE}")
    print(f"EVERY car positioned at: {EXACT_CAR_POSITION}")
    print()
    
    success = 0
    for i, frame_path in enumerate(frame_files, 1):
        img = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
        
        if img is None:
            continue
        
        bbox = get_car_bbox(img)
        if bbox is None:
            continue
        
        x, y, w, h = bbox
        
        # Crop car
        car = img[y:y+h, x:x+w]
        
        # Resize to EXACT size - every single car will be identical dimensions
        car_resized = cv2.resize(car, EXACT_CAR_SIZE, interpolation=cv2.INTER_LANCZOS4)
        
        # Create canvas
        canvas = np.zeros((CANVAS_SIZE[1], CANVAS_SIZE[0], 4), dtype=np.uint8)
        
        # Place at EXACT position - no calculations, no center-of-mass, just exact placement
        paste_x = EXACT_CAR_POSITION[0]
        paste_y = EXACT_CAR_POSITION[1]
        
        canvas[paste_y:paste_y+EXACT_CAR_SIZE[1], 
               paste_x:paste_x+EXACT_CAR_SIZE[0]] = car_resized
        
        # Save
        output_path = output_folder / frame_path.name
        cv2.imwrite(str(output_path), canvas)
        success += 1
        
        if i % 10 == 0:
            print(f"✓ {i}/{len(frame_files)} frames")
    
    print(f"\n✅ DONE!")
    print(f"All {success} cars are now:")
    print(f"   - EXACTLY {EXACT_CAR_SIZE[0]}x{EXACT_CAR_SIZE[1]} pixels")
    print(f"   - EXACTLY at position ({EXACT_CAR_POSITION[0]}, {EXACT_CAR_POSITION[1]})")
    print(f"   - ZERO variation between frames")

if __name__ == '__main__':
    main()
