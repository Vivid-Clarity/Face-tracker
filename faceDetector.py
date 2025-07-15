import cv2
import pathlib

class faceDetector:
    def __init__(self, img_path):
        self.cascade_path = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
        self.clf = cv2.CascadeClassifier(str(self.cascade_path))
        self.img_path = img_path
        self.camera = cv2.VideoCapture(0)
    
    def detect_face(self):
        cv2.namedWindow("Faces", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Faces", 800, 600)

        #Store the last known face position to maintain stability in face tracking
        last_face_position = None

        while True:
            # keyCode = cv2.waitKey(50)
            #Capture a frame from the webcam
            _, frame = self.camera.read()

            # if cv2.getWindowProperty("Faces", cv2.WND_PROP_VISIBLE) <1:
            #     break
            
            #Convert the frame to grayscale for face detection
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            #Detect faces in the frame
            faces = self.clf.detectMultiScale(
                grey,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            #Initialize face position variables
            x, y, width, height = None, None, None, None

            #If faces are detected, select the largest one and update the last known position
            if len(faces) > 0:
                faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)  # Sort faces by size
                last_face_position = faces[0]
                x, y, width, height = last_face_position
            elif last_face_position is not None:
                #Use the last known face position if no new face is detected
                x, y, width, height = last_face_position

            #Overlay the image if a face position is available
            if x is not None and y is not None and width is not None and height is not None:
                #Resize the overlay image to match the detected face size
                overlay_img = cv2.imread(self.img_path)
                if overlay_img is not None:
                    resized_overlay = cv2.resize(overlay_img, (width, height))
                    self.image_overlay(frame, resized_overlay, (x, y))
                else:
                    print(f"Failed to load image from {self.img_path}")

            # Display the frame with the overlay
            cv2.imshow("Faces", frame)    
            # Exit the loop if the 'q' key is pressed
            if cv2.waitKey(1) == ord("q"):
                break

        # Release the webcam and close all OpenCV windows
        self.camera.release()
        cv2.destroyAllWindows()    
        
    def image_overlay(self, frame, overlay, position):
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
        if y + h > frame.shape[0] or x + w > frame.shape[1]:
            return

        # Replace the image region with the overlay
        frame[y:y+h, x:x+w] = overlay