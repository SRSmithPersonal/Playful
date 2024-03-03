#!/usr/bin/env python3
import gi
import os
import subprocess
import threading
from mimetypes import MimeTypes
mime = MimeTypes()
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

keeper = []
ToStop = False
pro = []
Fullscreen = False
FileCount = 0
listbox = Gtk.ListBox()
StartPos = 0
Started = False


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))


def player():
    global keeper
    global ToStop
    global pro
    ToStop = False
    for x in range(StartPos, len(keeper)):
        if Fullscreen is True:
            pro = subprocess.Popen("mpv --fs " + "\"" + keeper[x] + "\"", shell=True)
        else:
            pro = subprocess.Popen("mpv " + "\"" + keeper[x] + "\"", shell=True)
        pro.wait()
        if ToStop is True:
            break


def stop():
    global ToStop
    ToStop = True
    global pro
    pro.terminate()
    pro.wait()


def clickclack(position):
    global StartPos
    global Started
    if StartPos == (position-1):
        if Started is True:
            stop()
        Started = True
        thread = threading.Thread(target=player)
        thread.daemon = True
        thread.start()
    else:
        StartPos = position-1


class FileChooserWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Playlist")

        grid = Gtk.Grid()
        self.add(grid)

        button1 = Gtk.Button(label="Choose File")
        button1.connect("clicked", self.on_file_clicked)
        grid.add(button1)

        button2 = Gtk.Button(label="Choose Video Folder")
        button2.connect("clicked", self.on_folder_clicked1)
        grid.attach_next_to(button2, button1, Gtk.PositionType.RIGHT, 1, 1)

        button3 = Gtk.Button(label="Choose Audio Folder")
        button3.connect("clicked", self.on_folder_clicked2)
        grid.attach_next_to(button3, button2, Gtk.PositionType.RIGHT, 1, 1)

        button4 = Gtk.Button(label="Play")
        button4.connect("clicked", self.on_play_clicked)
        grid.attach_next_to(button4, button1, Gtk.PositionType.BOTTOM, 1, 1)

        button5 = Gtk.Button(label="Stop")
        button5.connect("clicked", self.on_stop_clicked)
        grid.attach_next_to(button5, button3, Gtk.PositionType.BOTTOM, 1, 1)

        button6 = Gtk.Button(label="clear")
        button6.connect("clicked", self.on_clear_clicked)
        grid.attach_next_to(button6, button2, Gtk.PositionType.BOTTOM, 1, 1)

        button = Gtk.ToggleButton(label="Fullscreen")
        button.set_active(False)
        button.connect("toggled", self.fullscreen_button_toggled, "2")
        grid.attach_next_to(button, button6, Gtk.PositionType.BOTTOM, 1, 1)

        buttonE = Gtk.Button(label=" ")
        buttonE.connect("clicked", self.clicky)
        grid.attach_next_to(buttonE, button4, Gtk.PositionType.BOTTOM, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        # grid.attach_next_to(listbox, buttonE, Gtk.PositionType.BOTTOM, 3, 3)
        grid.attach_next_to(scrolledwindow, buttonE, Gtk.PositionType.BOTTOM, 3, 200)
        scrolledwindow.set_size_request(3, 200)
        scrolledwindow.add(listbox)
        listbox.connect('row-activated', lambda widget, row: clickclack(row.data[0]))
        listbox.show_all()

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_select_multiple(True)

        self.add_filters(dialog)
        global FileCount
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            for x in range(0, len(dialog.get_filenames())):
                FileCount += 1
                keeper.append(dialog.get_filenames()[x])
                listbox.add(ListBoxRowWithData((FileCount, dialog.get_filenames()[x].split('/')[-1])))
        listbox.show_all()
        dialog.destroy()

    def clicky(self, widget):
        print("click\n")

    def add_filters(self, dialog):
        filter_py = Gtk.FileFilter()
        filter_py.set_name("Video")
        filter_py.add_mime_type("video/*")
        dialog.add_filter(filter_py)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Audio")
        filter_py.add_mime_type("audio/*")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_folder_clicked1(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        global FileCount
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            temp = os.listdir(dialog.get_filename())
            for x in range(0, len(temp)):
                if mime.guess_type(temp[x])[0] is not None:
                    if mime.guess_type(temp[x])[0].split('/')[0] == 'video':
                        FileCount += 1
                        keeper.append(dialog.get_filename()+"/"+temp[x])
                        listbox.add(ListBoxRowWithData((FileCount, temp[x])))
        listbox.show_all()
        dialog.destroy()

    def on_folder_clicked2(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        global FileCount
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            temp = os.listdir(dialog.get_filename())
            for x in range(0, len(temp)):
                if mime.guess_type(temp[x])[0] is not None:
                    if mime.guess_type(temp[x])[0].split('/')[0] == 'audio':
                        FileCount += 1
                        keeper.append(dialog.get_filename()+"/"+temp[x])
                        listbox.add(ListBoxRowWithData((FileCount, temp[x])))
        listbox.show_all()
        dialog.destroy()

    def on_play_clicked(self, widget):
        global Started
        Started = True
        thread = threading.Thread(target=player)
        thread.daemon = True
        thread.start()

    def on_stop_clicked(self, widget):
        stop()

    def on_clear_clicked(self, widget):
        global keeper
        keeper = []

    def fullscreen_button_toggled(self, button, name):
        global Fullscreen
        if button.get_active():
            Fullscreen = True
        else:
            Fullscreen = False


win = FileChooserWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
