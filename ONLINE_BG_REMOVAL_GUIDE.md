# Online Background Removal - Step-by-Step Guide

## 🎯 Best Option: Remove.bg

### Method 1: Free Account (Quickest)
1. **Visit**: https://www.remove.bg/
2. **Sign Up**: Create a free account (email + password)
3. **Upload Images**:
   - Click "Upload Image"
   - Select your `car_frames` folder
   - Choose multiple files (Ctrl+A to select all 77 frames)
4. **Download**:
   - Download each processed image
   - Or upgrade for bulk download feature

**Limitations**: 
- Free: 1 preview credit/month, low-res downloads
- For 77 frames: Need paid plan

### Method 2: Remove.bg API (Paid - Best for 77 frames)
**Cost**: $9/month for 40 credits OR $0.20 per image (bulk: $0.09/image)

1. **Get API Key**:
   - Sign up at https://www.remove.bg/users/sign_up
   - Go to https://www.remove.bg/api
   - Get your API key

2. **Install Tool**:
   ```powershell
   pip install removebg
   ```

3. **Run Batch Processing**:
   ```powershell
   # Set API key (replace with your key)
   $env:REMOVEBG_API_KEY="your-api-key-here"
   
   # Process all frames
   python remove_bg_batch.py
   ```

---

## 🎨 Alternative 1: Pixlr (Free & Unlimited)

### Best Free Option!
1. **Visit**: https://pixlr.com/remove-background/
2. **Features**:
   - ✅ Completely FREE
   - ✅ No signup required
   - ✅ Unlimited usage
   - ✅ High quality AI removal

3. **Process**:
   - Upload one frame at a time
   - Click "Remove Background"
   - Download PNG with transparency
   - Repeat for all 77 frames

4. **Batch Tip**:
   - Open multiple browser tabs
   - Upload different frames in each tab
   - Process in parallel for speed

---

## 🔥 Alternative 2: Adobe Express (Free)

### High Quality, Free
1. **Visit**: https://www.adobe.com/express/feature/image/remove-background
2. **Sign In**: Free Adobe account required
3. **Upload & Process**:
   - Drag & drop images
   - Automatic background removal
   - Download as PNG
4. **Quality**: Excellent (Adobe's AI)

---

## 📸 Alternative 3: PhotoRoom (Freemium)

### Mobile & Desktop
1. **Visit**: https://www.photoroom.com/background-remover
2. **Features**:
   - Free tier available
   - Batch processing (paid)
   - Very good quality
3. **Process**: Upload → Remove → Download

---

## 📋 Step-by-Step: Using Pixlr (Recommended Free Method)

### For Your 77 Car Frames:

**Step 1: Prepare Workspace**
```powershell
# Create output folder
New-Item -ItemType Directory -Path "car_frames_nobg" -Force
```

**Step 2: Process Frames**
1. Open Pixlr: https://pixlr.com/remove-background/
2. Upload `car_frames/frame_001.jpg`
3. Wait for automatic processing (5-10 seconds)
4. Click "Download"
5. Save to `car_frames_nobg/frame_001.png`
6. Repeat for all 77 frames

**Pro Tip**: Open 5-10 tabs simultaneously to process faster!

**Step 3: Update Your Code**
Once all frames are processed, I'll update your code to use the new background-free images.

---

## 💰 Cost Comparison

| Service | Free Tier | Paid Plan | Quality | Speed |
|---------|-----------|-----------|---------|-------|
| **Pixlr** | ✅ Unlimited | N/A | ⭐⭐⭐⭐ | Manual |
| **Remove.bg** | 1 credit/mo | $9/40 credits | ⭐⭐⭐⭐⭐ | Fast |
| **Adobe Express** | ✅ Limited | $10/month | ⭐⭐⭐⭐⭐ | Manual |
| **PhotoRoom** | ✅ Limited | $9/month | ⭐⭐⭐⭐ | Fast |

---

## 🚀 Quick Start Recommendation

**For 77 frames, here's my recommendation:**

### Option A: Budget (Free)
Use **Pixlr** in multiple browser tabs:
- Time: ~30-45 minutes
- Cost: $0
- Quality: Very good

### Option B: Premium (Best Quality)
Use **Remove.bg API**:
- Time: ~5 minutes
- Cost: ~$6.93 (77 × $0.09)
- Quality: Excellent

### Option C: Middle Ground
Use **Adobe Express** free tier:
- Time: ~30-45 minutes  
- Cost: $0
- Quality: Excellent

---

## 📝 After Processing

Once you have all 77 background-free PNG files in `car_frames_nobg/`:

**Tell me and I'll:**
1. Update `script.js` to use the new folder
2. Update `index.html` to load PNG files
3. Test the viewer with transparent backgrounds
4. Commit changes to GitHub

---

## ❓ Which Service Should You Use?

**Choose based on your priority:**

- 🆓 **Want it free?** → Use **Pixlr** (unlimited, no signup)
- ⚡ **Want it fast?** → Pay for **Remove.bg API** ($6.93)
- 🎨 **Want best quality?** → Use **Adobe Express** (free, slow)
- 📱 **Prefer mobile?** → Use **PhotoRoom app**

---

## 🛠️ Need Help?

Let me know which service you choose, and I can:
- Help set up API keys (if using remove.bg API)
- Create automation scripts
- Update the code once frames are processed
- Test the final result

**Ready to start?** Pick a service and let me know if you need any assistance!
