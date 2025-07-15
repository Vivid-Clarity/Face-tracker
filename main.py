import tkinter
import customtkinter
from face_detector import face_cascade
from PIL import Image

def imgUploader(img_label):
    fileTypes = [("Image files", "*.jpg *.jpeg *.png")]
    file_path = customtkinter.filedialog.askopenfilename(title="Select an Image", filetypes=fileTypes)

    #if a file was selected, process it
    if file_path:
        print(f"Selected file: {file_path}")
        img = Image.open(file_path)
        
        # Resize the image to fit within a maximum size
        max_width, max_height = 600, 600
        scale = min(max_width / img.width, max_height / img.height)
        display_size = (int(img.width * scale), int(img.height * scale))

        pic = customtkinter.CTkImage(img, size=display_size)      

        img_label.configure(image=pic)
        img_label.image = pic
    else:
        print("No file selected.")


def init():
    #System settings
    customtkinter.set_appearance_mode('System')
    customtkinter.set_default_color_theme('blue')

    app = customtkinter.CTk()
    app.title("Face Detector")
    app.geometry("800x600")
    
    title_label = customtkinter.CTkLabel(app, text="Face Detector", font=("Arial", 24))
    title_label.pack(pady=20)

    #Image lavel for displaying the uploaded image
    img_label = customtkinter.CTkLabel(app, text="")
    img_label.pack(pady=10)

    #Image upload button
    upload_button = customtkinter.CTkButton(app, text="Upload Image", command= lambda:imgUploader(img_label))
    upload_button.pack(pady=10)



    return app


if __name__ == '__main__':
    app = init()
    app.mainloop()