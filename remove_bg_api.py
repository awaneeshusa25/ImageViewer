import requests
from pathlib import Path
import time

# Configuration
API_KEY = "iaz2fWbNrcugK9z4vr4gcHak"
API_URL = "https://api.remove.bg/v1.0/removebg"

# Directories
input_dir = Path("car_frames")
output_dir = Path("car_frames_nobg")
output_dir.mkdir(exist_ok=True)

# Get all frame files
frame_files = sorted(input_dir.glob("frame_*.jpg"))

print(f"🚀 Starting Remove.bg API Processing")
print(f"📁 Found {len(frame_files)} frames to process")
print(f"🔑 Using API key: {API_KEY[:10]}...")
print(f"📂 Output folder: {output_dir}\n")

success_count = 0
failed_files = []

for i, frame_path in enumerate(frame_files, 1):
    output_path = output_dir / (frame_path.stem + ".png")
    
    # Skip if already processed
    if output_path.exists():
        print(f"⏭️  {i}/{len(frame_files)}: {frame_path.name} (already exists)")
        success_count += 1
        continue
    
    try:
        print(f"🔄 {i}/{len(frame_files)}: Processing {frame_path.name}...", end=" ", flush=True)
        
        # Open and read the image file
        with open(frame_path, 'rb') as img_file:
            # Make API request with retry logic
            response = requests.post(
                API_URL,
                files={'image_file': img_file},
                data={'size': 'auto'},
                headers={'X-Api-Key': API_KEY},
                timeout=60
            )
        
        # Check if successful
        if response.status_code == 200:
            # Save the result
            with open(output_path, 'wb') as out_file:
                out_file.write(response.content)
            print(f"✅ Done!")
            success_count += 1
        else:
            error_msg = response.json().get('errors', [{}])[0].get('title', 'Unknown error')
            print(f"❌ Failed: {error_msg}")
            failed_files.append((frame_path.name, error_msg))
        
        # Rate limiting: wait a bit between requests
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        failed_files.append((frame_path.name, str(e)))

# Summary
print(f"\n{'='*60}")
print(f"✅ Successfully processed: {success_count}/{len(frame_files)} frames")
print(f"❌ Failed: {len(failed_files)} frames")

if failed_files:
    print(f"\n⚠️  Failed files:")
    for filename, error in failed_files:
        print(f"   - {filename}: {error}")

print(f"\n📂 Output saved to: {output_dir.absolute()}")
print(f"{'='*60}")

if success_count == len(frame_files):
    print("\n🎉 All frames processed successfully!")
    print("👉 Ready to update the viewer to use background-free images!")
