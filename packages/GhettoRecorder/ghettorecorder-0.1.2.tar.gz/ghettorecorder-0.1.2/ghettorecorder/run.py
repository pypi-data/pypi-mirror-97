# 0.1.2a
##################################################################################
#   MIT License
#
#   Copyright (c) [2021] [René Horn]
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
###################################################################################
import configparser
import io
import json
import logging
import os
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, wait
from concurrent.futures._base import ALL_COMPLETED, Executor, as_completed
from time import sleep, strftime, time
import urllib3
##############
import getpass
import shutil
import stat

# logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

# Could anyone please explain ... what it does?
# Well, this SCRIPT reads the data stream from a radio station into separate files.
# The data stream is SPLIT INTO PIECES, mostly "ARTIST - Title.MP3" style. Plus ".m3u" and ".pls" play list support.
# 'This' world is tumbling down. Record it with     !!! Ghetto RECORDER !!!
# Be brave, be curious!                                 rene_horn@gmx.net


# Usage:
# Runs on Python 3.5: R E A D --> (Windows 'pip'/Linux 'pip3, python3')
# Go to the next free internet WLAN.
# Windows Store/Linux package manager, install latest Python3 version.
# 'pip install ghettorecorder' - with a normal user account!
# 'pip show ghettorecorder' to find the install Location: site-packages/ghettorecorder /
# 'python - m ghettorecorder.run' will run the recorder from anywhere on your computer.
# GhettoRecorder is uninstalled by 'pip uninstall gettorecorder'. Recorded mp3 files not.
#  Copy 'run.py' and 'settings.ini' files wherever you want to have your record repository.
#  Windows let's you double click 'run.py'. Can run from desktop.
# Magic number 42 is used to connect to all radios found in 'settings.ini'.

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # go to .py script folder
username = getpass.getuser()

exit_app = False
urllib3.disable_warnings()
# print(sys.version)


def switch_dst_dir(container):  # if app runs in a container

    global username
    print('Hello, ' + username)
    if container == 'SNAP':
        ghetto_folder = '//home//' + username + '//GhettoRecorder'
    else:
        ghetto_folder = '//tmp//GhettoRecorder'  # DOCKER

    # set new radio_base_dir class attribute
    GBase.radio_base_dir = ghetto_folder

    source_ini = os.path.dirname(os.path.abspath(__file__)) + '//settings.ini'
    source_script = os.path.dirname(os.path.abspath(__file__)) + '//StartGhetto.sh'
    dst_ini = ghetto_folder + '//settings.ini'
    dst_script = ghetto_folder + '//StartGhetto.sh'

    access_rights = 0o755
    try:
        os.mkdir(ghetto_folder, access_rights)
    except FileExistsError:
        pass

    try:
        if not os.path.exists(dst_ini):
            shutil.copyfile(source_ini, dst_ini)
            shutil.copyfile(source_script, dst_script)
    except FileExistsError:
        pass
    st = os.stat(dst_script)
    os.chmod(dst_script, st.st_mode | stat.S_IEXEC)


def signal_handler(sig, frame):
    global exit_app
    print(' Stop recording ...')
    exit_app = True
    GBase.exit_app = True
    # sleep(3)  # give thread def: time for clean exit -
    sys.exit()


class GBase:
    # class attribute
    exit_app = False
    sleeper = 2
    pool = ThreadPoolExecutor(200)
    radio_base_dir = os.path.dirname(os.path.abspath(__file__)) + '//radiostations'  # if not set set_radio_base_dir()
    settings_path = os.path.dirname(os.path.abspath(__file__)) + '//settings.ini'  # if not set in set_settings_path()
    path = os.getcwd()
    path_to = path + '//'
    timer = 0

    def __init__(self, radio_base_dir=None, settings_path=None):
        self.instance_attr_time = 0
        self.trigger = False
        self.radio_base_dir = radio_base_dir
        self.settings_path = settings_path

    @staticmethod
    def make_directory(str_path):
        access_rights = 0o755
        try:
            os.mkdir(str_path, access_rights)
        except FileExistsError:
            pass
            # print(' Folder exists: ' + str_path)
            return False
        else:
            print('Successfully created the directory: ' + str_path)
            return True

    @staticmethod
    def remove_special_chars(str_name):
        # cleanup for writing files and folders

        # my_str = "hey th~!ere. /\ coolleagues?! Straße"
        ret_value = str_name.translate({ord(string): "" for string in '"!@#$%^*()[]{};:,./<>?\|`~=+"""'})
        return ret_value

    @staticmethod
    def this_time():
        time = strftime("%Y-%m-%d %H:%M:%S")
        return time

    def countdown(self, instance_attr_time):
        t = 0
        while not t == instance_attr_time:
            sleep(1)
            self.timer = t
            print(self.timer)
            t += 1
            if t == 0:
                self.trigger = True
        print(f' done {instance_attr_time} {self.trigger}')
        return self.trigger


