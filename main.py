import datetime
import math
import os
from time import sleep
import time
import tkinter as tk
import customtkinter as ctk

from tkVideoPlayer import TkinterVideo
from tkinter import ttk
import tkinterDnD
from PIL import Image, ImageTk
from RangeSlider.RangeSlider import RangeSliderH

from helpers import *
from helpers import CollapsiblePane as cp

from threading import Thread


class App:
    def changePage(self, pageNumber):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.pages[pageNumber]()


    def initPage(self):

        def run_progress():
            my_progress = ttk.Progressbar(self.app, orient=tk.HORIZONTAL, length=500, mode='determinate')
            my_progress['value'] += 500
            time.sleep(5)
            my_progress.pack(pady=40)

        def drop(event):
            # run_progress()
            print(event.data[1:-1])
            if event.data[1:-1].endswith(".mp4"):
                self.path = event.data[1:-1]
                self.changePage("progressPage")

        def click_frame(_):
            path = tk.filedialog.askopenfilename(title="Select the video", initialdir="/",
                                              filetypes=(('mp4 files','*.mp4'), ("mkv files", "*.mkv"), ("avi files", "*.avi")))
            if path:
                if path.endswith(".mp4"):
                    print(path)
                    self.path=path
                    self.changePage("progressPage")

        ctk.CTkLabel(master=self.app , font=("Segoe UI",24), text="Emo-Rooms").pack( padx=10, pady=5, anchor="w")
        ctk.CTkLabel(master=self.app, font=("Segoe UI",14), text=self.description, wraplength=1500, justify="left")\
            .pack(pady=5, padx=10, anchor = "nw")
        page = ctk.CTkFrame(self.app, corner_radius=30, border_width=1, fg_color="transparent")
        page.pack(padx=10, pady=10)

        page = ttk.Frame(page, ondrop=drop, padding=20)
        page.pack(fill="both", expand=True, padx=10, pady=10)
        page.bind("<Button-1>", click_frame)

        image = ctk.CTkImage(light_image=Image.open("icons/uploadImage.png"), size=(200, 200))
        label = ctk.CTkLabel(master=page, image=image, text="", height=220, width=self.app.winfo_screenwidth())
        # label.minsize((220, 500))
        print(self.app.winfo_screenwidth())
        print(self.app.winfo_screenheight())
        label.pack()
        label.bind("<Button-1>", click_frame)

        ctk.CTkLabel(master=page, text="Upload Video", font=("Segoe UI",14))\
            .pack(pady=5)
        ctk.CTkLabel(master=page, text="Click to browse or drag and drop video in the box", font=("Segoe UI",11))\
            .pack()

    def progressIndicatorPage(self):

        startTime = datetime.datetime.now()
        ctk.CTkLabel(master=self.app, font=("Segoe UI", 24), text="Emo-Rooms").pack(padx=10, pady=5, anchor="nw")
        ctk.CTkLabel(master=self.app, font=("Segoe UI", 14), text=self.description, wraplength=1500, justify="left") \
            .pack(pady=5, padx=10, anchor="nw")

        page = ctk.CTkFrame(self.app, corner_radius=30, border_width=1, fg_color="transparent")
        page.pack(padx=10, pady=10, fill="both", expand=True)

        statuslabel = tk.Label(master=page, text="Uploading...", font=("", 21), background="white")
        statuslabel.pack(padx=20, pady=(50,10))

        progressbar = ctk.CTkProgressBar(master=page, width=400, fg_color="#ddd", progress_color="black")
        progressbar.pack(padx=20, pady=10, anchor="center")
        progressbar.set(0)

        def time():
            seconds = int((datetime.datetime.now()- startTime).total_seconds())
            seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            string =  "Process running time: %d:%02d:%02d" % (hour, minutes, seconds)
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = tk.Label(master=page, text= "", font=("", 9), background="white")
        lbl.pack(padx=20, pady=10)
        time()

        def back():
            self.path = ""
            self.changePage("initPage")

        ctk.CTkButton(page, command=back, text="Back", fg_color="black", text_color="white", hover_color="#333").pack()

        def analyse(progressbar):
            print1()

            statuslabel["text"]="Processing..."
            progressbar.step()
            print2()
            self.changePage("settingsPage")

        bg = Thread(target=analyse, daemon=True, args=(progressbar,), name="analyse")
        bg.start()

    def buildVideoPlayer(self, path, frame, showRangeSelector=True):
        def seek(value):
            """ used to seek a specific timeframe """
            # print(value)
            videoplayer.seek(value)

        def update_duration(event):
            """ updates the duration after finding the duration """
            duration = videoplayer.video_info()["duration"]

        def update_scale(event):

            sec = math.floor(videoplayer.video_info()["duration"] % 60)
            min = math.floor(videoplayer.video_info()["duration"] / 60)
            hr = math.floor(videoplayer.video_info()["duration"] / 3600)
            duration = f'{"0" if hr <= 9 else ""}{hr}:{"0" if min <= 9 else ""}{min}:{"0" if sec <= 9 else ""}{sec}'

            sec = math.floor(videoplayer.current_duration() % 60)
            min = math.floor(videoplayer.current_duration() / 60)
            hr = math.floor(videoplayer.current_duration() / 3600)
            current = f'{"0" if hr <= 9 else ""}{hr}:{"0" if min <= 9 else ""}{min}:{"0" if sec <= 9 else ""}{sec}'

            duration_text.set(f'{current}/{duration}')
            if videoplayer.current_duration() > math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"]):
                seek(math.ceil(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"]))

        def video_ended(event):
            """ handle video ended """
            play_pause_button["text"] = "Play"
            seek(math.ceil(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"]))

        def play_pause():
            """ pauses and plays """
            if videoplayer.is_paused():
                videoplayer.play()
                play_pause_button["text"] = "| |"

            else:
                videoplayer.pause()
                play_pause_button["text"] = "▶"

        def play():
            if videoplayer.is_paused():
                videoplayer.play()
                play_pause_button["text"] = "| |"

        def pause():
            videoplayer.pause()
            play_pause_button["text"] = "Play"

        def updateStartSlider(_,__,___):
            seek(math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"]))
            # pause()
            self.start_time_in_sec =  math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"])
            sec = math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"] % 60)
            min = math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"] / 60)
            hr = math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"] / 3600)
            text = f'{"0" if hr<=9 else ""}{hr}:{"0" if min<=9 else ""}{min}:{"0" if sec<=9 else ""}{sec}'
            self.start_time_text.set(text)

        def updateEndSlider(_,__,___):
            # seek(math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"]))
            # pause()
            self.end_time_in_sec = math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"])
            sec = math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"] % 60)
            min = math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"] / 60)
            hr = math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"] / 3600)
            text = f'{"0" if hr <= 9 else ""}{hr}:{"0" if min <= 9 else ""}{min}:{"0" if sec <= 9 else ""}{sec}'
            self.end_time_text.set(text)

        def play_from_Beginning():
            seek(math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"]))
            # pause()

        def skip(value):
            seek(int(videoplayer.current_duration()) + value)

        videoplayer = TkinterVideo(master = frame, scaled=True, takefocus=False)
        videoplayer.load(r"{}".format(path))
        # videoplayer.set_size((250, 600))
        videoplayer.keep_aspect(True)
        videoplayer.pack(expand=True, fill="both")
        videoplayer.play()

        videoplayer.bind("<<Duration>>", update_duration)
        videoplayer.bind("<<SecondChanged>>", update_scale)
        videoplayer.bind("<<Ended>>", video_ended)

        bottombar = ctk.CTkFrame(frame, fg_color="transparent", width=800)
        bottombar.pack()

        tk.Button(bottombar, text="<<", command=lambda: skip(-5), width=10, background="white", border=0).grid(row=0, column=0, sticky='w')

        play_pause_button = tk.Button(bottombar,width=10, background="white", text="| |", command=play_pause, border=0)
        play_pause_button.grid(row=0, column=1, sticky='w')
        stop_button = tk.Button(bottombar, width=10, background="white", text="☐", command=play_from_Beginning,
                                      border=0)
        stop_button.grid(row=0, column=2, sticky='w')
        duration_text = tk.StringVar()
        duration_label = ctk.CTkLabel(master=bottombar, textvariable=duration_text)
        duration_label.grid(row=0, column=3, sticky='w')

        tk.Button(bottombar, text=">>", command=lambda: skip(5), width=10, background="white", border=0).grid(row=0, column=10, sticky='w')

        rangeSelector = RangeSliderH(frame, [self.start_time_in_percentage, self.end_time_in_percentage], padX=0, line_width=5, line_color="#ddd", line_s_color="black", show_value=False, Height=56, bar_radius=6)
        self.start_time_in_percentage.trace_variable("w", updateStartSlider)
        self.end_time_in_percentage.trace_variable("w", updateEndSlider)
        if showRangeSelector:
            rangeSelector.pack()

        updateStartSlider(1, 2, 3)
        updateEndSlider(1, 2, 3)

        return videoplayer, rangeSelector

    def settingsPage(self):

        def toggleCategory(number):
            value = self.ckvar[number-4].get()
            for i in range(number-3, number):
                self.ckvar[i].set(value)
            checkEachCategory()

        def checkEachCategory():
            for i in range(0,len(self.ckvar)-1,4):
                if self.ckvar[i+1].get()==0 or self.ckvar[i+2].get()==0 or self.ckvar[i+3].get()==0:
                    self.ckvar[i].set(0)

                if self.ckvar[i+1].get() == 1 and self.ckvar[i+2].get() == 1 and self.ckvar[i+3].get() == 1:
                    self.ckvar[i].set(1)

        def buildEachRow(frame, category, moodslist, row, ckvar_count):
            ctk.CTkCheckBox(master=frame, variable=self.ckvar[ckvar_count], command=lambda: toggleCategory(ckvar_count),
                            text=category, font=("", 12), checkbox_height=18, checkbox_width=18, border_width=1, fg_color="black") \
                .grid(row=row, column=0, sticky="nwes")
            ttk.Separator(frame, orient="horizontal").grid(row=row, column=1, columnspan=3,sticky="we", padx=7)
            ckvar_count += 1
            column = 1
            for mood in moodslist:
                ctk.CTkCheckBox(master=frame, variable=self.ckvar[ckvar_count], command=checkEachCategory,text=mood, font=("", 12),
                                checkbox_height=18, checkbox_width=18, border_width=1, fg_color="black") \
                    .grid(row=row + 1, column=column, sticky="nw")
                column += 1
                ckvar_count += 1
            row += 2

            return row, ckvar_count

        def analyse_all_emotions():
            print("path = ", self.path)
            print("video frame rate= ", videoplayer.video_info()["framerate"])
            print("video frame size= ", videoplayer.video_info()["framesize"])

            # YOUR CODE GOES HERE

            # self.changePage("resultsPage")
            self.resultsPage()

        def analyse_selected_emotions():
            selectedMoods = []
            count = 1
            for k,v in self.moodsList.items():
                count+=1
                for mood in v:
                    if self.ckvar[count].get() == 1:
                        selectedMoods.append(mood)
                    count+=1

            print("selectedMoods = " , selectedMoods)

            # YOUR CODE GOES HERE

            # self.changePage("resultsPage")
            self.resultsPage()

        def buildMoodsCheckBoxes(frame):
            ckvar_count = 0
            row = 0
            for (category, moodslist) in self.moodsList.items():
                row, ckvar_count = buildEachRow(frame, category, moodslist, row, ckvar_count)

            ctk.CTkButton(master=frame, text="Analyse with all emotions", command=analyse_all_emotions, fg_color="black", text_color="white",
                          hover_color="#333").grid(row=row, column=0, padx=20, pady=20, columnspan=2)
            ctk.CTkButton(master=frame, text="Analyse with selected emotions", command=analyse_selected_emotions, fg_color="black", text_color="white",
                          hover_color="#333").grid(row=row, column=2, padx=20, pady=20, columnspan=2)

        # image = ctk.CTkImage(light_image=Image.open("icons/uploadedIcon.png"), size=(700, 60))
        # label = ctk.CTkLabel(master=self.app, image=image, text="", width=700)
        # label.grid(column=0, row=1, sticky="w", padx=10, pady=(10,10))

        page = ctk.CTkFrame(self.app, fg_color="white")
        page.grid(row=0, column=0, padx=10, sticky="news", rowspan=2)

        page_1 = ctk.CTkFrame(page, corner_radius=10, border_width=1, fg_color="white")
        page_1.grid(row=1, column=0, pady=10, padx=(10, 0), sticky="news")
        page_1.columnconfigure(0, weight=0)

        ctk.CTkLabel(page_1, text=f"Uploaded video:", text_color="#888").grid(column=0, row=1, sticky="w", pady=(10,0), padx=10)
        ctk.CTkLabel(page_1, text=f"{self.path}").grid(column=1, row=1, sticky="w")

        def initPage():
            # set everything to normal
            self.setupEmotionsVariable(1)
            self.path = ""
            self.changePage("initPage")

        ctk.CTkButton(master=page_1, text="Use another video", command=initPage, fg_color="black", text_color="white",
                      hover_color="#333").grid(row=2, column=0, padx=10, sticky="nw", pady=10)

        page_2 = ctk.CTkFrame(page, corner_radius=10, border_width=1, fg_color="white")
        page_2.grid(row=2, column=0, pady=10, padx=(10,0), sticky="news")
        page_2.columnconfigure(0, weight=0)

        ctk.CTkLabel(master=page_2, font=("Segoe UI", 18), text="Settings")\
            .grid(row=0, column=0, padx=20, pady=(12,0), sticky="w")

        cpane = cp(page_2, "Emotion Selector")
        cpane.grid(row=1, column=0, sticky="news", padx=15, pady=(5,5))

        buildMoodsCheckBoxes(cpane.frame)

        cpane2 = cp(page_2, "Timebased analytics")
        cpane2.grid(row=2, column=0, sticky="w", padx=15, pady=10)

        videoplayer, rangeSelector = self.buildVideoPlayer(self.path, cpane2.frame)

        def analyse_with_cropped_video():
            print("path = ", self.path)
            print("time = ", self.start_time_in_sec,
                  math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"]))
            print("video frame rate= ", videoplayer.video_info()["framerate"])
            print("video frame size= ", videoplayer.video_info()["framesize"])

            start_time, end_time = self.start_time_in_sec, math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"])
            # YOUR CODE GOES HERE

            self.resultsPage()

        bottombar = ctk.CTkFrame(cpane2.frame, fg_color="transparent", width=800, )
        bottombar.pack()

        ctk.CTkLabel(master=bottombar, text="Start: ").grid(row=0, column=0)

        start_time_label = ctk.CTkLabel(master=bottombar, textvariable=self.start_time_text)
        start_time_label.grid(row=0, column=1)
        self.start_time_in_sec = math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"])
        sec = math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"] % 60)
        min = math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"] / 60)
        hr = math.floor(rangeSelector.getValues()[0] * videoplayer.video_info()["duration"] / 3600)
        text = f'{"0" if hr <= 9 else ""}{hr}:{"0" if min <= 9 else ""}{min}:{"0" if sec <= 9 else ""}{sec}'
        self.start_time_text.set(text)

        tk.Frame(bottombar, width=300).grid(row=0, column=3)

        ctk.CTkButton(master=bottombar, text="Analyse",command=analyse_with_cropped_video, fg_color="black", text_color="white",
                      hover_color="#333").grid(row=0, column=3)

        ctk.CTkLabel(master=bottombar, text="End: ").grid(row=0,column=9)

        end_time_label = ctk.CTkLabel(master=bottombar, textvariable=self.end_time_text)
        end_time_label.grid(row=0,column=10)
        self.end_time_in_sec = math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"])
        sec = math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"] % 60)
        min = math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"] / 60)
        hr = math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"] / 3600)
        text = f'{"0" if hr <= 9 else ""}{hr}:{"0" if min <= 9 else ""}{min}:{"0" if sec <= 9 else ""}{sec}'
        self.end_time_text.set(text)

        cpane3 = cp(page_2, "Individual view")
        cpane3.grid(row=3, column=0, sticky="w", padx=15, pady=(10, 15))

        ctk.CTkLabel(master=cpane3, text="Enter roll number") \
            .grid(row=1, column=0, padx=20, sticky="ne", pady=10)

        textbox = ctk.CTkTextbox(master=cpane3, width=200, corner_radius=5, border_color="#aaa", border_width=1, height=20)
        textbox.grid(row=1, column=1, sticky="nw", pady=10)

        def analyse_with_given_roll_number():
            print("path = ", self.path)
            print("time = ", self.start_time_in_sec,
                  math.floor(rangeSelector.getValues()[1] * videoplayer.video_info()["duration"]))
            print("video frame rate= ", videoplayer.video_info()["framerate"])
            print("video frame size= ", videoplayer.video_info()["framesize"])

            roll_number = textbox.get('0.0', ctk.END)
            print("Given roll number= ", roll_number)
            if len(roll_number)==0:
                return

            # YOUR CODE GOES HERE

            self.resultsPage()

        ctk.CTkButton(master=cpane3, text="Analyse", command=analyse_with_given_roll_number, fg_color="black",
                      text_color="white",
                      hover_color="#333").grid(row=2, column=1, pady=5, sticky="nw")


        # page = ctk.CTkFrame(self.app, fg_color="transparent", width=320, )
        # page.grid(row=4, column=0, pady=(5,10), padx=10)

        # def backButton():
        #     self.changePage("initPage")
        #
        # ctk.CTkButton(master=page, text = "Back", command=backButton,  fg_color="black", text_color="white", hover_color="#333").grid(row=0, column=0, padx=20)


    def resultsPage(self):
        # ctk.CTkLabel(master=self.app, font=("Segoe UI", 24), text="Emo-Rooms").grid(row=0, column=0, padx=10, pady=5)

        page = ctk.CTkFrame(self.app, corner_radius=10, border_width=1, fg_color="white")
        page.grid(row=0, column=1, pady=10, padx=10, sticky="news")
        # page.columnconfigure(1, weight=1)

        tk.Frame(page, width=760, background="white").grid(row=0, column=0, columnspan=2)

        ctk.CTkLabel(master=page, font=("Segoe UI", 18), text="Summary") \
            .grid(row=0, column=0, padx=20, pady=(12, 0), sticky="n", columnspan=2)

        def showcharts():
            for path, dir, files in os.walk("results"):
                print(path, dir, files)
                for count, file in enumerate(files):
                    imgpath = os.path.join(path, file)

                    img = Image.open(imgpath)
                    img = img.resize((350,200))
                    img = ImageTk.PhotoImage(img)
                    label = tk.Label(page, image=img, height=200, width=300)
                    label.grid(row=1 if count<2 else 2, column=count%2, sticky="news", padx=(25,10), pady=(10,0))
                    label.image = img

        showcharts()

        page = ctk.CTkFrame(self.app, corner_radius=10, border_width=1, fg_color="white")
        page.grid(row=1, column=1, pady=10, padx=10, sticky="news")
        # page.columnconfigure(1, weight=1)

        ctk.CTkLabel(master=page, font=("Segoe UI", 18), text="Video view").pack(padx=5, pady=5)

        page_1 = tk.Frame(master=page)
        page_1.pack()

        # self.result_path
        self.buildVideoPlayer(self.result_path, page_1, False)

        # page = ctk.CTkFrame(page, fg_color="transparent", width=400, )
        # page.grid(row=2, column=0, pady=10, padx=10)

        # def backButton():
        #     self.changePage("settingsPage")



    def __delete__(self, instance):
        self.app.protocol('WM_DELETE_WINDOW', self.destructor)

    def destructor(self):
        self.app.destroy()

    def setupEmotionsVariable(self, value):
        self.ckvar = [tk.IntVar(value=value)]

        for k, v in self.moodsList.items():
            self.ckvar.append(tk.IntVar(value=value))
            for i in v:
                self.ckvar.append(tk.IntVar(value=value))

    def __init__(self):

        self.pages = {
            "initPage" : self.initPage,
            "progressPage" : self.progressIndicatorPage,
            "settingsPage" : self.settingsPage,
            "resultsPage" : self.resultsPage,
        }

        self.path = "song.mp4"
        self.result_path = "song.mp4"

        self.moodsList = {
            "Self-Conscious" : ["Shame", "Pride", "Shy"],
            "Knowledge" : ["Interest", "Confusion", "Relief"],
            "Hostile": ["Fear", "Anger", "Contempt"],
            "Pleasurable": ["Happiness", "Amusement", "Awe"],
        }

        self.description = "Emo-ROOM is an emotion analysis tool with unique features like time-based monitoring and individual tracking from uploaded videos. Users are provided with functionalities to select emotions and time intervals that they want to monitor. It uses different deep learning models and computer vision algorithms to accurately recognise facial action units to identify the facial emotion of students in a classroom. The tool is capable of detecting and identifying multiple students and continuously tracking them throughout the video."

        ctk.set_appearance_mode("light")  # default to system
        ctk.set_default_color_theme("dark-blue")
        self.app = tkinterDnD.Tk()
        self.app.title("Emo-rooms")
        self.app.config(bg="white")
        self.app.minsize(720, 480)
        # self.app.state("zoomed")
        self.app.attributes('-fullscreen', True)
        # self.app.maxsize(720, 880)

        self.start_time_text = tk.StringVar()
        self.end_time_text = tk.StringVar()
        # self.tempcanvas = tk.Canvas(self.app)
        # self.tempcanvas.grid(row=0, column=0)
        #
        # y_scrollbar = ttk.Scrollbar(self.app, orient=tk.VERTICAL, command=self.tempcanvas.yview)
        # y_scrollbar.grid(column=5, row=0, sticky='ns')
        #
        # self.tempcanvas.configure(yscrollcommand=y_scrollbar.set)
        # # my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(ALL)))
        #
        # self.canvas = tk.Frame(self.tempcanvas)
        # self.tempcanvas.create_window((0,0), window=self.canvas, anchor="nw")

        self.start_time_in_percentage = tk.DoubleVar()
        self.end_time_in_percentage = tk.DoubleVar()
        self.start_time_in_sec = 0
        self.end_time_in_sec = 0

        self.setupEmotionsVariable(1)

        self.changePage("settingsPage")

        self.app.mainloop()


if __name__ == '__main__':
    app = App()

