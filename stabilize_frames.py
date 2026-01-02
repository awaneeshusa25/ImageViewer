import cv2
import numpy as np
from pathlib import Path

# Configuration
INPUT_FOLDER = 'car_frames_nobg'
OUTPUT_FOLDER = 'car_frames_stable'
OUTPUT_SIZE = (800, 600)
REFERENCE_FRAME_NUM = 1  # Use first frame as absolute reference

def get_visual_center(image):
    """Find the visual center by detecting the strongest feature point"""
    if image.shape[2] == 4:
        # Convert to BGR for feature detection
        bgr = image[:, :, :3]
        alpha = image[:, :, 3]
        
        # Create mask from alpha
        mask = alpha > 0
        
        # Find contours
        contours, _ = cv2.findContours(alpha, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get the largest contour (the car)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get moments
            M = cv2.moments(largest_contour)
            
            if M["m00"] != 0:
                # Calculate centroid
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Get bounding rect
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Return both centroid and bbox
                return (cx, cy), (x, y, w, h)
    
    return None, None

def main():
    input_folder = Path(INPUT_FOLDER)
    output_folder = Path(OUTPUT_FOLDER)
    output_folder.mkdir(exist_ok=True)
    
    frame_files = sorted(input_folder.glob('frame_*.png'))
    
    if not frame_files:
        print(f"No frames found in {INPUT_FOLDER}")
        return
    
    print("Step 1: Loading reference frame...")
    ref_img = cv2.imread(str(frame_files[REFERENCE_FRAME_NUM - 1]), cv2.IMREAD_UNCHANGED)
    ref_center, ref_bbox = get_visual_center(ref_img)
    
    if ref_center is None or ref_bbox is None:
        print("Could not detect car in reference frame!")
        return
    
    ref_x, ref_y, ref_w, ref_h = ref_bbox
    
    print(f"Reference visual center: {ref_center}")
    print(f"Reference bbox: {ref_bbox}")
    
    # Calculate scale based on reference
    padding = 80
    scale_w = (OUTPUT_SIZE[0] - 2 * padding) / ref_w
    scale_h = (OUTPUT_SIZE[1] - 2 * padding) / ref_h
    scale = min(scale_w, scale_h)
    
    print(f"Scale factor: {scale:.4f}")
    
    # Target position on canvas (where reference center will be)
    target_x = OUTPUT_SIZE[0] // 2
    target_y = OUTPUT_SIZE[1] // 2
    
    print(f"\nStep 2: Processing all frames to match reference position...")
    print(f"Target position: ({target_x}, {target_y})")
    
    # Calculate reference transformation
    ref_scaled_center_x = int((ref_center[0] - ref_x) * scale)
    ref_scaled_center_y = int((ref_center[1] - ref_y) * scale)
    
    success = 0
    for i, frame_path in enumerate(frame_files, 1):
        img = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
        
        if img is None:
            print(f"Failed: {frame_path.name}")
            continue
        
        center, bbox = get_visual_center(img)
        
        if center is None or bbox is None:
            print(f"No car detected: {frame_path.name}")
            continue
        
        x, y, w, h = bbox
        
        # Crop the car
        car_crop = img[y:y+h, x:x+w]
        
        # Resize with same scale as reference
        new_w = int(w * scale)
        new_h = int(h * scale)
        car_scaled = cv2.resize(car_crop, (new_w, new_h), 
                               interpolation=cv2.INTER_LANCZOS4)
        
        # Calculate where this car's center is in the scaled image
        scaled_center_x = int((center[0] - x) * scale)
        scaled_center_y = int((center[1] - y) * scale)
        
        # Create canvas
        canvas = np.zeros((OUTPUT_SIZE[1], OUTPUT_SIZE[0], 4), dtype=np.uint8)
        
        # Calculate paste position to align centers
        # We want this car's center to be at the same position as reference center
        paste_x = target_x - ref_scaled_center_x
        paste_y = target_y - ref_scaled_center_y
        
        # Adjust paste position by the difference in car centers
        offset_x = ref_scaled_center_x - scaled_center_x
        offset_y = ref_scaled_center_y - scaled_center_y
        
        paste_x += offset_x
        paste_y += offset_y
        
        # Paste car onto canvas
        if paste_x >= 0 and paste_y >= 0 and \
           paste_x + new_w <= OUTPUT_SIZE[0] and \
           paste_y + new_h <= OUTPUT_SIZE[1]:
            canvas[paste_y:paste_y+new_h, paste_x:paste_x+new_w] = car_scaled
        else:
            # Handle clipping
            src_x1 = max(0, -paste_x)
            src_y1 = max(0, -paste_y)
            src_x2 = min(new_w, OUTPUT_SIZE[0] - paste_x)
            src_y2 = min(new_h, OUTPUT_SIZE[1] - paste_y)
            
            dst_x1 = max(0, paste_x)
            dst_y1 = max(0, paste_y)
            dst_x2 = dst_x1 + (src_x2 - src_x1)
            dst_y2 = dst_y1 + (src_y2 - src_y1)
            
            if src_x2 > src_x1 and src_y2 > src_y1:
                canvas[dst_y1:dst_y2, dst_x1:dst_x2] = car_scaled[src_y1:src_y2, src_x1:src_x2]
        
        # Save
        output_path = output_folder / frame_path.name
        cv2.imwrite(str(output_path), canvas)
        success += 1
        
        if i % 10 == 0:
            print(f"Processed {i}/{len(frame_files)}...")
    
    print(f"\nStable alignment complete!")
    print(f"Successfully processed {success}/{len(frame_files)} frames")
    print(f"All cars aligned to reference frame position")

if __name__ == '__main__':
    main()