class GIni(GBase):

    ini_keys = {}        # cls attribute to store selections from ini file, works because of key[key] = value, else not
    srv_param_dict = {}  # all ini keys plus short url, suffix, server type stuff
    song_dict = {}       # recorder reads song title from key, related to the url in settings.ini
    start_stop_recording = {}  # ini key: 'start' , 'stop'; while loop check start, working check stop go upper while
    # ini_key + '_single_title', ini_key + '_rec_from_here'
    cost_current_ini = ''  # ini key for cost_dict calc / should be a dict
    cost_dict = {}        # stores len of received headers to calc amount of data searching strings per day
    fail_meta_dict = {}  # can not read metadata from stream, no data
    # list of search strings delimiter blank, first key is named 'STRINGS': Britney Phantom ไม่เคยจะจำ Elton Jim techno
    search_dict = {'STRINGS': 'Britney Spears ไม่เคยจะจำ Elton AC/DC techno Band feat. mix'}  # only show it is working
    list_items = []
    search_title_keys_list = []  # radio short keys, not start recording all streams, only searched titles

    def __init__(self):
        super().__init__()

    @staticmethod
    def show_items_ini_file():

        config = configparser.ConfigParser()  # imported library to wok with .ini files
        try:
            config.read_file(open(GBase.settings_path))
        except FileNotFoundError as ex:
            print(ex)
            sys.exit()
        else:

            i = 0

            print('\t  _______       __  __       ___                      __       ')
            print('\t / ___/ /  ___ / /_/ /____  / _ \___ _______  _______/ /__ ____')
            print('\t/ (_ / _ \/ -_) __/ __/ _ \/ , _/ -_) __/ _ \/ __/ _  / -_) __/')
            print('\t\___/_//_/\__/\__/\__/\___/_/|_|\__/\__/\___/_/  \_,_/\__/_/   ')
            print('                                                       Elvis lebt')
            for _ in dict(config.items('STATIONS')):
                GIni.list_items.append(_)
            for _ in GIni.list_items:
                print('\t>> %-20s <<' % _)

            print(' \n Radio stations in your list. ')
        return

    @staticmethod
    def find_ini_file(key_name):
        config = configparser.ConfigParser()  # imported library to work with .ini files
        try:
            config.read_file(open(GBase.settings_path))
        except FileNotFoundError as ex:
            print(ex)
            sys.exit()
        else:

            station_value = 'False'  # init var for return value
            stations = config['STATIONS']

            try:
                station_value = stations[key_name]  # if all ok get a valid string of value -> True
            except KeyError as ex:
                print(ex)
                print('-- FALSE radio station, input was ->>> ' + key_name)

        return station_value  # single value

    @staticmethod
    def find_all_in_stations():

        config = configparser.ConfigParser()  # imported library to work with .ini files
        try:
            config.read_file(open(GBase.settings_path))
        except FileNotFoundError as ex:
            print(ex)
            sys.exit()
        else:
            stations = config['STATIONS']

        return stations  # list of values

    @staticmethod
    def parse_url_simple_url(radio_url):
        url = radio_url  # whole url is used for connection to radio server

        # 'http:' is first [0], 'ip:port/xxx/yyy' second item [1] in list_url_protocol
        list_url_protocol = url.split("//")
        list_url_ip_port = list_url_protocol[1].split("/")  # 'ip:port' is first item in list_url_ip_port
        radio_simple_url = list_url_protocol[0] + '//' + list_url_ip_port[0]
        return radio_simple_url


