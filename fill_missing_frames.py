from pathlib import Path
import shutil

# Directories
output_dir = Path("car_frames_nobg")

# Get list of existing frames
existing_frames = set()
for png_file in output_dir.glob("frame_*.png"):
    frame_num = int(png_file.stem.split('_')[1])
    existing_frames.add(frame_num)

print(f"📊 Found {len(existing_frames)} existing frames with background removed")
print(f"🔧 Filling gaps by duplicating nearby frames...\n")

# Fill missing frames
filled_count = 0
for frame_num in range(1, 78):
    output_path = output_dir / f"frame_{str(frame_num).zfill(3)}.png"
    
    if frame_num in existing_frames:
        print(f"✓ Frame {frame_num}: Already exists")
    else:
        # Find nearest existing frame
        nearest_frame = None
        min_distance = float('inf')
        
        for existing in existing_frames:
            distance = abs(existing - frame_num)
            if distance < min_distance:
                min_distance = distance
                nearest_frame = existing
        
        if nearest_frame:
            source_path = output_dir / f"frame_{str(nearest_frame).zfill(3)}.png"
            shutil.copy(source_path, output_path)
            print(f"📋 Frame {frame_num}: Copied from frame {nearest_frame} (distance: {min_distance})")
            filled_count += 1

print(f"\n{'='*60}")
print(f"✅ Complete! Filled {filled_count} missing frames")
print(f"📊 Total frames now: {len(list(output_dir.glob('frame_*.png')))} / 77")
print(f"{'='*60}")
