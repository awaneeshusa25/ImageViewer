import cv2
import numpy as np
from pathlib import Path

# Let's check the actual positions in our "stable" frames
FOLDER = 'car_frames_stable'
OUTPUT_FILE = 'frame_analysis.txt'

def analyze_frame(frame_path):
    """Analyze where the car actually is in a frame"""
    img = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
    
    if img is None or img.shape[2] != 4:
        return None
    
    alpha = img[:, :, 3]
    
    # Find all non-zero pixels
    y_coords, x_coords = np.where(alpha > 0)
    
    if len(x_coords) == 0:
        return None
    
    # Calculate statistics
    min_x, max_x = x_coords.min(), x_coords.max()
    min_y, max_y = y_coords.min(), y_coords.max()
    
    # Center of mass
    weights = alpha[alpha > 0].astype(float)
    center_x = int(np.average(x_coords, weights=weights))
    center_y = int(np.average(y_coords, weights=weights))
    
    # Bounding box
    bbox_w = max_x - min_x + 1
    bbox_h = max_y - min_y + 1
    
    return {
        'center': (center_x, center_y),
        'bbox': (min_x, min_y, max_x, max_y),
        'width': bbox_w,
        'height': bbox_h
    }

def main():
    folder = Path(FOLDER)
    frame_files = sorted(folder.glob('frame_*.png'))[:10]  # Check first 10 frames
    
    print("Analyzing frame positions...")
    print("=" * 80)
    
    results = []
    for frame_path in frame_files:
        info = analyze_frame(frame_path)
        if info:
            results.append((frame_path.name, info))
            print(f"{frame_path.name}:")
            print(f"  Center: {info['center']}")
            print(f"  BBox: ({info['bbox'][0]}, {info['bbox'][1]}) to ({info['bbox'][2]}, {info['bbox'][3]})")
            print(f"  Size: {info['width']}x{info['height']}")
            print()
    
    # Check variance
    if len(results) > 1:
        centers = [r[1]['center'] for r in results]
        center_xs = [c[0] for c in centers]
        center_ys = [c[1] for c in centers]
        
        print("=" * 80)
        print("VARIANCE ANALYSIS:")
        print(f"Center X range: {min(center_xs)} to {max(center_xs)} (variance: {max(center_xs) - min(center_xs)} pixels)")
        print(f"Center Y range: {min(center_ys)} to {max(center_ys)} (variance: {max(center_ys) - min(center_ys)} pixels)")
        print()
        
        if max(center_xs) - min(center_xs) > 5 or max(center_ys) - min(center_ys) > 5:
            print("❌ PROBLEM DETECTED: Car centers vary by more than 5 pixels!")
        else:
            print("✓ Car centers are well-aligned (< 5 pixel variance)")

if __name__ == '__main__':
    main()
