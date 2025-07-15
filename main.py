import customtkinter
from faceDetector import faceDetector
from imageUploader import imageUploader

def init():
    #System settings
    customtkinter.set_appearance_mode('System')
    customtkinter.set_default_color_theme('blue')

    app = customtkinter.CTk()
    app.title("Face Detector")
    app.geometry("800x600")

    # Configure grid layout
    app.grid_rowconfigure(0, weight=0)  # title 
    app.grid_rowconfigure(1, weight=3)  # top 60%
    app.grid_rowconfigure(2, weight=2)  # bottom 40%
    app.grid_columnconfigure(0, weight=1)

    #Title label
    title_label = customtkinter.CTkLabel(app, text="Face Detector", font=("Arial", 24))
    title_label.grid(row=0, column=0, pady=10)

    #-------------------------------------------------------
    #face tracker frame
    face_tracker_frame = customtkinter.CTkFrame(app, border_width=5, border_color="black")
    face_tracker_frame.pack_propagate(False)    
    face_tracker_frame.grid(row=1, column=0, sticky="nsew")


    #-------------------------------------------------------
    #image frame
    image_frame = customtkinter.CTkFrame(app,border_width=5, border_color="black")
    image_frame.pack_propagate(False)
    image_frame.grid(row=2, column=0, sticky="nsew")

    #image frame grid
    image_frame.grid_columnconfigure(0, weight=1)  #image
    image_frame.grid_columnconfigure(1, weight=3)  #buttons
    image_frame.grid_rowconfigure(0, weight=1)

    #Image label for displaying the uploaded image
    img_label = customtkinter.CTkLabel(image_frame, text="")
    img_label.grid(row=0, column=0, padx=5, pady=10, sticky="nse")

    #creating an instance of imgUploader
    image_uploader = imageUploader(img_label, image_frame)

    #-------------------------------------------------------
    #button frame
    button_frame = customtkinter.CTkLabel(image_frame, text="")
    button_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nse")

    #button frame grid
    button_frame.grid_rowconfigure(0, weight=1)  #upload button
    button_frame.grid_rowconfigure(1, weight=1)  #face detection button
    image_frame.grid_columnconfigure(0, weight=1)

    #Image upload button
    upload_button = customtkinter.CTkButton(button_frame, text="Upload Image", command= image_uploader.upload)
    upload_button.grid(row=0, column=0, padx=50, pady=10, sticky="s")

    
    #Face detection button
    run_detection = customtkinter.CTkButton(button_frame, text="Run Face Detection", command=lambda:start_face_detection(image_uploader))
    run_detection.grid(row=1, column=0, padx=50, pady=10, sticky="n")
    
    return app

def start_face_detection(image_uploader):
    img_path = image_uploader.get_image_path()
    if img_path:
        face_detector = faceDetector(img_path)
        face_detector.detect_face()

    else:
        print("No image uploaded yet.")

if __name__ == '__main__':
    app = init()
    app.mainloop()