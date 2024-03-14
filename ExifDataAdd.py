import os
from pathlib import Path
from PIL import Image, ImageTk
import datetime
import tkinter as tk
from tkinter import filedialog
import piexif


class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EXIF Populator")
        
        #File Search Variables
        self.dir_read_path=''
        self.dir_read_path_good=False
        self.dir_save_path=''
        self.dir_save_path_good=False
        self.files = None
        self.file_index = None

        #Exif
        self.day=-1
        self.month=-1
        self.year=-1
        self.date=''

        #Image
        self.image= None
        self.image_loaded = False
        self.thumb= None
        self.thumb_white=ImageTk.PhotoImage(Image.new('RGB',(800,450),color='white'))
        self.current_exif_data= None

        #Frames
        self.control_frame=tk.Frame(self)
        self.image_frame=tk.Frame(self)
        self.input_frame=tk.Frame(self.control_frame)
        self.button_frame=tk.Frame(self.control_frame)

        #Frame Packing
        self.control_frame.grid(column=0,row=0,sticky="NSEW")
        self.image_frame.grid(column=1,row=0,sticky="NSEW")

        #Image Frame
        self.dir_label = tk.Label(self.image_frame,text="Please Load A Directory")#Directory & File Information
        self.image_label = tk.Label(self.image_frame,width=800, height=450,image=self.thumb_white)
        self.info_label = tk.Label(self.image_frame,text="Information Appears Here")#Information messages to user
        self.dir_label.grid(column=0,row=0,sticky="NSEW")
        self.image_label.grid(column=0,row=1,sticky="NSEW")
        self.info_label.grid(column=0,row=2,sticky="NSEW")

        #Data Input Frame
        self.year_label = tk.Label(self.input_frame, text="Enter Year: (YYYY):")
        self.month_label = tk.Label(self.input_frame, text="Enter Month: (MM):")
        self.day_label = tk.Label(self.input_frame, text="Enter Day: (DD):")
        self.year_entry = tk.Entry(self.input_frame)
        self.month_entry = tk.Entry(self.input_frame)
        self.day_entry = tk.Entry(self.input_frame)
        self.year_label.grid(column=0,row=1,sticky="NSEW")
        self.year_entry.grid(column=1,row=1,sticky="NSEW")
        self.month_label.grid(column=0,row=2,sticky="NSEW")
        self.month_entry.grid(column=1,row=2,sticky="NSEW")
        self.day_label.grid(column=0,row=3,sticky="NSEW")
        self.day_entry.grid(column=1,row=3,sticky="NSEW")
        self.input_frame.grid(column=0,row=0,sticky="NSEW")
        self.input_frame.grid_columnconfigure((0,1),minsize=135)
        self.input_frame.grid_rowconfigure(0,minsize=23)
        self.input_frame.grid_rowconfigure(4,minsize=309)

        
        #Button Frame
        self.next_button = tk.Button(self.button_frame, text="Next",command=self.next_image)
        self.prev_button = tk.Button(self.button_frame, text="Prev",command=self.prev_image)
        self.load_button = tk.Button(self.button_frame, text="Select Read Directory", command=self.pick_read_dir)
        self.load2_button = tk.Button(self.button_frame, text="Select Save Directory", command=self.pick_save_dir)
        self.save_button = tk.Button(self.button_frame, text="Write Exif",command=self.write_exif)
        self.quit_button = tk.Button(self.button_frame,text="Quit", command=self.quit)
        self.next_button.grid(column=1,row=0,sticky="NSEW")
        self.prev_button.grid(column=0,row=0,sticky="NSEW")
        self.load2_button.grid(column=0,row=1,sticky="NSEW")
        self.load_button.grid(column=1,row=1,sticky="NSEW")
        self.save_button.grid(column=0,row=2,columnspan=2,sticky="NSEW")
        self.quit_button.grid(column=0,row=3,columnspan=2,sticky="NSEW")
        self.button_frame.grid_columnconfigure((0,1),minsize=135)
        self.button_frame.grid(column=0,row=1,sticky="NSEW")

    def clear_image_information(self):
        self.image_label.config(image=self.thumb_white)
        self.image.close()
        self.image_loaded = False
        self.thumb = None
        self.current_exif_data = None

        self.date=''
        self.day=-1
        self.month=-1
        self.year=-1
        return
    
    def pop_file(self):
        self.files.pop(self.file_index)
        self.file_index= None
        return
    
    def clear_read_dir(self):
        self.dir_read_path =''
        self.dir_read_path_good = False

    def exif_give_date(self):
        try:
            date_str=self.current_exif_data[306].replace(' ',':').split(':')
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, date_str[0])

            self.month_entry.delete(0, tk.END)
            self.month_entry.insert(0, date_str[1])

            self.day_entry.delete(0, tk.END)
            self.day_entry.insert(0, date_str[2])
            tk.messagebox.showerror("Error", "Image Has Exif") 

        except KeyError:
            return


    
    def run_fast_scandir(self,dir,ext):    # dir: str, ext: list
        if(not self.dir_read_path):
            return
        
        subfolders, files = [], []
        for f in os.scandir(dir):
            if f.is_dir():
                subfolders.append(f.path)
            if f.is_file():
                if os.path.splitext(f.name)[1].lower() in ext:
                    files.append(f.path.replace("\\","/"))


        for dir in list(subfolders):
            sf, f = self.run_fast_scandir(dir, ext)
            subfolders.extend(sf)
            files.extend(f)
            #print(f)
        return subfolders,files
    

    def load_image(self,path):
        self.image = Image.open(path)
        if(self.image):
            self.dir_label.config(text=f"{path}")
            image_thumb = self.image.resize((800, 450))
            self.thumb = ImageTk.PhotoImage(image_thumb)
            self.image_label.config(image=self.thumb)
            self.current_exif_data = self.image._getexif()
            if(self.current_exif_data):
                self.exif_give_date()
        else:
            self.info_label.config(text="Image Failed to Load")
        return
    
    def next_image(self):
        self.info_label.config(text="")
        #Disable Button if Path not selected
        if(not self.dir_read_path):
            self.dir_label.config(text="Please Select A Directory!")
            return
        
        if(self.image_loaded):
            if(self.file_index != len(self.files)-1):
                self.file_index+=1
            else:
                self.file_index=0
                self.info_label.config(text="Reached End of Images, Sending to Start")

        else:
            self.file_index=0
            self.image_loaded=True

        self.load_image(self.files[self.file_index])
        return

    def prev_image(self):
        self.info_label.config(text="")
        #Disable Button if Path not selected
        if(not self.dir_read_path):
            self.dir_label.config(text="Please Select A Directory!")
            return  
              
        if(self.image_loaded):
            self.clear_image_information()
            if(self.file_index != 0):
                self.file_index-=1
            else:
                self.file_index=len(self.files)-1
                self.info_label.config(text="Reached Beginning of Images, Sending to End")

        else:
            self.file_index=len(self.files)-1
            self.image_loaded=True

        self.load_image(self.files[self.file_index])
        return
       
    def pick_read_dir(self):
        #Clear Out Everything
        self.info_label.config(text="")
        self.dir_read_path=''
        self.files=[]
        self.file_index = False
        self.image_loaded = False
        self.image_label.config(image=self.thumb_white)#update reference
        self.image=[]

        self.dir_read_path=filedialog.askdirectory(title="Pick A Directory to Read Files From") 
        if self.dir_read_path:
            self.files=self.run_fast_scandir(self.dir_read_path,[".jpg",".jpeg","JPG",".JPEG"])[1]
            if(self.files):
                self.dir_label.config(text=f"Read From: {self.dir_read_path}")
                self.info_label.config(text="Click Next to Load First Image")
                self.dir_read_path_good=True
                return

        self.dir_label.config(text="Please Select A Directory")        
        self.info_label.config(text="Directory Selection has failed")
        self.dir_read_path_good=False
        return
    
    def pick_save_dir(self):
        self.dir_save_path=''

        self.dir_save_path=filedialog.askdirectory(title="Pick A Directory To Save Files To") 
        if self.dir_save_path:
            self.info_label.config(text=f"Save to: {self.dir_save_path}")
            self.dir_save_path_good=True
            return
            
        
        self.dir_label.config(text="Please Select A Directory")        
        self.info_label.config(text="Directory Selection has failed")
        self.dir_save_path_good=False
        return
    
    def verify_day(self,day):
        try:
            day=int(day)
            if(1<=day<=31):
                return True
            else:
                return False
        except ValueError:
            return False
    
    def verify_month(self,month):
        try:
            month=int(month)
            if(1<=month<=12):
                return True
            else:
                return False
        except ValueError:
            return False
        
    def verify_year(self,year):
        try:
            year=int(year)
            if(1900<=year<=3000):
                return True
            else:
                return False
        except ValueError:
            return False
        
    def create_date(self,year,month,day):
        try:
            self.day=int(day)
            self.month=int(month)
            self.year=int(year)
            # Create a datetime object with the provided year, month, and day
            date_obj = datetime.datetime(self.year, self.month, self.day, 12,0,0)
        
        # Format the datetime object as a string in the desired format
            self.date = date_obj.strftime('%Y:%m:%d %H:%M:%S')
            return True
        except ValueError:
            self.date=''
            self.day=-1
            self.month=-1
            self.year=-1
            return False
    def verify_dir(self,path):
        Path(path).mkdir(parents=True, exist_ok=True)
        return
    
    def write_exif(self):       
        if(not self.dir_read_path_good):
            self.info_label.config(text="Please Select A Directory to Read From")
            return
        
        if(not self.image_loaded):
            self.info_label.config(text="Please Load an Image")
            return
        
        if(not self.dir_save_path_good):
            self.info_label.config(text="Please Select A Directory to Save to")
            return
        
        
        day=self.day_entry.get()
        month=self.month_entry.get()
        year=self.year_entry.get()
        
        if( not self.verify_day(day) or not self.verify_month(month) or not self.verify_year(year)):
            self.info_label.config(text="Please Input a Valid Date")
            return
        
        self.date=''
        if( not self.create_date(year,month,day)):
            self.info_label.config(text="Please Input a Valid Date")
            return
        
        zeroth_ifd = {
            piexif.ImageIFD.Make: u"FUJIFILM",
            piexif.ImageIFD.Model: u"XS5",
            piexif.ImageIFD.DateTime: self.date,
            piexif.ImageIFD.XResolution: (self.image.width, 1),
            piexif.ImageIFD.YResolution: (self.image.height, 1),
            piexif.ImageIFD.Software: u"emexifadd"
            }
        exif_ifd = {
            piexif.ExifIFD.DateTimeOriginal: self.date,
            piexif.ExifIFD.DateTimeDigitized: self.date,
            }


        exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd}
        exif_data_bytes=piexif.dump(exif_dict)
        self.verify_dir(f"{self.dir_save_path}/{self.year}/{str(self.month).zfill(2)}")      
        path=f"{self.dir_save_path}/{self.year}/{str(self.month).zfill(2)}/{os.path.basename(self.files[self.file_index])}"
        
        self.image.save(path)
        piexif.insert(exif=exif_data_bytes,image=path)
        #Write Complete increment to next image if available
        #https://piexif.readthedocs.io/en/latest/functions.html#insert
        self.pop_file()
        self.clear_image_information()

        if(len(self.files)!=0):
            self.next_image()
        else:
            self.clear_read_dir()
            self.info_label.config(text="Photos Completed Please Select a New Read Directory")
            

def button_click(event=None):
    focused_widget = app.focus_get()
    if isinstance(focused_widget, tk.Button):
        focused_widget.invoke()   

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"  # Prevent default behavior of tab key

def focus_prev_widget(event):
    event.widget.tk_focusPrev().focus()
    return "break"  # Prevent default behavior of tab key

if __name__ == "__main__":
    app = ImageApp()
    app.bind("<Tab>", focus_next_widget)
    app.bind("<Up>", focus_prev_widget)
    app.bind("<Down>", focus_next_widget)
    app.bind('<Return>', button_click)
    app.mainloop()