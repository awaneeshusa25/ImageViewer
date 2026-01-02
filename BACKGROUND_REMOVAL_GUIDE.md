# Background Removal Guide for Car Frames

## Option 1: Remove.bg (Recommended for Quality)

### Online Bulk Processing
1. **Visit:** https://www.remove.bg/
2. **Sign up** for a free account (includes 1 free preview)
3. **Bulk Upload:**
   - Go to https://www.remove.bg/upload
   - Upload multiple images (up to 50 at once with paid plan)
   - Download all processed images

### Pricing (as of 2026)
- Free: 1 preview credit
- Subscription: $9/month for 40 credits
- Pay-as-you-go: Available

### Using Remove.bg API (Automated)
```bash
# Install remove.bg API
pip install removebg

# Set your API key
export REMOVEBG_API_KEY="your-api-key-here"

# Process all frames
python remove_bg_api.py
```

## Option 2: PhotoRoom (Free Alternative)

### Online Service
1. **Visit:** https://www.photoroom.com/tools/background-remover
2. **Features:**
   - Free unlimited background removal
   - Batch processing available
   - High quality results
3. **Upload** your car frames
4. **Download** processed images

## Option 3: Photopea (Free Photoshop Alternative)

### Online Editor
1. **Visit:** https://www.photopea.com/
2. **Open** your first frame
3. **Create an Action** to record steps:
   - Select → Subject (AI selection)
   - Select → Inverse
   - Delete background
   - Export as PNG
4. **Batch Process:**
   - File → Scripts → Load Files into Stack
   - Apply action to all layers
   - Export all

## Option 4: GIMP with BIMP Plugin (100% Free)

### Download & Install
1. **GIMP:** https://www.gimp.org/downloads/
2. **BIMP Plugin:** https://alessandrofrancesconi.it/projects/bimp/

### Batch Processing Steps
1. Open GIMP
2. Filters → Batch Image Manipulation
3. Add your 77 frames
4. Add manipulation: Select by Color → Delete
5. Export all as PNG with transparency

## Option 5: Python with CV2 (Advanced)

### For Technical Users
```python
import cv2
import numpy as np
from pathlib import Path

def remove_bg_simple(image_path, output_path):
    # Read image
    img = cv2.imread(str(image_path))
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to separate subject from background
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Create transparent background
    b, g, r = cv2.split(img)
    rgba = [b, g, r, mask]
    img_rgba = cv2.merge(rgba, 4)
    
    # Save
    cv2.imwrite(str(output_path), img_rgba)

# Process all frames
input_dir = Path("car_frames")
output_dir = Path("car_frames_nobg")
output_dir.mkdir(exist_ok=True)

for frame in sorted(input_dir.glob("frame_*.jpg")):
    output = output_dir / (frame.stem + ".png")
    remove_bg_simple(frame, output)
    print(f"Processed: {frame.name}")
```

## Current Workaround: Pure White Studio Background

The CSS has been optimized to show a clean white studio background:
- Pure white base color
- Subtle studio lighting gradient
- Minimal shadows (8px with 8% opacity)
- Professional showroom appearance

Even without removing backgrounds from source images, the viewer now looks professional and clean!

## Recommendations

### For Best Results:
1. **Small batches (< 10 images):** Use remove.bg or PhotoRoom online
2. **Large batches (77 frames):** Use remove.bg API with subscription
3. **Budget option:** Use Photopea or GIMP + BIMP
4. **Good enough:** Keep current CSS optimization (already done!)

### Next Steps:
1. Try remove.bg with a few sample frames to test quality
2. If satisfied, process all 77 frames
3. Save processed frames as `car_frames_nobg/frame_XXX.png`
4. Update script.js to load from the new folder
5. Done!
