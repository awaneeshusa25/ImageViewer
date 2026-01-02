import cv2
import numpy as np
from pathlib import Path

# Configuration
INPUT_FOLDER = 'car_frames_nobg'
OUTPUT_FOLDER = 'car_frames_fixed'
OUTPUT_SIZE = (800, 600)

def get_car_center_of_mass(image):
    """Calculate center of mass of the car"""
    if image.shape[2] == 4:
        alpha = image[:, :, 3]
        # Weight by alpha channel
        y_coords, x_coords = np.where(alpha > 0)
        if len(x_coords) == 0:
            return None
        
        weights = alpha[alpha > 0].astype(float)
        cx = int(np.average(x_coords, weights=weights))
        cy = int(np.average(y_coords, weights=weights))
        return (cx, cy)
    return None

def get_car_bbox(image):
    """Get tight bounding box of the car"""
    if image.shape[2] == 4:
        alpha = image[:, :, 3]
        coords = cv2.findNonZero(alpha)
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
    
    print("Loading reference frame (frame 1)...")
    ref_img = cv2.imread(str(frame_files[0]), cv2.IMREAD_UNCHANGED)
    ref_center = get_car_center_of_mass(ref_img)
    ref_bbox = get_car_bbox(ref_img)
    
    if ref_center is None or ref_bbox is None:
        print("Could not detect car in reference frame!")
        return
    
    print(f"Reference center of mass: {ref_center}")
    
    # Determine target scale based on reference
    ref_x, ref_y, ref_w, ref_h = ref_bbox
    
    # Calculate maximum dimensions from all frames
    print("\nAnalyzing all frames to find consistent scale...")
    max_w, max_h = ref_w, ref_h
    
    for frame_path in frame_files[1:]:
        img = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
        bbox = get_car_bbox(img)
        if bbox:
            _, _, w, h = bbox
            max_w = max(max_w, w)
            max_h = max(max_h, h)
    
    # Calculate scale to fit with padding
    padding = 80
    scale_w = (OUTPUT_SIZE[0] - 2 * padding) / max_w
    scale_h = (OUTPUT_SIZE[1] - 2 * padding) / max_h
    scale = min(scale_w, scale_h)
    
    print(f"Consistent scale factor: {scale:.4f}")
    
    # Target center on canvas
    canvas_center = (OUTPUT_SIZE[0] // 2, OUTPUT_SIZE[1] // 2)
    print(f"Target center on canvas: {canvas_center}")
    
    print(f"\nProcessing {len(frame_files)} frames with pixel-perfect alignment...")
    
    for i, frame_path in enumerate(frame_files, 1):
        img = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
        
        if img is None:
            print(f"Failed to load: {frame_path.name}")
            continue
        
        # Get center of mass for this frame
        center = get_car_center_of_mass(img)
        bbox = get_car_bbox(img)
        
        if center is None or bbox is None:
            print(f"Could not detect car in: {frame_path.name}")
            continue
        
        # Crop car tightly
        x, y, w, h = bbox
        car_crop = img[y:y+h, x:x+w]
        
        # Calculate scaled dimensions
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        # Resize car
        car_scaled = cv2.resize(car_crop, (new_w, new_h), 
                               interpolation=cv2.INTER_LANCZOS4)
        
        # Calculate offset from crop corner to center of mass in original
        offset_x = center[0] - x
        offset_y = center[1] - y
        
        # Scale the offset
        scaled_offset_x = int(offset_x * scale)
        scaled_offset_y = int(offset_y * scale)
        
        # Create canvas
        canvas = np.zeros((OUTPUT_SIZE[1], OUTPUT_SIZE[0], 4), dtype=np.uint8)
        
        # Calculate paste position so center of mass aligns with canvas center
        paste_x = canvas_center[0] - scaled_offset_x
        paste_y = canvas_center[1] - scaled_offset_y
        
        # Ensure paste position is within bounds
        if paste_x >= 0 and paste_y >= 0 and \
           paste_x + new_w <= OUTPUT_SIZE[0] and \
           paste_y + new_h <= OUTPUT_SIZE[1]:
            canvas[paste_y:paste_y+new_h, paste_x:paste_x+new_w] = car_scaled
        else:
            # Handle edge case - center it
            paste_x = max(0, min(paste_x, OUTPUT_SIZE[0] - new_w))
            paste_y = max(0, min(paste_y, OUTPUT_SIZE[1] - new_h))
            
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
        
        if i % 10 == 0:
            print(f"Aligned {i}/{len(frame_files)} frames...")
    
    print(f"\nPrecise center-of-mass alignment complete!")
    print(f"All frames now have car's center of mass at pixel {canvas_center}")

if __name__ == '__main__':
    main()