class GNet(GBase):
    
    is_shout_dict = {}
    is_ice_dict = {}
    is_ice_json_dict = {}
    is_unk_dict = {}
    is_no_meta_avail_dict = {}
    
    http_pool = urllib3.PoolManager(num_pools=200)
    request = ''
    ua_standard = {'Icy-MetaData': '1', 'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}
    query_shoutcast = '/currentsong'

    def __init__(self):
        super().__init__()

    @staticmethod
    def playlist_server(url):

        play_list_server = ''
        if url[-5:] == '.m3u8' or url[-5:] == '.xspf':
            print(' .m3u8/.xspf play lists not yet supported')
            sys.exit()

        if url[-4:] == '.m3u' or url[-4:] == '.pls':  # or url[-5:] == '.m3u8' or url[-5:] == '.xspf':
            read_url = GNet.http_pool.request('GET', url, preload_content=False)
            print(' \n        --- | ---')
            print(read_url.read().decode('utf-8'), end="")
            print(" \n        --- | ---")
            try:
                play_list_server = input('copy and paste a server from above, here ->: ')
            except Exception as ex:
                print(ex)
                print(' exception: input error ')
                return False

        else:
            return False

        return play_list_server.strip()
 
    @staticmethod
    def is_server_meta_stream(url):
        # print('\n(  ( ((GR)) )  ) \t' + url + ' Click the url to listen.')
        # meta info header, if content-type is found do not go tu suffix check
        try:
            print(url)
            request = GNet.http_pool.request('GET', url, headers=GNet.ua_standard, preload_content=False)

        except Exception as ke:
            print('   --> server failed, no recording ' + url)
            print(ke)
            return False
        else:
            if request.status != 200:
                request.release_conn()
                return False
            return True

    @staticmethod
    def is_server_alive(server_name):  # if interc. w. is_server_meta_stream d_kultur swr2_streamuse fail to get name?
        # print(' is_server_alive {server_name}')
        try:
            response = GNet.http_pool.request('GET', server_name, headers=GNet.ua_standard, preload_content=False)
            print(f' response status: {response.status} {server_name}')
        except Exception as ex:
            print(repr(ex))  # zombie server
            return False
        else:
            return True

    @staticmethod
    def is_server_shoutcast(server_name, key):

        try:
            request = GNet.http_pool.request('GET', server_name, preload_content=False, retries=10)  # winamp
            if not request.headers['icy-notice1'].find('http://www.winamp.com') == -1:  # find() -1 fail
                GNet.is_shout_dict[key] = True
                # GIni.cost_dict[GIni.cost_current_ini] = len(request.headers)
        except KeyError:
            # print(repr(ex))
            # print(' no Shoutcast stream')
            return False
        else:
            return True

    @staticmethod
    def is_server_icecast(server_name, key):

        try:
            request = GNet.http_pool.request('GET', server_name, preload_content=False)  # 'server'
            substr_start_num = request.headers['server'].lower().find("icecast")
            if not substr_start_num == -1:  # -1 false from find()
                GNet.is_ice_dict[key] = True
                return True
            else:
                print(f' server type: {request.headers["server"]}')
        except KeyError:
            # print(repr(ex))
            # print(' Exception in is_server_icecast ')
            return False

    @staticmethod
    def ice_status_json(request):
        data_stats_source_title = False
        source = request.read()
        data = json.loads(source)

        data_stats = data.get('icestats')
        data_stats_source = data_stats.get('source')
        try:
            data_stats_source_title = data_stats_source.get('title')
        except AttributeError:
            # print(repr(e))
            data_stats_source = data_stats.get('source')
            data_stats_source_title = data_stats_source[0]['title']

        GIni.cost_dict[GIni.cost_current_ini] = len(source)
        return data_stats_source_title

    @staticmethod
    def is_server_icecast_status_json(server_name, full_url, key):

        try:
            request = GNet.http_pool.request('GET', server_name + '/status-json.xsl', preload_content=False)
            song_title = GNet.ice_status_json(request)

        except Exception as ex:
            print(ex)
            print(' server got no readable json file \n will read from stream directly \n')
            return False

        return song_title

    @staticmethod
    def stream_filetype(server_name):

        request = GNet.http_pool.request('GET', server_name, headers=GNet.ua_standard, preload_content=False)
        content_type = ''
        try:
            request.headers
        except Exception as ex:
            print(ex)
            print(' stream_filetype in EXCEPTION')
        else:
            if request.headers['content-type'] == 'audio/aacp' or request.headers['content-type'] == 'application/aacp':
                content_type = '.aacp'
            if request.headers['content-type'] == 'audio/aac':
                content_type = '.aac'
            if request.headers['content-type'] == 'audio/ogg' or request.headers['content-type'] == 'application/ogg':
                content_type = '.ogg'
            if request.headers['content-type'] == 'audio/mpeg':
                content_type = '.mp3'
            if request.headers['content-type'] == 'audio/x-mpegurl' or request.headers['content-type'] == 'text/html':
                content_type = '.m3u'
            # application/x-winamp-playlist , audio/scpls , audio/x-scpls ,  audio/x-mpegurl

            return content_type

    @staticmethod
    def is_shout_ice_unknown_server(server_port, full_url, key):

        response = GNet.is_server_alive(server_port)
        if not response:
            print(' is_server_alive ' + server_port + 'Can not get the server. Exit')
            return
        else:
            GNet.is_server_shoutcast(server_port, key)
            if not GNet.is_shout_dict[key]:
                GNet.is_server_icecast(server_port, key)
                if GNet.is_ice_dict[key]:
                    if GNet.is_server_icecast_status_json(server_port, full_url, key):
                        # http://stream.dancewave.online:8080/retrodance.mp3/status-json.xsl full url
                        GNet.is_ice_json_dict[key] = True

            if not GNet.is_ice_json_dict[key]:
                if not GNet.is_shout_dict[key]:
                    GNet.is_unk_dict[key] = True
                    req = GNet.http_pool.request('GET', full_url, headers={'Icy-MetaData': '1'}, preload_content=False)
                    try:
                        GNet.icy_metadata = int(req.headers['icy-metaint'])
                        print(f' chunk size {GNet.icy_metadata} {key}')
                        # GIni.cost_dict[GIni.cost_current_ini] = GNet.icy_metadata
                        # chunk size, calculate request one day (title search)
                        # write in dict for no metadata = true
                    except Exception as ex:
                        print(ex)
                        print(' server has no metadata - try record into one file ')
                        GNet.is_no_meta_avail_dict[key] = True


class GRecorder:

    stream_song_name = '_no-name-record_no_split_'
    path_to_song_dict = {}  # each thread writes the new title to the station key name {station : title}

    def __init__(self, url, ini_key):
        self.url = url
        self.ini_key = ini_key

    @staticmethod
    def thread_pull_song_name(url, ini_key, params_dict, path_to_song_dict):
        # print(f'=== thread_pull_song_name ... ')
        update_terminal = False
        stream_song_name = GRecorder.path_to_song_dict[ini_key]
        GIni.fail_meta_dict[url] = 'False'

        while not GBase.exit_app:

            if GIni.srv_param_dict[ini_key + '_is_unknown_server'] == 'True':
                if not GIni.fail_meta_dict[url] == 'True':  # let record go in one file
                    ret = GRecorder.get_metadata_from_stream(url)  # read one time from stream
                    stream_song_name = ret

            if GIni.srv_param_dict[ini_key + '_is_icecast_json'] == 'True':
                ice_short_url = GIni.srv_param_dict[url]  # get http://ip:port from full url
                # ice_short_url = GIni.parse_url_simple_url(url)
                # call def for reading json file
                stream_song_name = GNet.is_server_icecast_status_json(ice_short_url, ice_short_url, ini_key)

            if GIni.srv_param_dict[ini_key + '_is_shoutcast_server'] == 'True':
                srv = GIni.srv_param_dict[url]  # get http://ip:port from full url
                srv_current = srv + '/currentsong'
                response = GNet.http_pool.request('GET', srv_current, headers=GNet.ua_standard, preload_content=False)
                stream_song_name = response.data.decode('utf-8')

            if GIni.srv_param_dict[ini_key + '_is_no_meta_data_avail'] == 'True':
                stream_song_name = '_no-name-record_no_split_'
                # print(' _is_no_meta_data_avail ' + stream_song_name)

            if not len(stream_song_name) <= 2:
                GRecorder.path_to_song_dict[ini_key] = stream_song_name
                # print(f' <<<<<<<<<<<<<<<{ini_key} GRecorder.path_to_song_dict: {GRecorder.path_to_song_dict}')
                if not update_terminal == stream_song_name:
                    update_terminal = stream_song_name
                    print('\t\t title on ' + ini_key + ':\t' + update_terminal)
            # give recorder command to record, we got a match from search
            GIni.search_title_keys_list.append(42)
            try:
                for _ in GIni.search_title_keys_list:
                    if _ == ini_key:
                        # if some phrases are found in def search_pattern_start_record
                        got_it = GRecorder.search_pattern_start_record(stream_song_name, ini_key)
                        if got_it:
                            GIni.start_stop_recording[ini_key] = 'start'
                        else:
                            GIni.start_stop_recording[ini_key] = 'stop'

            except Exception as ex:
                print(ex)
            # GRecorder.search_pattern_start_record(stream_song_name, ini_key)
            # print(GIni.start_stop_recording)
            sleep(GBase.sleeper)

            if GBase.exit_app:
                print(f' stop get title {ini_key}')

    @staticmethod
    def search_pattern_start_record(title, ini_key):
        # search title for strings to see if we should start recording this song/title
        search_list = []  # chop the string
        try:
            strings = GIni.search_dict[ini_key]  # dict with user search strings
            # print(f' strings; {strings} {ini_key}' )
            search_list = strings.encode('utf-8').lower().split(b' ')
        except KeyError as ex:
            pass

        for search_str in search_list:

            if not len(search_str) <= 1:  # b'' match problem

                if not title.encode('utf-8').lower().find(search_str) == -1:  # find() returns -1, if not found
                    print(f'<<< match station: {ini_key} phrase: {search_str}')
                    # GIni.start_stop_recording[ini_key + '_adv'] = 'start_from_here'
                    return True
        return False

    @staticmethod
    def record_songs(url, directory_save, stream_suffix, radio_short_key, path_to_song_dict):
        # print('record_songs')
        stream_request_size = io.DEFAULT_BUFFER_SIZE
        fresh_song = 'False'
        old_time = time()
        sleeper_recorder = False

        try:
            if GIni.start_stop_recording[radio_short_key] == 'stop':
                sleeper_recorder = True
        except KeyError:
            pass

        sleep(GBase.sleeper + 1)  # wait to get song name from def: thread_pull_song_name
        stream_song_name = GRecorder.path_to_song_dict[radio_short_key]

        try:
            request = GNet.http_pool.request('GET', url, preload_content=False, retries=10)
        except urllib3.exceptions.NewConnectionError:
            print('Connection failed. ' + url)
        else:
            # print(' \n Recording ... ')
            request.auto_close = False  # NOT DEL !!! :) , for continuous recording fine

            while not GBase.exit_app:
                while not GBase.exit_app:
                    if GIni.start_stop_recording[radio_short_key] == 'stop':
                        sleep(.1)
                    else:
                        # print(f'----> else {radio_short_key} sleeper_recorder {sleeper_recorder}'
                        #      f' dict {GIni.start_stop_recording[radio_short_key]}')
                        if sleeper_recorder:
                            print(f'----> start record: {radio_short_key}')
                            try:
                                # recorder def looses connect if too long idle
                                request = GNet.http_pool.request('GET', url, preload_content=False, retries=10)
                            except urllib3.exceptions.NewConnectionError:
                                pass
                        break
                i = 0
                while not GBase.exit_app:  # outer loop create empty new files

                    if GIni.start_stop_recording[radio_short_key] == 'stop':
                        print(f'----> stop record: {radio_short_key}')

                        break

                    if not fresh_song == stream_song_name:

                        fresh_song = stream_song_name  # check if it can be removed, we look in a dict now
                        clean_name = GBase.remove_special_chars(stream_song_name)

                        if clean_name == '_no-name-record_no_split_':  # init name of title on startup
                            clean_name = clean_name + GBase.this_time()
                            clean_name = GBase.remove_special_chars(clean_name)

                        fresh_file = directory_save + '//' + clean_name + stream_suffix
                        if i == 5:
                            print(f' \t\t\t\t\t\t(  (  ( (Ghetto Recorder) )  )  ) )')
                            i = 0
                        i += 1

                        with open(fresh_file, 'wb') as record_file:

                            while not GBase.exit_app:  # inner loop get the stream and write into file

                                chunk = request.read(stream_request_size)  # wasting no space in cluster size
                                record_file.write(chunk)
                                # this_chunk_len = int(len(chunk))
                                # result = result + this_chunk_len

                                if time() - old_time > 60:
                                    old_time = time()
                                    # print(f' {radio_short_key} mb/min: {round((result / 1024) / 1024, 2)} mb')
                                    # result = 0
                                if not chunk:
                                    record_file.flush()
                                    break

                                stream_song_name_new = GRecorder.path_to_song_dict[radio_short_key]  # look what's new

                                if not stream_song_name_new == '':  # some weired stations send this string
                                    stream_song_name = stream_song_name_new
                                if not fresh_song == stream_song_name:  # only here break, jump to outer loop
                                    record_file.flush()
                                    break

                            if GBase.exit_app:
                                print(f' exit record {radio_short_key}')
                                break
        return

    @staticmethod
    def get_metadata_from_stream(url):

        try:
            request = GNet.http_pool.request('GET', url, headers={'Icy-MetaData': '1'}, preload_content=False)

            icy_metadata = request.headers['icy-metaint']
            icy_metadata = int(icy_metadata)
        except KeyError as ke:
            print(ke)
            print('Connection failed miserable in get_metadata_from_stream reader: ' + url)
            GIni.fail_meta_dict[url] = 'True'
        else:
            request.read(icy_metadata)
            chunk_1b = request.read(1)
            chunk_1b = ord(chunk_1b)
            # \x03 hex value, was div. by 4; hex C (12d) * hex 4 = 30 48d; hex 3 (3d) * 16d = 48d;
            read_bytes = chunk_1b * 16
            read_bytes = int(read_bytes)
            metadata_content = request.read(read_bytes)
            metadata_content = metadata_content.decode('utf-8')
            title_info = metadata_content.split(";")
            title_info = title_info[0].split("=")
            title_info = GBase.remove_special_chars(title_info[1])
            request.release_conn()
            return title_info


def step1_collect_stream_server():
    # collect the keys from settings.ini, test if server is alive
    # produce a dictionary with key: short name, value: url
    try:
        if os.environ["SNAP"]:
            print('GR in Ubuntu Snap Container')
            switch_dst_dir('SNAP')
    except KeyError:
        pass
    try:
        if os.environ["DOCKER"]:
            print('GR in Docker Container')  # set var in Dockerfile DOCKER=True
            switch_dst_dir('DOCKER')
    except KeyError:
        pass


    GIni.show_items_ini_file()  # print to terminal
    valid_input = False
    while True:  # collect a list of radio keys to work on
        ini_file_input = input('Copy/Paste a Radio >> settings.ini <<, Enter to record -->:')
        if ini_file_input == 42:
            valid_input = True
            # read all keys from ini file

        if ini_file_input == '':  # exit, or valid_input go next
            break
        else:
            valid_input = True
            print(f' Hit Enter <---| to RECORD, or paste next radio, paste 42 for ALL radios ')
            str_key = ini_file_input.strip()

            if str_key:
                str_val = GIni.find_ini_file(GBase.remove_special_chars(str_key))

                if str_key == '42':
                    # if 42, return gives a list instead of a value
                    str_list = GIni.find_all_in_stations()
                    for ini_key in str_list:
                        ini_row_value = str_list[ini_key]
                        add_server_to_data_base(ini_key, ini_row_value)
                else:
                    add_server_to_data_base(str_key, str_val)  # work with one value

    if valid_input:
        step2_test_stream_server(GIni.ini_keys)


def add_server_to_data_base(str_key, str_val):
    GIni.ini_keys[str_key] = str_val  # append url to dictionary as value
    GBase.make_directory(GBase.radio_base_dir)
    GBase.make_directory(GBase.radio_base_dir + '//' + str_key)

    is_playlist_server = GNet.playlist_server(GIni.ini_keys[str_key])

    if is_playlist_server:  # update dictionary with new url
        GIni.ini_keys[str_key] = is_playlist_server  # append dictionary, test if it is alive
        if not GNet.is_server_meta_stream(GIni.ini_keys[str_key]):
            print('   --> playlist_server server failed, no recording')
            del GIni.ini_keys[str_key]
    if not GNet.is_server_meta_stream(GIni.ini_keys[str_key]):  # first time internet access, response code
        # delete key from dict, return
        del GIni.ini_keys[str_key]


def step2_test_stream_server(ini_keys):
    # further update dictionary
    # calc_connection_cost()
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(test_stream_server, key) for key in ini_keys}

        for fut in as_completed(futures):
            pass
            # print(f"The outcome is {fut.result()} {fut.__dict__}")

    record(ini_keys, GIni.srv_param_dict)  # this starts record threads and loops at end for shutdown signal


