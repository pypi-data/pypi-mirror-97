import logging
from pathlib import Path
import os
from tkinter import ttk
from time import sleep
from ghettorecorder.lib.edit import UItextEditor
from ghettorecorder.lib import term
try:
    import tkinter as tk
except ImportError:
    print(f'\n\n  Please install --> python3-tk: on Ubuntu sudo apt-get install python3-tk\n\n')
try:
    from tkinter.filedialog import askdirectory, askopenfilename
except ImportError:
    print(f'\n error tkinter.filedialog import askdirectory, askopenfilename\n')

# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)


class UIWindow(tk.Tk):

    box_list = []
    search_list = []
    entry_list = []
    lbl_li = []

    timer_val = ['', 1, 2, 4, 6, 12, 24]
    data_dir_set = False
    record_started = False
    search_started = False

    info_text = [
        'Die Zeilen in der Mitte sind für Suchbegriffe da.',
        'Man sollte vorher im linken Kasten den Haken setzen. "Search"',
        'Begriffe wie: Elvis mozart band Beton, in die Zeile schreiben',
        'Es ist egal, ob das Wort GROSS oder klein geschrieben ist.',
        'Das Radio spielt den Titel mit dem Wort, Aufnahme beginnt.',
        'Bei schnellen Titelwechseln kann noch ein Teil des folgenden',
        'Titels aufgenommen werden. Einfach löschen.',
        '"Timer" oben rechts, wenn man nicht selber Stop drücken will.',
        'Der Timer ist die Eieruhr. nur in Stunden. Fertig! :)',
        'Die Uhr kann man jederzeit ändern. Viel Spaß!',
    ]

    info_te_eng = [
        'The lines in the middle area are used for searching phrases.',
        'Please activate the corresponding box on the left. "Search"',
        'Phrases like: Elvis mozart band concrete, can be written.',
        'There is no rule for writing the words UPPER or lower case.',
        'Radio station is playing a title with a search phrase! Record.',
        'Sometimes titles are published before or after the content',
        'changes. Get rid of the garbage files. Delete it.',
        'A "Timer" in the upper right corner. If you do not like pressing',
        'the "Stop" button yourself. One can change the value every time.',
        'Have fun!'
    ]

    def __init__(self, radio_dir=None, settings_path=None):
        super().__init__()
        self.gr_version = '0.1.1'
        self.radio_dir = radio_dir
        self.settings_path = settings_path

        self.title(f"Ghetto Recorder {self.gr_version} Concrete IT (by René Horn)")
        self.geometry('{}x{}'.format(620, 460))

        # main containers create
        self.top_frame = tk.Frame(master=self, bg='azure3', width=600, height=50, pady=3)
        self.center = tk.Frame(master=self, bg='gray2', width=50, height=40, padx=3, pady=3)
        self.info = tk.Frame(master=self, bg='azure3', width=50, height=2, padx=1, pady=1)
        self.btm_frame = tk.Frame(master=self, bg='azure3', width=600, height=40, pady=3)

        # main containers layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.top_frame.grid(row=0, sticky="ew")
        self.center.grid(row=1, sticky="nsew")
        self.info.grid(row=2, sticky="nsew")
        self.btm_frame.grid(row=3, sticky="ew")

        # center widgets create
        self.center.grid_rowconfigure(0, weight=1)
        self.center.grid_columnconfigure(1, weight=1)

        self.ctr_left = tk.Frame(self.center, bg='blue', width=25, height=190)
        self.canvas = tk.Canvas(self.center, bg='cornflowerblue', width=250, height=190, bd=0)
        self.ctr_mid = tk.Frame(self.center, bg='azure3', width=250, height=190, padx=3, pady=3)
        self.ctr_right = tk.Frame(self.center, bg='green', width=25, height=190, padx=3, pady=3)
        # center grid
        self.ctr_left.grid(row=0, column=0, sticky="ns")
        self.canvas.grid(row=0, column=1, sticky="nsew")

        self.ctr_mid.grid(row=0, column=1, sticky="nsew")
        self.ctr_right.grid(row=0, column=2, sticky="ns")
        self.ctr_mid.grid_remove()  # call .grid again

        # upper frame Buttons
        self.lbl_ini = tk.Label(self.top_frame, bg='azure3')
        self.btn_ini = tk.Button(self.top_frame, text="Radio list", width=10, command=self.browse_file_button)
        self.lbl_browse = tk.Label(self.top_frame, bg='azure3')
        self.btn_browse = tk.Button(self.top_frame, text="Save to ...", width=10, command=self.browse_dir_button)
        self.lbl_timer = tk.Label(self.top_frame, text='Timer', bg='azure3', anchor="s")
        self.combo_timer = ttk.Combobox(self.top_frame, state="readonly", width=5, values=self.timer_val)

        self.entry_ini = tk.Entry(self.top_frame, background="white", borderwidth=1, relief=tk.FLAT, width=70)
        self.entry_ini.insert(0, ' Path to settings.ini')
        self.entry_bbr = tk.Entry(self.top_frame, background="white",  borderwidth=1, relief=tk.FLAT, width=70)
        self.entry_bbr.insert(0, ' place to create a bunch of folders')

        # upper frame layout

        self.lbl_ini.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.btn_ini.grid(row=0, column=1, padx=2, pady=2, sticky='w')
        self.entry_ini.grid(row=0, column=2, columnspan=3, padx=5, sticky='e')
        self.lbl_timer.grid(row=0, column=5, padx=10, sticky="s")

        self.lbl_browse.grid(row=1, column=0, padx=2, pady=2, sticky="w")
        self.btn_browse.grid(row=1, column=1, padx=2, sticky='w')
        self.entry_bbr.grid(row=1, column=2, columnspan=3, padx=5, sticky='e')
        self.combo_timer.grid(row=1, column=5, padx=10, sticky='e')

        # center right
        self.progressbar = ttk.Progressbar(self.ctr_right, orient="vertical", length=350, mode="determinate")
        # bottom

        self.lbl_rec = tk.Label(master=self.btm_frame, bg='azure3', anchor="s")
        self.btn_editor = tk.Button(master=self.btm_frame, text="Radio Editor",
                                    width=10,  padx=2, pady=1, command=UItextEditor)
        self.btn_stop = tk.Button(master=self.btm_frame, text="Stop", width=10, padx=2, pady=1, command=self.exit_app)
        self.btn_rec = tk.Button(master=self.btm_frame, text="Record", width=10,
                                 padx=2, pady=1, command=self.list_checked)
        self.lbl_info = tk.Label(master=self.btm_frame, bg='azure3', anchor="s")

        # bottom grid
        self.lbl_rec.grid(row=0, column=0, padx=10, sticky="w")
        self.btn_editor.grid(row=0, column=1, sticky='e')
        self.btn_stop.grid(row=0, column=2, sticky='w')
        self.btn_rec.grid(row=0, column=3, sticky='w')
        self.lbl_info.grid(row=0, column=4, sticky='e')

        self.canvas.create_rectangle(0, 0, 250, 190, fill='cornflowerblue', width=0)
        self.canvas.create_line(0, 125, 2000, 125, fill='orange', width=10)
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)

        # show path to settings.ini
        ini_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.ini")
        term.GBase.settings_path = ini_file
        self.entry_ini.delete(0, tk.END)
        self.entry_ini.insert(0, ini_file)
        self.lbl_info.config(text='Oben links der Knopf ist für die Datei mit den Web Radios.')

    def on_enter(self, event):
        self.canvas.create_line(0, 225, 2000, 225, fill='orange', width=10, tag="line")

    def on_leave(self, enter):
        self.canvas.delete("line")

    def set_settings_path(self, settings_path):
        self.settings_path = settings_path

    def get_settings_path(self):
        return self.settings_path

    def set_radio_dir(self, radio_dir):
        self.radio_dir = radio_dir

    def get_radio_dir(self):
        return self.radio_dir

    def browse_dir_button(self):
        dir_name = askdirectory(title='Ghetto Recorder')
        if not dir_name:
            return
        self.set_radio_dir(dir_name)
        self.entry_bbr.delete(0, tk.END)
        self.entry_bbr.insert(0, dir_name)
        term.GBase.radio_base_dir = dir_name
        # self.lbl_browse.config(text=dir_name)
        self.data_dir_set = True
        return dir_name

    def browse_file_button(self):
        filepath = askopenfilename(
            filetypes=[("INI Files", "*.ini"), ("All Files", "*.*")],
            title='Ghetto Recorder',
            initialdir=os.path.dirname(os.path.abspath(__file__))
        )
        if not filepath:
            return
        self.set_settings_path(filepath)
        self.entry_ini.delete(0, tk.END)
        self.entry_ini.insert(0, filepath)

        term.GBase.settings_path = filepath  # set new path
        term.GIni.show_items_ini_file()
        # get the radios
        self.load_settings(term.GIni.list_items, self.ctr_mid)  # only keys, not values
        self.btn_ini = tk.Button(self.top_frame, text="Radio list", width=10, state="disabled")
        self.btn_ini.grid(row=0, column=1, sticky='w')

        return filepath

    def print_dir(self):
        data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "radiostations")
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kreuzberg")
        try:
            with open(test_file, 'wb') as record_file:

                record_file.write(b'\x03')
            os.remove(test_file)

            if not self.data_dir_set:

                term.GBase.radio_base_dir = data_folder
                term.GBase.make_directory(data_folder)
                self.entry_bbr.delete(0, tk.END)
                self.entry_bbr.insert(0, data_folder)

        except Exception as ex:
            print(ex)
            self.entry_bbr.delete(0, tk.END)
            self.entry_bbr.insert(0, 'My directory is read only')

    def exit_app(self):
        term.GBase.exit_app = True
        sleep(term.GBase.sleeper + 1)  # threads sleep too, time for exit
        self.btn_rec = tk.Button(master=self.btm_frame, text="Record", width=10, command=self.list_checked)
        self.btn_rec.grid(row=0, column=3, sticky='w')
        term.GBase.exit_app = False

    def cb_checked(self):
        is_playlist_server = ''
        for ctr, int_var in enumerate(self.box_list):
            if int_var.get():     # IntVar not zero==checked
                self.lbl_li[ctr].configure(foreground='black')  # <widget>.configure(foreground='black',bg='red')

    def cb_search(self):
        for ctr, int_var in enumerate(self.search_list):
            # search checkbox selection
            if int_var.get():  # IntVar not zero==checked
                self.entry_list[ctr].delete(0, tk.END)
                # set the related record check box
                self.box_list[ctr].set(1)
                self.lbl_li[ctr].configure(foreground='red')  # <widget>.configure(foreground='black',bg='red')
                print(self.lbl_li[ctr].cget("text"))

    def load_settings(self, list_of_widgets, frame):

        self.print_dir()
        self.box_list = []
        self.search_list = []
        # remove start screen
        self.ctr_mid.grid()
        self.canvas.grid_remove()
        tk.Label(frame, text='Record', underline=0 , bg='azure3').grid(row=0, column=2, sticky="e")
        tk.Label(frame, text='Add search (Record if match - multi): podcast concert elvis', underline=0,
                 bg='azure3').grid(row=0, column=1, sticky="n")
        tk.Label(frame, text='Search', bg='azure3').grid(row=0, column=0, sticky="w")
        tk.Label(frame, text='Radio', bg='azure3').grid(row=0, column=3, sticky="w")

        term.GBase.pool.submit(self.display_info_text)

        for idx, text in enumerate(list_of_widgets):

            self.box_list.append(tk.IntVar())  # auto var from python PY_VAR0 1 2 for finding check buttons
            self.search_list.append(tk.IntVar())
            lbl = tk.Label(frame, text=text, bg='azure3')
            lbl.grid(row=idx + 1, column=3, sticky="w")
            self.lbl_li.append(lbl)

            entry = tk.Entry(frame, width=60, bg='azure3')
            entry.grid(row=idx + 1, column=1, sticky="w")

            self.entry_list.append(entry)
            tk.Checkbutton(frame, variable=self.search_list[-1],
                           command=self.cb_search, bg='azure3').grid(row=idx + 1, column=0, sticky='e')

            tk.Checkbutton(frame, variable=self.box_list[-1],
                           command=self.cb_checked, bg='azure3').grid(row=idx + 1, column=2, sticky='e')

    def list_checked(self):

        for ctr, int_var in enumerate(self.box_list):
            # all checked rec.
            if int_var.get():

                # all get a string, that is never found
                term.GIni.search_dict[self.lbl_li[ctr].cget("text")] = "x!c?42"

                # SEARCH check only metadata, start rec. if found
                self.record_started = True
                if self.search_list[ctr].get():  # not zero = True
                    self.search_started = True
                    # update dict for threads going to search def GRecorder.search_pattern_start_record
                    term.GIni.search_dict[self.lbl_li[ctr].cget("text")] = self.entry_list[ctr].get()
                    term.GIni.search_title_keys_list.append(self.lbl_li[ctr].cget("text"))
                    sleep(2)
                    # update label with search content from entry
                    self.lbl_info.config(text=self.entry_list[ctr].get())

                # PLAYLIST is handled in add_server_to..UI, bit diff. than in terminal
                self.add_server_to_data_base_ui(str(self.lbl_li[ctr].cget("text")),
                                                str(term.GIni.find_ini_file(self.lbl_li[ctr].cget("text"))))

        self.btn_rec = tk.Button(master=self.btm_frame, text="Record", width=10, state="disabled")
        self.btn_rec.grid(row=0, column=3, sticky='w')

        # here updated list, zombies deleted
        for key in term.GIni.ini_keys:
            term.test_stream_server(key)

        for key in term.GIni.ini_keys:
            term.GBase.pool.submit(self.start_records, key)

        term.GBase.pool.submit(self.display_title)

        # if selected, start timer
        if self.combo_timer.get():
            new_timer = int(self.combo_timer.get()) * 3600  # 60s * 60m = ?
            term.GBase.pool.submit(self.timer, new_timer)
            self.progressbar.grid(row=0, column=0, sticky='s')

    @staticmethod
    def start_records(key):

        # ----- no del -- term.GRecorder.thread_pull_song_name(url, key, None, None)
        stream_suffix = term.GIni.srv_param_dict[key + '_file']
        term.GIni.song_dict[key] = str('_no-name-record_no_split_')  # init the dict for this thread
        term.GIni.start_stop_recording[key] = 'start'
        term.GIni.start_stop_recording[key + '_adv'] = 'start_from_here'

        for _ in term.GIni.search_title_keys_list:
            if _ == key:
                term.GIni.start_stop_recording[key] = 'stop'

        url = term.GIni.ini_keys[key]
        print(f'{key} {url}')
        dir_save = term.GBase.radio_base_dir + '//' + key
        term.GBase.pool.submit(term.GRecorder.record_songs, url, dir_save, stream_suffix, key, None)
        term.GRecorder.path_to_song_dict = term.GIni.song_dict
        term.GBase.pool.submit(term.GRecorder.thread_pull_song_name, url, key, None, None)

    def display_title(self):

        while not term.GBase.exit_app:
            for idx, var in enumerate(self.box_list):
                if var.get():
                    radio = str(self.lbl_li[idx].cget("text"))
                    self.entry_list[idx].delete(0, tk.END)
                    try:
                        title = term.GRecorder.path_to_song_dict[radio]
                        self.entry_list[idx].insert(0, title)
                    except Exception as ex:
                        print(ex)

            for sec in range(10):
                sleep(1)
                if term.GBase.exit_app:
                    break

    @staticmethod
    def add_server_to_data_base_ui(str_key, str_val):
        is_playlist_server = ''
        term.GIni.ini_keys[str_key] = str_val  # append url to dictionary as value
        term.GBase.make_directory(term.GBase.radio_base_dir + '//' + str_key)
        # playlist url?
        if str_val[-4:] == '.m3u' or str_val[-4:] == '.pls':  # or url[-5:] == '.m3u8' or url[-5:] == '.xspf':
            # take first from the list
            is_playlist_server = UIUtils.playlist_m3u(str_val)
        if not is_playlist_server == '':  # update dictionary with new url
            term.GIni.ini_keys[str_key] = is_playlist_server  # append dictionary, test if it is alive
            if not term.GNet.is_server_meta_stream(term.GIni.ini_keys[str_key]):
                print('   --> playlist_server server failed, no recording')
                del term.GIni.ini_keys[str_key]
        if not term.GNet.is_server_meta_stream(term.GIni.ini_keys[str_key]):  # first time internet access, response code
            # delete key from dict, return
            del term.GIni.ini_keys[str_key]

    def timer(self, time_left):
        combo_time = 0
        current_timer = 0
        while time_left - current_timer:
            current_timer += 1
            self.progress(current_timer, time_left)
            sleep(1)
            if self.combo_timer.get():
                combo_time = int(self.combo_timer.get()) * 3600
            if not combo_time == time_left:
                time_left = combo_time
            if term.GBase.exit_app:
                break
            if not self.record_started:
                break

        term.GBase.exit_app = True
        sleep(term.GBase.sleeper + 1)  # threads sleep too, time for exit
        term.GBase.exit_app = False
        self.btn_rec = tk.Button(master=self.btm_frame, text="Record", width=10, command=self.list_checked)
        self.btn_rec.grid(row=0, column=3, sticky='w')

    def progress(self, current_timer, max_value):
        # progressbar['value'] = 20 , is the percentage from 100, combobox returns string value
        # doing some math, p = (P * 100) / G, percent = (math.percentage value * 100) / base
        cur_percent = round((current_timer * 100) / max_value, 0)
        # print(f'cur_percent {cur_percent}  current_timer {current_timer} max {max_value}')
        self.progressbar['value'] = cur_percent
        self.update_idletasks()
        sleep(1)

    def display_info_text(self):

        while not term.GBase.exit_app:
            if self.search_started or self.record_started:
                self.lbl_info.config(text=' ')
                break
            for line in UIWindow.info_text:
                self.lbl_info.config(text=line)
                for _ in range(10):
                    if self.search_started or self.record_started:
                        self.lbl_info.config(text=' ')
                        break
                    sleep(1)

            for line in UIWindow.info_te_eng:
                self.lbl_info.config(text=line)
                for _ in range(10):
                    if self.search_started or self.record_started:
                        self.lbl_info.config(text=' ')
                        break
                    sleep(1)


