# Face Detection Project

This project is a Python script that utilizes the MediaPipe library for face detection in real-time video streams. It captures video from the default camera, detects faces in each frame, and displays the processed video with bounding boxes around the detected faces.

## Features

- Real-time face detection using the MediaPipe library
- Draws bounding boxes around detected faces
- Displays the confidence score for each detected face
- Counts the number of faces detected in each frame
- Computes and displays the frames per second (FPS)
- Applies bilateral filtering for smoothing the output video

## Requirements

- Python 3.x
- NumPy
- OpenCV (cv2)
- MediaPipe

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yashshah035/Face-Counting.git

2. Install the required dependencies:

   ```bash
   pip install numpy opencv-python mediapipe

## Usage

1. Navigate to the project directory:

   ```bash
   cd Face-Counting

2. Run the main Python file:

   ```bash
   python FaceCounter.py

3. The script will open a window displaying the video feed from your default camera. Detected faces will be highlighted with bounding boxes and confidence scores.

4. Press 'q' to quit the application.

## Code Explanation

The provided code performs the following steps:

1. Imports the necessary libraries: NumPy, time, OpenCV (cv2), and MediaPipe.
2. Initializes the MediaPipe Face Detection model with a detection confidence threshold of 0.4.
3. Defines a `detector` function that takes a video frame as input, detects faces, and draws bounding boxes and confidence scores on the frame.
4. Opens the default camera using `cv2.VideoCapture(0)` and sets the resolution to 1980x1080 pixels.
5. Enters a loop that reads frames from the camera, passes them to the `detector` function, computes the FPS, and displays the processed frame with face detections.
6. Applies bilateral filtering for smoothing the output video.
7. Displays the number of faces detected in the current frame.
8. Continues the loop until the 'q' key is pressed, then releases the camera and closes all windows.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License.
