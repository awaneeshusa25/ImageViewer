import cv2
import numpy as np
from pathlib import Path

# Configuration
INPUT_FOLDER = 'car_frames_nobg'
OUTPUT_FOLDER = 'car_frames_aligned'
CANVAS_SIZE = (1200, 900)  # Fixed canvas size (width, height)

def get_car_bbox(image):
    """Get bounding box of the car (non-transparent pixels)"""
    if image.shape[2] == 4:  # Has alpha channel
        alpha = image[:, :, 3]
        # Find all non-transparent pixels
        coords = cv2.findNonZero(alpha)
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        coords = cv2.findNonZero(binary)
    
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        return x, y, w, h
    return None

def align_to_reference(image, ref_bbox, ref_center):
    """Align image to match reference bounding box center"""
    # Get bounding box of current image
    bbox = get_car_bbox(image)
    
    if bbox is None:
        # Return centered on canvas
        canvas = np.zeros((CANVAS_SIZE[1], CANVAS_SIZE[0], 4), dtype=np.uint8)
        return canvas
    
    x, y, w, h = bbox
    
    # Calculate current center
    curr_center_x = x + w // 2
    curr_center_y = y + h // 2
    
    # Calculate offset needed to match reference center
    offset_x = ref_center[0] - curr_center_x
    offset_y = ref_center[1] - curr_center_y
    
    # Create canvas
    canvas = np.zeros((CANVAS_SIZE[1], CANVAS_SIZE[0], 4), dtype=np.uint8)
    
    # Calculate canvas center
    canvas_center_x = CANVAS_SIZE[0] // 2
    canvas_center_y = CANVAS_SIZE[1] // 2
    
    # Calculate where to place the image on canvas
    paste_x = canvas_center_x - curr_center_x + offset_x - x
    paste_y = canvas_center_y - curr_center_y + offset_y - y
    
    # Calculate regions for copying
    src_x1 = max(0, -paste_x)
    src_y1 = max(0, -paste_y)
    src_x2 = min(image.shape[1], CANVAS_SIZE[0] - paste_x)
    src_y2 = min(image.shape[0], CANVAS_SIZE[1] - paste_y)
    
    dst_x1 = max(0, paste_x)
    dst_y1 = max(0, paste_y)
    dst_x2 = dst_x1 + (src_x2 - src_x1)
    dst_y2 = dst_y1 + (src_y2 - src_y1)
    
    # Copy image to canvas
    if src_x2 > src_x1 and src_y2 > src_y1:
        canvas[dst_y1:dst_y2, dst_x1:dst_x2] = image[src_y1:src_y2, src_x1:src_x2]
    
    return canvas

def main():
    input_folder = Path(INPUT_FOLDER)
    output_folder = Path(OUTPUT_FOLDER)
    output_folder.mkdir(exist_ok=True)
    
    # Get all PNG files
    frame_files = sorted(input_folder.glob('frame_*.png'))
    
    if not frame_files:
        print(f"No frame files found in {INPUT_FOLDER}")
        return
    
    print(f"Processing {len(frame_files)} frames with precise alignment...")
    
    # Load reference frame (first frame)
    print("Loading reference frame...")
    ref_img = cv2.imread(str(frame_files[0]), cv2.IMREAD_UNCHANGED)
    ref_bbox = get_car_bbox(ref_img)
    
    if ref_bbox is None:
        print("Could not detect car in reference frame!")
        return
    
    # Calculate reference center
    ref_x, ref_y, ref_w, ref_h = ref_bbox
    ref_center = (ref_x + ref_w // 2, ref_y + ref_h // 2)
    
    print(f"Reference car center: {ref_center}")
    print(f"Reference car size: {ref_w}x{ref_h}")
    
    # Process all frames
    success_count = 0
    for i, input_path in enumerate(frame_files, 1):
        img = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)
        
        if img is None:
            print(f"Failed to load: {input_path}")
            continue
        
        # Align to reference
        aligned = align_to_reference(img, ref_bbox, ref_center)
        
        # Save
        output_path = output_folder / input_path.name
        cv2.imwrite(str(output_path), aligned)
        success_count += 1
        
        if i % 10 == 0:
            print(f"Processed {i}/{len(frame_files)} frames...")
    
    print(f"\nPrecise alignment complete!")
    print(f"Successfully aligned {success_count}/{len(frame_files)} frames")
    print(f"All cars centered at the same position relative to reference frame")

if __name__ == '__main__':
    main()
