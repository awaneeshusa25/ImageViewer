// Car 360 Viewer Configuration
const totalFrames = 77; // Total number of frames extracted
const FRAME_FOLDER = 'car_frames_nobg'; // Professional background-removed frames
const FRAME_EXTENSION = 'png'; // PNG for transparency
let currentFrame = 1;
let isAutoRotating = false;
let autoRotateInterval;
let isDragging = false;
let startX = 0;
let currentX = 0;
let hasInteracted = false;

// Image cache to prevent flickering
const imageCache = {};

const carImage = document.getElementById('car-image');
const currentFrameDisplay = document.getElementById('current-frame');
const totalFramesDisplay = document.getElementById('total-frames');
const rotationHint = document.getElementById('rotation-hint');
const loadingOverlay = document.getElementById('loading-overlay');
const interactOverlay = document.getElementById('interact-overlay');

// Update total frames display
totalFramesDisplay.textContent = totalFrames;

// Preload all frames and show loading
let loadedFrames = 0;
const framesToPreload = totalFrames;

function preloadAllFrames() {
    for (let i = 1; i <= framesToPreload; i++) {
        const frameString = String(i).padStart(3, '0');
        const img = new Image();
        img.onload = () => {
            // Cache the loaded image
            imageCache[i] = img;
            loadedFrames++;
            if (loadedFrames === framesToPreload) {
                // All frames loaded, hide loading overlay
                setTimeout(() => {
                    loadingOverlay.classList.add('hidden');
                }, 500);
            }
        };
        img.src = `${FRAME_FOLDER}/frame_${frameString}.${FRAME_EXTENSION}`;
    }
}

// Start preloading on page load
preloadAllFrames();

// Handle interact overlay click
interactOverlay.addEventListener('click', () => {
    interactOverlay.classList.add('hidden');
    hasInteracted = true;
    // Start a gentle auto-rotation on first interaction
    setTimeout(() => {
        if (!isDragging && !isAutoRotating) {
            for (let i = 1; i <= 10; i++) {
                setTimeout(() => loadFrame(currentFrame + 1), i * 100);
            }
        }
    }, 300);
});

// Load specific frame
function loadFrame(frameNumber) {
    if (frameNumber < 1) frameNumber = totalFrames;
    if (frameNumber > totalFrames) frameNumber = 1;
    
    currentFrame = frameNumber;
    const frameString = String(frameNumber).padStart(3, '0');
    
    // Use cached image if available to prevent flickering
    if (imageCache[frameNumber]) {
        carImage.src = imageCache[frameNumber].src;
    } else {
        carImage.src = `${FRAME_FOLDER}/frame_${frameString}.${FRAME_EXTENSION}`;
    }
    
    currentFrameDisplay.textContent = currentFrame;
}

// Mouse events for dragging
carImage.parentElement.addEventListener('mousedown', (e) => {
    if (!hasInteracted) {
        interactOverlay.classList.add('hidden');
        hasInteracted = true;
    }
    isDragging = true;
    startX = e.clientX;
    if (rotationHint) {
        rotationHint.style.display = 'none';
    }
});

document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    
    currentX = e.clientX;
    const delta = currentX - startX;
    
    // Smoother sensitivity: move 3 pixels = 1 frame
    const frameDelta = Math.floor(delta / 3);
    
    if (Math.abs(frameDelta) >= 1) {
        let newFrame = currentFrame + frameDelta;
        loadFrame(newFrame);
        startX = currentX;
    }
});

document.addEventListener('mouseup', () => {
    isDragging = false;
});

// Touch events for mobile
carImage.parentElement.addEventListener('touchstart', (e) => {
    if (!hasInteracted) {
        interactOverlay.classList.add('hidden');
        hasInteracted = true;
    }
    isDragging = true;
    startX = e.touches[0].clientX;
    if (rotationHint) {
        rotationHint.style.display = 'none';
    }
});

carImage.parentElement.addEventListener('touchmove', (e) => {
    if (!isDragging) return;
    e.preventDefault();
    
    currentX = e.touches[0].clientX;
    const delta = currentX - startX;
    
    // Smoother touch sensitivity
    const frameDelta = Math.floor(delta / 3);
    
    if (Math.abs(frameDelta) >= 1) {
        let newFrame = currentFrame + frameDelta;
        loadFrame(newFrame);
        startX = currentX;
    }
});

carImage.parentElement.addEventListener('touchend', () => {
    isDragging = false;
});

// Auto-rotate button
document.getElementById('autoRotateBtn').addEventListener('click', function() {
    isAutoRotating = !isAutoRotating;
    
    if (isAutoRotating) {
        this.style.background = '#667eea';
        this.style.color = 'white';
        
        // Rotate through frames automatically
        autoRotateInterval = setInterval(() => {
            let nextFrame = currentFrame + 1;
            if (nextFrame > totalFrames) nextFrame = 1;
            loadFrame(nextFrame);
        }, 50); // Speed: 50ms per frame
    } else {
        this.style.background = 'rgba(255, 255, 255, 0.95)';
        this.style.color = '#667eea';
        clearInterval(autoRotateInterval);
    }
});

// Fullscreen button
document.getElementById('fullscreenBtn').addEventListener('click', function() {
    const viewerWrapper = document.querySelector('.viewer-wrapper');
    
    if (!document.fullscreenElement) {
        viewerWrapper.requestFullscreen().catch(err => {
            console.log('Fullscreen error:', err);
        });
    } else {
        document.exitFullscreen();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    switch(e.key) {
        case 'ArrowLeft':
            loadFrame(currentFrame - 1);
            break;
        case 'ArrowRight':
            loadFrame(currentFrame + 1);
            break;
        case 'f':
        case 'F':
            document.getElementById('fullscreenBtn').click();
            break;
        case 'a':
        case 'A':
            document.getElementById('autoRotateBtn').click();
            break;
    }
});

// Hide rotation hint after first interaction
setTimeout(() => {
    if (rotationHint) {
        rotationHint.style.opacity = '0';
        rotationHint.style.transition = 'opacity 1s';
        setTimeout(() => {
            rotationHint.style.display = 'none';
        }, 1000);
    }
}, 4000);

// Preload adjacent frames for smooth rotation
function preloadFrames() {
    // Preload more frames ahead and behind for ultra-smooth rotation
    for (let i = -5; i <= 5; i++) {
        let frameNum = currentFrame + i;
        if (frameNum < 1) frameNum += totalFrames;
        if (frameNum > totalFrames) frameNum -= totalFrames;
        
        // Only preload if not already cached
        if (!imageCache[frameNum]) {
            const frameString = String(frameNum).padStart(3, '0');
            const img = new Image();
            img.onload = () => {
                imageCache[frameNum] = img;
            };
            img.src = `${FRAME_FOLDER}/frame_${frameString}.${FRAME_EXTENSION}`;
        }
    }
}

// Preload initial frames
preloadFrames();

// Preload on frame change
carImage.addEventListener('load', preloadFrames);

console.log('%c360° Car Showroom Ready! 🚗', 'color: #667eea; font-size: 16px; font-weight: bold;');
console.log(`Loaded ${totalFrames} frames from video`);
console.log('Keyboard shortcuts:');
console.log('  Left/Right Arrow - Rotate car');
console.log('  F - Toggle fullscreen');
console.log('  A - Toggle auto-rotate');
