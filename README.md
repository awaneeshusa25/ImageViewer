# 360° Image Viewer Application

A beautiful, interactive 360-degree panoramic image viewer built with HTML, CSS, and JavaScript using the Pannellum library.

## Features

✨ **Interactive Controls**
- Drag to look around the panorama
- Scroll to zoom in/out
- Double-click for fullscreen mode
- Auto-rotate functionality
- Reset view button

🖼️ **Image Upload**
- Load your own 360° panoramic images
- Supports all standard image formats (JPG, PNG, etc.)
- Drag-and-drop support

⌨️ **Keyboard Shortcuts**
- `F` - Toggle fullscreen
- `A` - Toggle auto-rotate
- `R` - Reset view

📱 **Responsive Design**
- Works on desktop, tablet, and mobile devices
- Touch gesture support for mobile viewing

## Getting Started

### Quick Start

1. Simply open `index.html` in a web browser
2. The viewer will load with a sample panorama
3. Click "Load 360° Image" to upload your own image

### Using Your Own 360° Images

The application works best with **equirectangular 360° panoramic images**. These images have:
- 2:1 aspect ratio (e.g., 4096x2048 pixels)
- Full spherical coverage
- Equirectangular projection

#### Where to Get 360° Images

1. **Take Your Own Photos:**
   - Use a 360° camera (Ricoh Theta, Insta360, etc.)
   - Use a smartphone with 360° photo apps
   - Stitch multiple photos using software like PTGui or Hugin

2. **Download Sample Images:**
   - [Pannellum Examples](https://pannellum.org/images/)
   - [Flickr 360° Photos](https://www.flickr.com/groups/equirectangular/)
   - Google Street View panoramas

3. **Create Panoramas:**
   - Use panorama stitching software
   - Use Photoshop's Photomerge feature
   - Use free tools like Hugin

### How to Use

1. **Navigate the View:**
   - Click and drag to look around
   - Use mouse wheel to zoom in/out
   - Arrow keys for fine control

2. **Upload Your Image:**
   - Click the "Load 360° Image" button
   - Select your equirectangular panorama
   - The viewer will automatically load it

3. **Use Controls:**
   - 🔲 Fullscreen button (top right)
   - 🔄 Auto-rotate button (top right)
   - ↺ Reset view button (top right)

## Technical Details

### Technologies Used

- **HTML5** - Structure
- **CSS3** - Styling with modern gradients and animations
- **JavaScript (ES6)** - Functionality
- **Pannellum** - 360° panorama viewer library

### Browser Compatibility

Works on all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

### File Structure

```
360 imageViewerApplication/
├── index.html          # Main HTML file
├── style.css          # Stylesheet
├── script.js          # JavaScript functionality
└── README.md          # This file
```

## Customization

### Change Default Image

Edit `script.js` and modify the `DEFAULT_IMAGE` variable:

```javascript
const DEFAULT_IMAGE = 'path/to/your/image.jpg';
```

### Adjust Viewer Settings

In `script.js`, you can customize the viewer by modifying the pannellum options:

```javascript
viewer = pannellum.viewer('panorama', {
    hfov: 100,              // Initial horizontal field of view
    minHfov: 50,            // Minimum zoom level
    maxHfov: 120,           // Maximum zoom level
    autoRotate: false,      // Enable auto-rotate on load
    // ... more options
});
```

### Styling

Modify `style.css` to change:
- Color scheme (currently purple/blue gradient)
- Button styles
- Layout and spacing
- Font choices

## Tips for Best Results

1. **Image Quality:**
   - Use high-resolution images (4K or higher)
   - Ensure proper exposure and lighting
   - Avoid visible stitching errors

2. **Performance:**
   - Large images may take longer to load
   - Compress images for web use
   - Recommended size: 4096x2048 to 8192x4096 pixels

3. **Creating Panoramas:**
   - Overlap photos by 30-50% when stitching
   - Use a tripod for better results
   - Shoot in RAW format for better editing

## Troubleshooting

**Image won't load:**
- Ensure the image is in a supported format (JPG, PNG)
- Check that the image is equirectangular projection
- Try a smaller file size

**Viewer is laggy:**
- Use a smaller image size
- Close other browser tabs
- Try a different browser

**Mobile touch not working:**
- Ensure you're using a modern mobile browser
- Try refreshing the page
- Check that JavaScript is enabled

## License

Free to use for personal and commercial projects.

## Credits

Built with [Pannellum](https://pannellum.org/) - A lightweight, free, and open-source panorama viewer for the web.

---

Enjoy exploring your 360° panoramas! 🌍✨