class UIUtils(UIWindow):

    def __init__(self, radio_dir=None, settings_path=None):
        super().__init__()

    @staticmethod
    def playlist_m3u(url):
        # returns the first server of the playlist
        try:
            read_url = term.GNet.http_pool.request('GET', url, preload_content=False)
        except Exception as ex:
            print(ex)
        else:
            file = read_url.read().decode('utf-8')

            m3u_lines = file.split("\n")
            # print(' \n    m3u_lines    ' + file)
            m3u_lines = list(filter(None, m3u_lines))  # remove empty rows
            m3u_streams = []
            for row_url in m3u_lines:
                if row_url[0:4].lower() == 'http'.lower():
                    m3u_streams.append(row_url)  # not to lower :)
                    # print(len(m3u_streams))

            if len(m3u_streams) > 1:
                print(' !!! Have more than one stream in playlist_m3u. !!! Take first stream available.')
                play_server = m3u_streams[0]
                return play_server
            if len(m3u_streams) == 1:
                # print(' One server found in playlist_m3u')
                play_server = m3u_streams[0]
                return play_server
            if len(m3u_streams) == 0:
                # print(' No http ... server found in playlist_m3u !!! -EXIT-')
                return False

    @staticmethod
    def sum(arg):
        total = 0
        for val in arg:
            total += val
        return total

if __name__ == "__main__":
    uiw = UIWindow()
    uiw.mainloop()




