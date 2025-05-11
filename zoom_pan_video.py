import cv2
import argparse
import sys
# footage was taken from 27cm away from subject
# python zoom_pan_video.py {video_file} --zoom{zoom_percentage}

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Zoom and pan a video with looping.")
    parser.add_argument("video_path", help="Path to the video file (1080p or 4K)")
    parser.add_argument("--zoom", type=int, default=1500, #for 1cm by 1cm crop
                        help="Zoom percentage (100 = no zoom, >100 zoom in). E.g., 200 means 2x zoom.")
    args = parser.parse_args()

    # Open the video file
    cap = cv2.VideoCapture(args.video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Read the first frame to get dimensions
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read video frame.")
        return
    height, width = frame.shape[:2]

    # Choose the smaller dimension as the base square size
    base_dim = min(width, height)

    # Convert zoom percentage to zoom factor (e.g., 200 -> 2.0)
    zoom_factor = args.zoom / 100.0
    # Calculate crop size (the square region dimensions)
    crop_size = int(base_dim / zoom_factor)
    # Ensure crop_size doesn't exceed frame dimensions
    crop_size = min(crop_size, width, height)

    # Initialize panning offsets so that the crop is centered
    offset_x = (width - crop_size) // 2
    offset_y = (height - crop_size) // 2

    # Define pan step (adjust as needed)
    pan_step = max(1, crop_size // 20)

    # Set up arrow key codes based on the operating system.
    if sys.platform.startswith('darwin'):
        # macOS key codes
        UP_KEY    = 63232
        DOWN_KEY  = 63233
        LEFT_KEY  = 63234
        RIGHT_KEY = 63235
    elif sys.platform.startswith('linux'):
        LEFT_KEY  = 65361
        UP_KEY    = 65362
        RIGHT_KEY = 65363
        DOWN_KEY  = 65364
    else:  # Windows (or others)
        LEFT_KEY  = 2424832
        UP_KEY    = 2490368
        RIGHT_KEY = 2555904
        DOWN_KEY  = 2621440

    window_name = "Zoomed & Panned Video (arrow keys to pan, q/Esc to quit)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    print("Make sure the video window is active (click on it) to capture key presses.")
    print("Press arrow keys to pan. Press 'q' or Esc to quit.")

    # Main loop to continuously read frames and loop the video
    while True:
        # If we've reached the end, loop the video back to the start.
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
            if not ret:
                break  # Something went wrong; exit the loop

        # Ensure cropping offsets remain within frame boundaries
        offset_x = max(0, min(offset_x, width - crop_size))
        offset_y = max(0, min(offset_y, height - crop_size))

        # Crop the frame to the square region
        cropped_frame = frame[offset_y:offset_y + crop_size, offset_x:offset_x + crop_size]

        # Display the cropped (zoomed) frame
        cv2.imshow(window_name, cropped_frame)

        # Wait for key press (using waitKeyEx to capture extended keys like arrows)
        key = cv2.waitKeyEx(30)
        if key != -1:
            print("Key pressed:", key)
        if key == ord('q') or key == 27:  # 'q' or Esc to quit
            break
        elif key == LEFT_KEY:
            offset_x -= pan_step
        elif key == RIGHT_KEY:
            offset_x += pan_step
        elif key == UP_KEY:
            offset_y -= pan_step
        elif key == DOWN_KEY:
            offset_y += pan_step

        # Read the next frame
        ret, frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
