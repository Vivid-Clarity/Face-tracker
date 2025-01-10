import cv2
import pathlib

# Load the overlay image (PNG)
# overlay_img = cv2.imread('overlay.png', cv2.IMREAD_UNCHANGED)  # Ensure the image has an alpha channel

# # Function to overlay the image
# def overlay_image_alpha(img, overlay, position, alpha_mask):
#     x, y = position
#     h, w = overlay.shape[0], overlay.shape[1]

#     for c in range(0, 3):
#         img[y:y+h, x:x+w, c] = img[y:y+h, x:x+w, c] * (1 - alpha_mask[:, :, c] / 255.0) + overlay[:, :, c] * (alpha_mask[:, :, c] / 255.0)


# Load the overlay image (JPG)
overlay_img = cv2.imread('overlay.jpg')  # No alpha channel

# Function to overlay the image
def overlay_image(img, overlay, position):
    x, y = position
    h, w = overlay.shape[:2]

    # Ensure the overlay dimensions fit within the frame
    if y + h > img.shape[0] or x + w > img.shape[1]:
        return

    # Replace the image region with the overlay
    img[y:y+h, x:x+w] = overlay

cascade_path = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
print(cascade_path)

clf = cv2.CascadeClassifier(str(cascade_path))

camera = cv2.VideoCapture(0)

cv2.namedWindow("Faces", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Faces", 800, 600)

last_face_position = None

while True:
    _, frame = camera.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = clf.detectMultiScale(
        grey,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    x, y, width, height = None, None, None, None

    if len(faces) > 0:
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        last_face_position = faces[0]
        x, y, width, height = last_face_position
    elif last_face_position is not None:
        x, y, width, height = last_face_position

    if x is not None and y is not None and width is not None and height is not None:
        resized_overlay = cv2.resize(overlay_img, (width, height))
        overlay_image(frame, resized_overlay, (x, y))


    # for (x,y,width,height) in faces:
    #     #draws a recatngle
    #     #want this to be an image overlaid over face
    #     # cv2.rectangle(frame, (x,y), (x+width, y+height), (255,255,0), 2)

    #     #PNG----------------------
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
    
    cv2.imshow("Faces", frame)
    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()