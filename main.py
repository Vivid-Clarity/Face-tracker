import cv2
import pathlib

"""
# OLD CODE FOR PNG
# Load the overlay image (PNG)
# overlay_img = cv2.imread('overlay.png', cv2.IMREAD_UNCHANGED)  # Ensure the image has an alpha channel

# # Function to overlay the image
# def overlay_image_alpha(img, overlay, position, alpha_mask):
#     x, y = position
#     h, w = overlay.shape[0], overlay.shape[1]

#     for c in range(0, 3):
#         img[y:y+h, x:x+w, c] = img[y:y+h, x:x+w, c] * (1 - alpha_mask[:, :, c] / 255.0) + overlay[:, :, c] * (alpha_mask[:, :, c] / 255.0)
"""

# Load the overlay image (JPG format, without alpha channel)
overlay_img = cv2.imread('overlay.jpg')  # Ensure the image is in JPG format

# Function to overlay an image onto another image at a given position
def overlay_image(img, overlay, position):
    """
    Overlays an image onto another image at a specified position.

    Parameters:
    img (numpy.ndarray): The background image.
    overlay (numpy.ndarray): The overlay image to be placed on top.
    position (tuple): The (x, y) position where the overlay image will be placed.

    Returns:
    None
    """
    x, y = position
    h, w = overlay.shape[:2]

    # Ensure the overlay dimensions fit within the frame boundaries
    if y + h > img.shape[0] or x + w > img.shape[1]:
        return

    # Replace the image region with the overlay
    img[y:y+h, x:x+w] = overlay

# Load the Haar Cascade for face detection
cascade_path = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
print(f"Haar Cascade path: {cascade_path}")

clf = cv2.CascadeClassifier(str(cascade_path))

# Initialize the webcam for capturing video
camera = cv2.VideoCapture(0)

# Create a resizable window for displaying the video feed
cv2.namedWindow("Faces", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Faces", 800, 600)

# Store the last known face position to maintain stability in face tracking
last_face_position = None

while True:
    # Capture a frame from the webcam
    _, frame = camera.read()
    
    # Convert the frame to grayscale for face detection
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = clf.detectMultiScale(
        grey,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Initialize face position variables
    x, y, width, height = None, None, None, None

    # If faces are detected, select the largest one and update the last known position
    if len(faces) > 0:
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)  # Sort faces by size
        last_face_position = faces[0]
        x, y, width, height = last_face_position
    elif last_face_position is not None:
        # Use the last known face position if no new face is detected
        x, y, width, height = last_face_position

    # Overlay the image if a face position is available
    if x is not None and y is not None and width is not None and height is not None:
        # Resize the overlay image to match the detected face size
        resized_overlay = cv2.resize(overlay_img, (width, height))
        overlay_image(frame, resized_overlay, (x, y))

    """
    # OLD CODE FOR RECTANGLE
    # for (x,y,width,height) in faces:
    #     #draws a recatngle
    #     #want this to be an image overlaid over face
    #     # cv2.rectangle(frame, (x,y), (x+width, y+height), (255,255,0), 2)
    """
    
    """
    # OLD CODE FOR USING PNG
    #     # # Resize the overlay image to match face dimensions
    #     # resized_overlay = cv2.resize(overlay_img, (width, height))

    #     # # Split the overlay image into color and alpha channels
    #     # overlay_color = resized_overlay[:, :, :3]
    #     # overlay_alpha = resized_overlay[:, :, 3:]

    #     # # Overlay the image on the frame
    #     # overlay_image_alpha(frame, overlay_color, (x, y), overlay_alpha)

    #     #JPG-----------------------------
    #     # Resize the overlay image to match face dimensions
    #     resized_overlay = cv2.resize(overlay_img, (width, height))

    #     # Overlay the image on the frame
    #     overlay_image(frame, resized_overlay, (x, y))
    """

    # Display the frame with the overlay
    cv2.imshow("Faces", frame)    
    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release the webcam and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()