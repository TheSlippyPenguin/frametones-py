
import cv2 #pip install opencv-python
import os
import vicosis_utils as utils
import time
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from RangeSlider import RangeSliderH
import numpy as np
import psutil #pip install psutil

# TODO CPU usage
# TODO resize to 900x600
# TODO display image
# TODO default directories for file explorer
# TODO hide preview images
# TODO connect other processors

class Fenetre() :
    def __init__(self) :
        # Initialisation de la fenêtre racine
        self.racine = Tk()

        # fond blanc
        self.racine.configure(bg='white')

        # Attributs esthétiques de la fenêtre
        self.racine.title('Menu principal')
        self.racine.geometry('720x480')

        # Film info

        self.film_path = ""
        self.n_film_frames = -1
        self.source = None

        # Processor settings

        self.output_height = 128

        self.highres = IntVar()
        self.highres.set(0)

        self.mode = IntVar()
        self.mode.set(1)

        self.quality = IntVar()
        self.quality.set(7)

        self.start_frame_number = IntVar(value=0)
        self.end_frame_number = IntVar(value=340000)

        self.frame_count = IntVar()
        self.frame_count.set(10)

        self.progress = IntVar()
        self.progress.set(0)

        # Styles

        self.radiostyle = ttk.Style()
        self.radiostyle.configure('white.TRadiobutton', background='white')

        self.labelstyle = ttk.Style()
        self.labelstyle.configure('white.TLabel', background='white')

        # Source images

        self.empty_preview = PhotoImage(file='empty_preview.png')
        self.handle = PhotoImage(file='handle.png')

        # Lancement des fonctions
        self.creer_widgets(self.racine)
        self.racine.mainloop()

    def creer_widgets(self, root):
        # TOP
        # Projet algo S4 (header)
        # version 1.0 (header)

        self.projectname_header = ttk.Label(root, text = 'Projet algo S4', font='Arial 13 bold', style='white.TLabel')
        self.projectname_header.place(x=304, y=10)

        self.projectversion_header = ttk.Label(root, text = 'version 1.0', font='Arial 11 italic', style='white.TLabel')
        self.projectversion_header.place(x=322, y=30)

        # MIDDLE LEFT
        # Source (header)
        # Sélectionner fichier (Entry to display filename)
        # Sélectionner fichier (Button to open file explorer)
        # Haute résolution (checkbox)
        # Haute résolution (label)
        # Explication haute résolution (label)
        # Paramètres de traitement (header)
        # Couleur moyenne par image - bandes (radio button)
        # Couleur moyenne par image - circulaire (radio button)
        # Couleurs par clusters (radio button)
        # curseur qualité (slider)
        # Qualité (label)

        self.source_header = ttk.Label(root, text = 'Source', font='Arial 11 bold', style='white.TLabel')
        self.source_header.place(x=73, y=70)

        self.selectfile_entry = ttk.Entry(root, width = 29, font='Arial 10', background='white')
        self.selectfile_entry.place(x=73, y=94)
        self.selectfile_entry.insert(INSERT, "Sélectionner un fichier source")
        self.selectfile_entry.configure(state='readonly')

        self.selectfile_button = ttk.Button(root, text = '...', width=3, command=self.load_film)
        self.selectfile_button.place(x=282, y=94)

        self.highres_checkbox = ttk.Checkbutton(root, onvalue=1, offvalue=0, variable=self.highres)
        self.highres_checkbox.place(x=73, y=135)

        self.highres_label1 = ttk.Label(root, text = 'Haute résolution', font='Arial 10', style='white.TLabel')
        self.highres_label1.place(x=95, y=122)

        self.highres_label2 = ttk.Label(root, text = 'Sélectionner si la résolution du fichier source\ndépasse 480x360', font='Arial 9 italic', style='white.TLabel')
        self.highres_label2.place(x=95, y=141)

        self.processing_header = ttk.Label(root, text = 'Paramètres de traitement', font='Arial 11 bold', style='white.TLabel')
        self.processing_header.place(x=73, y=180)

        self.meanbands_radiobutton = ttk.Radiobutton(root, text = 'Couleur moyenne par image - bandes', value=1, variable=self.mode, style='white.TRadiobutton')
        self.meanbands_radiobutton.place(x=73, y=203)

        self.meancircle_radiobutton = ttk.Radiobutton(root, text = 'Couleur moyenne par image - circulaire', value=2, variable=self.mode, style='white.TRadiobutton')
        self.meancircle_radiobutton.place(x=73, y=222)

        self.clusters_radiobutton = ttk.Radiobutton(root, text = 'Couleurs par clusters', value=3, variable=self.mode, style='white.TRadiobutton')
        self.clusters_radiobutton.place(x=73, y=241)

        self.fast_label = ttk.Label(root, text = 'Rapide', font='Arial 9 italic', style='white.TLabel')
        self.fast_label.place(x=73, y=290)

        self.quality_slider = Scale(root, from_=1, to=10, orient=HORIZONTAL, length=187, variable=self.quality, background='white')
        self.quality_slider.place(x=120, y=270)

        self.slow_label = ttk.Label(root, text = 'Lent', font='Arial 9 italic', style='white.TLabel')
        self.slow_label.place(x=315, y=290)

        self.quality_label = ttk.Label(root, text = 'Qualité', font='Arial 10', style='white.TLabel')
        self.quality_label.place(x=192, y=310)

        # MIDDLE RIGHT
        # Paramètres vidéo (header)
        # Image gauche (label)
        # Image droite (label)
        # Image gauche (image)
        # Image droite (image)
        # Temps (range slider)
        # Temps gauche (label)
        # Temps droite (label) OU utiliser les labels du range slider directement
        # Actualiser (button)
        # curseur images par heure (slider)
        # Images par heure (label)

        self.videosettings_header = ttk.Label(root, text = 'Paramètres vidéo', font='Arial 11 bold', style='white.TLabel')
        self.videosettings_header.place(x=400, y=70)

        self.leftimage_label = ttk.Label(root, text = 'première image', font='Arial 10 italic', style='white.TLabel')
        self.leftimage_label.place(x=400, y=94)

        self.rightimage_label = ttk.Label(root, text = 'dernière image', font='Arial 10 italic', style='white.TLabel')
        self.rightimage_label.place(x=530, y=94)

        self.leftimage_image = self.empty_preview
        self.leftimage_label = ttk.Label(root, image=self.leftimage_image)
        self.leftimage_label.place(x=400, y=114)

        self.rightimage_image = self.empty_preview
        self.rightimage_label = ttk.Label(root, image=self.rightimage_image)
        self.rightimage_label.place(x=530, y=114)

        self.time_rangeslider = RangeSliderH(root, [self.start_frame_number, self.end_frame_number], Width=255, Height=45, padX=25, min_val=0, max_val=self.end_frame_number.get(), font_size=10,\
     line_s_color='black',line_color='black', bar_color_inner='white', bar_color_outer='black',  line_width=1, bar_radius=8, font_family='Arial', show_value=True,\
        valueSide='BOTTOM', digit_precision='.0f', imageL=self.handle, imageR=self.handle, auto=False)
        self.time_rangeslider.place(x=400, y=180)

        self.refresh_button = ttk.Button(root, text = 'Actualiser', width=10, command=self.refresh_preview)
        self.refresh_button.place(x=400, y=225)

        self.large_label = ttk.Label(root, text = 'Gros', font='Arial 9 italic', style='white.TLabel')
        self.large_label.place(x=400, y=290)

        self.imagecount_slider = Scale(root, from_=10, to=2500, resolution=10, orient=HORIZONTAL, length=187, variable=self.frame_count, background='white')
        self.imagecount_slider.place(x=433, y=270)

        self.thin_label = ttk.Label(root, text = 'Fin', font='Arial 9 italic', style='white.TLabel')
        self.thin_label.place(x=628, y=290)

        self.imagesperhour_label = ttk.Label(root, text = 'Images à traiter', font='Arial 10', style='white.TLabel')
        self.imagesperhour_label.place(x=480, y=310)


        # BOTTOM
        # Lancer le traitement (button)
        # Annuler (button)
        # Barre de progression (progressbar)
        # images traitées (text)

        self.begin_button = ttk.Button(root, text = 'Lancer le traitement', width=20, command=self.DEBUG_load_settings)
        self.begin_button.place(x=300, y=350)

        self.progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=574, mode='determinate', maximum=self.frame_count.get(), variable=self.progress)
        self.progressbar.place(x=73, y=391)

        self.info_text = Text(root, width=69, height=2, font='Arial 10', state="disabled")
        self.info_text.place(x=73, y=420)

        self.usage_text=  Text(root, width=11, height=2, font='Arial 10', state="disabled")
        self.usage_text.place(x=566, y=420)
        self.write_info(self.usage_text, 'En attente\n')
        self.write_info(self.usage_text, '...\n') 


    def load_film(self):
        self.film_path = filedialog.askopenfilename(title = "Choisir un fichier", filetypes = (("Video files", "*.mp4"), ("all files", "*.*")))

        self.selectfile_entry.config(state='normal')
        self.selectfile_entry.delete(0, END)
        self.selectfile_entry.insert(0, self.film_path)
        self.selectfile_entry.config(state='disabled')

        self.delete_all_info(self.info_text)
        self.write_info(self.info_text, 'Fichier vidéo chargé : ' + self.film_path + '\n')

        # get relevant file info
        self.source = cv2.VideoCapture(self.film_path)
        self.n_film_frames = int(self.source.get(cv2.CAP_PROP_FRAME_COUNT))

        # update slider
        self.time_rangeslider.max_val=self.n_film_frames
        self.time_rangeslider.forceValues([0, self.n_film_frames])


    def refresh_preview(self):
        if self.film_path == '':
            self.write_info(self.info_text, 'Erreur : Aucun fichier vidéo chargé\n')
            return
        
        # get the first image at the start time
        self.source.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame_number.get())
        print(self.start_frame_number.get())
        start_frame = self.source.read()[1]
        start_frame = cv2.resize(start_frame, (120, 60))

        # get the last image at the end time
        self.source.set(cv2.CAP_PROP_POS_FRAMES, self.end_frame_number.get()-1)
        print(self.end_frame_number.get())
        end_frame = self.source.read()[1]
        end_frame = cv2.resize(end_frame, (120, 60))

        # write images as files
        cv2.imwrite('start_frame.png', start_frame)
        cv2.imwrite('end_frame.png', end_frame)
        # update the images
        self.leftimage_image = PhotoImage(file='start_frame.png')
        self.rightimage_image = PhotoImage(file='end_frame.png')

        self.leftimage_label.config(image=self.leftimage_image)
        self.rightimage_label.config(image=self.rightimage_image)
        

    def write_info(self, subject, text):
        subject.config(state='normal')
        subject.insert(INSERT, text)
        subject.config(state='disabled')

    def delete_all_info(self, subject):
        subject.config(state='normal')
        subject.delete(1.0, END)
        subject.config(state='disabled')

    def DEBUG_load_settings(self):
        
        out = f"High Res={self.highres.get()} ; Mode={self.mode.get()} ; Quality={self.quality.get()} ; Start frame={self.start_frame_number.get()} ; End frame={self.end_frame_number.get()}\
 ; Frames={self.frame_count.get()}"
        self.delete_all_info(self.info_text)
        self.write_info(self.info_text, out)

        self.process_film()


    def process_kmeans(self):
        
        output_image = np.zeros((self.output_height+4, self.frame_count.get(), 3), np.uint8)

        for i in range(self.frame_count.get()):
            frame_start_time = time.time()

            self.source.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame_number.get() + (i*self.frame_step) )
            frame = self.source.read()[1]
            output_image[:, i] = utils.kmeans_strip(image=frame, color_count=self.quality.get(), strip_height=self.output_height+4, compress=bool(self.highres.get()))[:, 0]

            # notify progress
            self.progress.set(i+1)
            self.delete_all_info(self.info_text)
            self.delete_all_info(self.usage_text)

            self.write_info(self.info_text, f"Image {i+1}/{self.frame_count.get()} traitée\n")
            self.write_info(self.info_text, f"FPS: {1/(time.time()-frame_start_time):.1f}\n")

            self.write_info(self.usage_text, f"RAM: {psutil.virtual_memory()[2]}%\n")
            #self.write_info(self.usage_text, f"CPU: {cpu_usage}%\n")

            self.progressbar.update()
            self.info_text.update()
            self.usage_text.update()

        output_image = output_image[4:, :, :]

        return output_image
    
    def process_film(self):

        self.disable_all()

        start_time = time.time()

        out_path = filedialog.askdirectory(title = "Choisir un dossier de destination", mustexist=True)
        os.chdir(out_path)

        self.frame_step = (self.end_frame_number.get() - self.start_frame_number.get()) // self.frame_count.get()
        self.progressbar.config(maximum=self.frame_count.get())

        match self.mode.get():
            case 1: # Bands
                print("Process bands")
            case 2: # Circles
                print("Process circles")
            case 3: # KMeans
                # paramètres bancals
                output_image = self.process_kmeans()


        cv2.imwrite(f"output_image.jpg", output_image)

        self.delete_all_info(self.info_text)
        self.write_info(self.info_text, f"Image enregistrée dans {out_path}\n")
        self.write_info(self.info_text, f"Temps de traitement : {time.time()-start_time:.1f}s\n")

        
        self.racine.destroy()

    def disable_all(self):
        # disable everything while processing
        self.begin_button.config(state='disabled')
        self.selectfile_button.config(state='disabled')
        self.selectfile_entry.config(state='disabled')
        self.meanbands_radiobutton.config(state='disabled')
        self.meancircle_radiobutton.config(state='disabled')
        self.clusters_radiobutton.config(state='disabled')
        self.highres_checkbox.config(state='disabled')
        self.refresh_button.config(state='disabled')
        self.quality_slider.config(state='disabled')
        self.imagecount_slider.config(state='disabled')


    

app = Fenetre()