def init_dicts_srv_type(key):

    GNet.is_shout_dict[key] = False
    GNet.is_ice_dict[key] = False
    GNet.is_ice_json_dict[key] = False
    GNet.is_unk_dict[key] = False
    GNet.is_no_meta_avail_dict[key] = False

def calc_connection_cost():

    for item in GIni.cost_dict:
        print(f' key: {item} Bytes: {GIni.cost_dict[item]}, title search only - cost per/hour: '
              f'{round(((int(GIni.cost_dict[item]) * 30 * 60)/1024) /1024, 2)}mb')


def print_stream_server():

    print(f'GIni.srv_param_dict {GIni.srv_param_dict}')


def record(ini_keys, path_dict_srv_params):
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    for ini_key in ini_keys:

        GIni.song_dict[ini_key] = '_no-name-record_no_split_'  # init the dict for this thread
        GIni.start_stop_recording[ini_key] = 'start'
        # GIni.start_stop_recording[ini_key] = 'stop'            # init it here, should be set via user interface
        GIni.start_stop_recording[ini_key + '_adv'] = 'start_from_here'  # MUST be set or a key error in record def:

        url = GIni.ini_keys[ini_key]
        GRecorder.path_to_song_dict = GIni.song_dict
        # print(f' <<<<<<<<<<<<<<< GRecorder.path_to_song_dict: {GRecorder.path_to_song_dict}')

        GBase.pool.submit(GRecorder.thread_pull_song_name, url, ini_key, path_dict_srv_params, None)

        dir_save = GBase.radio_base_dir + '//' + ini_key
        stream_suffix = path_dict_srv_params[ini_key + '_file']
        # print(
        #     f' url,{url} dir_save:{dir_save} stream_suffix: {stream_suffix} ini_key: {ini_key} '
        #     f'to_song_dict:{GRecorder.path_to_song_dict}')
        GBase.pool.submit(GRecorder.record_songs, url, dir_save, stream_suffix, ini_key, None)

    while not GBase.exit_app:
        sleep(1)

