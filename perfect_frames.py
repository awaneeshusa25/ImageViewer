import cv2
import numpy as np
from pathlib import Path

INPUT_FOLDER = 'car_frames_nobg'
OUTPUT_FOLDER = 'car_frames_perfect'
OUTPUT_SIZE = (800, 600)
TARGET_CAR_SIZE = (500, 400)  # Fixed car size for all frames

def get_car_info(image):
    """Get car bounding box and center"""
    if image.shape[2] != 4:
        return None, None
    
    alpha = image[:, :, 3]
    coords = cv2.findNonZero(alpha)
    
    if coords is None:
        return None, None
    
    bbox = cv2.boundingRect(coords)
    
    # Calculate center of mass
    y_coords, x_coords = np.where(alpha > 0)
    weights = alpha[alpha > 0].astype(float)
    center_x = int(np.average(x_coords, weights=weights))
    center_y = int(np.average(y_coords, weights=weights))
    
    return bbox, (center_x, center_y)

def main():
    input_folder = Path(INPUT_FOLDER)
    output_folder = Path(OUTPUT_FOLDER)
    output_folder.mkdir(exist_ok=True)
    
    frame_files = sorted(input_folder.glob('frame_*.png'))
    
    if not frame_files:
        print("No frames found!")
        return
    
    print(f"Creating perfectly normalized frames...")
    print(f"Output size: {OUTPUT_SIZE}")
    print(f"Fixed car size: {TARGET_CAR_SIZE}")
    
    # Target center on canvas
    canvas_center_x = OUTPUT_SIZE[0] // 2
    canvas_center_y = OUTPUT_SIZE[1] // 2
    
    print(f"Car will be centered at: ({canvas_center_x}, {canvas_center_y})")
    
    success = 0
    for i, frame_path in enumerate(frame_files, 1):
        img = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
        
        if img is None:
            print(f"Failed: {frame_path.name}")
            continue
        
        bbox, center = get_car_info(img)
        
        if bbox is None or center is None:
            print(f"No car: {frame_path.name}")
            continue
        
        x, y, w, h = bbox
        
        # Crop car
        car_crop = img[y:y+h, x:x+w]
        
        # Calculate center offset within the crop
        offset_x = center[0] - x
        offset_y = center[1] - y
        
        # Resize car to target size while maintaining aspect ratio
        aspect = w / h
        target_aspect = TARGET_CAR_SIZE[0] / TARGET_CAR_SIZE[1]
        
        if aspect > target_aspect:
            # Width is limiting factor
            new_w = TARGET_CAR_SIZE[0]
            new_h = int(TARGET_CAR_SIZE[0] / aspect)
        else:
            # Height is limiting factor
            new_h = TARGET_CAR_SIZE[1]
            new_w = int(TARGET_CAR_SIZE[1] * aspect)
        
        car_resized = cv2.resize(car_crop, (new_w, new_h), 
                                interpolation=cv2.INTER_LANCZOS4)
        
        # Calculate where center of mass is in resized image
        scale_x = new_w / w
        scale_y = new_h / h
        resized_center_x = int(offset_x * scale_x)
        resized_center_y = int(offset_y * scale_y)
        
        # Create canvas
        canvas = np.zeros((OUTPUT_SIZE[1], OUTPUT_SIZE[0], 4), dtype=np.uint8)
        
        # Calculate paste position so center of mass is at canvas center
        paste_x = canvas_center_x - resized_center_x
        paste_y = canvas_center_y - resized_center_y
        
        # Paste with clipping if needed
        if paste_x >= 0 and paste_y >= 0 and \
           paste_x + new_w <= OUTPUT_SIZE[0] and \
           paste_y + new_h <= OUTPUT_SIZE[1]:
            canvas[paste_y:paste_y+new_h, paste_x:paste_x+new_w] = car_resized
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
                canvas[dst_y1:dst_y2, dst_x1:dst_x2] = car_resized[src_y1:src_y2, src_x1:src_x2]
        
        # Save
        output_path = output_folder / frame_path.name
        cv2.imwrite(str(output_path), canvas)
        success += 1
        
        if i % 10 == 0:
            print(f"Processed {i}/{len(frame_files)}...")
    
    print(f"\nPerfect normalization complete!")
    print(f"All {success} frames now have:")
    print(f"- Same canvas size: {OUTPUT_SIZE}")
    print(f"- Same car dimensions (aspect-ratio preserved)")
    print(f"- Same center position: ({canvas_center_x}, {canvas_center_y})")

if __name__ == '__main__':
    main()
