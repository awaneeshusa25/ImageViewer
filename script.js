// Default 360 image URL (using a sample panorama)
const DEFAULT_IMAGE = 'https://pannellum.org/images/alma.jpg';

let viewer;
let isAutoRotating = false;

// Initialize the panorama viewer
function initViewer(imageUrl) {
    const loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.classList.add('active');

    // Destroy existing viewer if it exists
    if (viewer) {
        viewer.destroy();
    }

    // Create new viewer
    viewer = pannellum.viewer('panorama', {
        type: 'equirectangular',
        panorama: imageUrl,
        autoLoad: true,
        showControls: true,
        showFullscreenCtrl: false,
        showZoomCtrl: true,
        mouseZoom: true,
        doubleClickZoom: true,
        draggable: true,
        keyboardZoom: true,
        friction: 0.15,
        hfov: 100,
        minHfov: 50,
        maxHfov: 120,
        pitch: 0,
        yaw: 0,
        autoRotate: false,
        autoRotateInactivityDelay: 3000,
        autoRotateStopDelay: 5000,
        compass: false,
        northOffset: 0,
        hotSpotDebug: false,
    });

    // Hide loading indicator when loaded
    viewer.on('load', function() {
        setTimeout(() => {
            loadingIndicator.classList.remove('active');
        }, 500);
    });

    // Error handling
    viewer.on('error', function(err) {
        loadingIndicator.classList.remove('active');
        console.error('Error loading panorama:', err);
        alert('Error loading the panorama. Please try a different image.');
    });
}

// Initialize with default image
initViewer(DEFAULT_IMAGE);

// Fullscreen button
document.getElementById('fullscreenBtn').addEventListener('click', function() {
    if (viewer) {
        viewer.toggleFullscreen();
    }
});

// Auto-rotate button
document.getElementById('autoRotateBtn').addEventListener('click', function() {
    if (viewer) {
        isAutoRotating = !isAutoRotating;
        
        if (isAutoRotating) {
            viewer.setAutoRotate(2); // Rotation speed
            this.style.background = '#667eea';
            this.style.color = 'white';
        } else {
            viewer.setAutoRotate(false);
            this.style.background = 'rgba(255, 255, 255, 0.95)';
            this.style.color = '#667eea';
        }
    }
});

// Reset view button
document.getElementById('resetBtn').addEventListener('click', function() {
    if (viewer) {
        viewer.setPitch(0);
        viewer.setYaw(0);
        viewer.setHfov(100);
        
        // Stop auto-rotate
        if (isAutoRotating) {
            isAutoRotating = false;
            viewer.setAutoRotate(false);
            document.getElementById('autoRotateBtn').style.background = 'rgba(255, 255, 255, 0.95)';
            document.getElementById('autoRotateBtn').style.color = '#667eea';
        }
    }
});

// Image upload handler
document.getElementById('imageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    
    if (file) {
        // Check if it's an image
        if (!file.type.startsWith('image/')) {
            alert('Please select a valid image file.');
            return;
        }

        // Create URL for the uploaded image
        const imageUrl = URL.createObjectURL(file);
        
        // Load the new panorama
        initViewer(imageUrl);
        
        // Reset input
        e.target.value = '';
    }
});

// Double-click for fullscreen
document.getElementById('panorama').addEventListener('dblclick', function() {
    if (viewer) {
        viewer.toggleFullscreen();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (!viewer) return;

    switch(e.key) {
        case 'f':
        case 'F':
            viewer.toggleFullscreen();
            break;
        case 'r':
        case 'R':
            document.getElementById('resetBtn').click();
            break;
        case 'a':
        case 'A':
            document.getElementById('autoRotateBtn').click();
            break;
    }
});

// Add touch gesture support
let touchStartX = 0;
let touchStartY = 0;

document.getElementById('panorama').addEventListener('touchstart', function(e) {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
});

document.getElementById('panorama').addEventListener('touchmove', function(e) {
    if (!viewer) return;

    const touchEndX = e.touches[0].clientX;
    const touchEndY = e.touches[0].clientY;

    const deltaX = touchEndX - touchStartX;
    const deltaY = touchEndY - touchStartY;

    // Update viewer based on touch movement
    const currentYaw = viewer.getYaw();
    const currentPitch = viewer.getPitch();

    viewer.setYaw(currentYaw - deltaX * 0.1);
    viewer.setPitch(currentPitch + deltaY * 0.1);

    touchStartX = touchEndX;
    touchStartY = touchEndY;
});

// Log viewer info
console.log('%c360° Image Viewer Ready! 🎉', 'color: #667eea; font-size: 16px; font-weight: bold;');
console.log('Keyboard shortcuts:');
console.log('  F - Toggle fullscreen');
console.log('  A - Toggle auto-rotate');
console.log('  R - Reset view');
