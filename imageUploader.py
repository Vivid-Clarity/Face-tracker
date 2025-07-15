import customtkinter
from PIL import Image


class imageUploader:
    def __init__(self, img_label, image_frame):
        self.img_label = img_label
        self.image_frame = image_frame
        self.file_path = ""
    
    def upload(self):
        fileTypes = [("Image files", "*.jpg *.jpeg *.png")]
        self.file_path = customtkinter.filedialog.askopenfilename(title="Select an Image", filetypes=fileTypes)

        #if a file was selected, process it
        if self.file_path:
            print(f"Selected file: {self.file_path}")
            img = Image.open(self.file_path)
            
            #Get image_frame dimensions
            self.image_frame.update_idletasks()
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()

            # print(f"Frame size: {frame_width}x{frame_height}")  #for debugging

            #calculate the display size while maintaining aspect ratio
            max_width = int(frame_width * 0.9)
            max_height = int(frame_height * 0.9)
            scale = min(max_width / img.width, max_height / img.height)
            display_size = (int(img.width * scale), int(img.height * scale))

            pic = customtkinter.CTkImage(img, size=display_size)      

            self.img_label.configure(image=pic)
            self.img_label.image = pic
        else:
            print("No file selected.")
