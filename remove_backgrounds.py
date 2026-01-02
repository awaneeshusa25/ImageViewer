from PIL import Image
import os
from pathlib import Path

# Simple approach: Convert images to PNG with transparency
# This won't remove the background automatically, but prepares for manual editing

input_dir = Path("car_frames")
output_dir = Path("car_frames_png")

# Create output directory
output_dir.mkdir(exist_ok=True)

# Get all frame files
frame_files = sorted([f for f in input_dir.glob("frame_*.jpg")])

print(f"Converting {len(frame_files)} frames to PNG format...")
print("Note: For automatic background removal, you'll need to use an online tool")
print("like remove.bg or a professional image editor.\n")

for i, frame_path in enumerate(frame_files, 1):
    print(f"Converting {i}/{len(frame_files)}: {frame_path.name}")
    
    # Read and convert to PNG
    img = Image.open(frame_path)
    output_path = output_dir / frame_path.stem + ".png"
    img.save(output_path, "PNG")

print(f"\n✅ Converted to PNG format in: {output_dir}")
print("\nFor background removal, I recommend:")
print("1. Use remove.bg website (bulk processing)")
print("2. Use Photoshop/GIMP with batch processing")
print("3. Use online AI background removers")