def test_stream_server(key):
    # srv_param_dict is a simulation of a db for collecting all bool vars, file types, short urls
    # to fire then the http connects and feed the title pull def with correct connection type: json, http, stream
    ini_keys = GIni.ini_keys  # for not twisting brain at end of def / the dict with the radio names
    # GIni.cost_current_ini = key  # for Byte cost calculation / should switch to dict

    # write next dictionary with connection parameters
    GIni.srv_param_dict[key] = GIni.ini_keys[key]
    # print(f'   GIni.srv_param_dict[key]   {GIni.srv_param_dict[key]}    {path_dict[key]}')

    GIni.srv_param_dict[ini_keys[key]] = GIni.parse_url_simple_url(GIni.srv_param_dict[key])  # http://ip:port

    # str_in is input, modify to get more dictionary keys; file type, is shout is ice ...
    ret = GNet.stream_filetype(GIni.srv_param_dict[key])

    GIni.srv_param_dict[key + '_file'] = ret
    if ret is None or ret == '' or ret == ' ':
        GIni.srv_param_dict[key + '_file'] = '.mp3'

    # init the dicts with False
    init_dicts_srv_type(key)
    # server type, either read the title from http, json file or from http stream
    # each server type property has a dict, { radio name : False/True}, with a small db it would be much cleaner
    # GNet.is_shout_ice_unknown_server(server_port, full_url, key)
    GNet.is_shout_ice_unknown_server(GIni.srv_param_dict[ini_keys[key]], GIni.srv_param_dict[key], key)

    if GNet.is_shout_dict[key]:
        GIni.srv_param_dict[key + '_is_shoutcast_server'] = 'True'
    else:
        GIni.srv_param_dict[key + '_is_shoutcast_server'] = 'False'
    if GNet.is_ice_dict[key]:
        GIni.srv_param_dict[key + '_is_icecast_server'] = 'True'
    else:
        GIni.srv_param_dict[key + '_is_icecast_server'] = 'False'
    if GNet.is_ice_json_dict[key]:
        GIni.srv_param_dict[key + '_is_icecast_json'] = 'True'
    else:
        GIni.srv_param_dict[key + '_is_icecast_json'] = 'False'
    if GNet.is_unk_dict[key]:
        GIni.srv_param_dict[key + '_is_unknown_server'] = 'True'
    else:
        GIni.srv_param_dict[key + '_is_unknown_server'] = 'False'
    if GNet.is_no_meta_avail_dict[key]:
        GIni.srv_param_dict[key + '_is_no_meta_data_avail'] = 'True'
    else:
        GIni.srv_param_dict[key + '_is_no_meta_data_avail'] = 'False'


def main():
    step1_collect_stream_server()


if __name__ == '__main__':
    main()
