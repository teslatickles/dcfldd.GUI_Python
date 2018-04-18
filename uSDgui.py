#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog, Menu, messagebox
import os
from plistlib import loads as loading
import subprocess
from subprocess import *
import time
import threading
from PIL import ImageTk, Image
from tkinter.ttk import Progressbar
# import progressor
# import tkinter.ttk as ttk


class HButtons:

    # code block that initializes HButtons class()
    def __init__(self, master):

        global disk
        global disks

        disks = {False: [], True: []}
        for disk in loading(dev_detect('diskutil list -plist'))['WholeDisks']:
            disks[loading(dev_detect('diskutil info -plist ' + disk))['Internal']].append(disk)

        # second thread defined -- for dcfldd background operation
        thread_flash = threading.Thread(target=self.flash)
        thread_flash.daemon = True

        # main button frame -- frame packed with uSD check_Buttons, FLASH and FILE select buttons
        frame = Frame(master, bg="whitesmoke")
        frame.pack(pady=5, expand=1)

        progress_var = DoubleVar()
        self.MAX = 150

        self.progress = Progressbar(frame, orient=HORIZONTAL, length=115, mode="determinate", variable=progress_var)
        self.progress.start()

        # most buttons are coded here
        # image button and flash button code
        self.imgButton = Button(frame, text="File to duplicate", font="Tahoma", command=self.filebox,
                                highlightbackground="whitesmoke").pack(side=TOP, padx=20, pady=17)
        self.flashButton = Button(frame, text="Flash", font="Tahoma", command=thread_flash.start,
                                  highlightbackground="whitesmoke", fg="brown").pack(side=BOTTOM, padx=20, pady=7)

        # checkbutton code block

        self.u1 = Checkbutton(frame, text="uSD1", font="Tahoma", var=chk_state, command=self.usdsel1,
                              background="coral")
        self.u2 = Checkbutton(frame, text="uSD2", font="Tahoma", var=chk_state2, command=self.usdsel2,
                              bg="coral")
        self.u3 = Checkbutton(frame, text="uSD3", font="Tahoma", var=chk_state3, command=self.usdsel3,
                              bg="coral")
        self.u4 = Checkbutton(frame, text="uSD4", font="Tahoma", var=chk_state4, command=self.usdsel4,
                              bg="coral")

        # [self.u1.configure(state='active') if disk == "disk2" else self.u1.config(state='disabled')
        # for disks in disks]

        self.u1.pack(padx=35, pady=2, fill="x")
        self.u2.pack(padx=35, pady=2, fill="x")
        self.u3.pack(padx=35, pady=2, fill="x")
        self.u4.pack(padx=35, pady=2, fill="x")

        self.u1.invoke()
        self.u1.invoke()

        self.u2.invoke()
        self.u2.invoke()

        self.u3.invoke()
        self.u3.invoke()

        self.u4.invoke()
        self.u4.invoke()

        # [card_ind2.pack() if disk == "disk3" else card_ind2.pack_forget() for disks in disks]

        # [card_ind3.pack() if disk == "disk4" else card_ind3.pack_forget() for disks in disks]

        # [card_ind4.pack() if disk == "disk5" else card_ind4.pack_forget() for disks in disks]

    def invoke(self):
        self.u1.invoke()
        self.u1.invoke()

        self.u2.invoke()
        self.u2.invoke()

        self.u3.invoke()
        self.u3.invoke()

        self.u4.invoke()
        self.u4.invoke()

    def progress_f(self):
        k = 0
        while k <= self.MAX:
            self.progress_var.set(k)
            k += 1
            time.sleep(0.02)
            root.update()
        root.after(100, self.progress_f)

    def flash(self):

        self.progress.pack_configure(side=BOTTOM, expand=0, pady=10, padx=10)

        stoprequest.set()

        selection = str(root.filename)
        img = selection[:-28][+25:]

        dev_1 = '2'
        dev_2 = '3'
        dev_3 = '4'
        dev_4 = '5'

        bish = "#!/bin/bash\n\n"

        y = "sudo dcfldd sizeprobe=if "
        x = "if={} ".format(img)

        a = "of=/dev/rdisk{} ".format(dev_1)
        b = "of=/dev/rdisk{} ".format(dev_2)
        g = "of=/dev/rdisk{} ".format(dev_3)
        h = "of=/dev/rdisk{} ".format(dev_4)

        za = "diskutil unmountDisk /dev/disk{}\n".format(dev_1)
        zb = "diskutil unmountDisk /dev/disk{}\n".format(dev_2)
        zg = "diskutil unmountDisk /dev/disk{}\n".format(dev_3)
        zh = "diskutil unmountDisk /dev/disk{}\n".format(dev_4)

        spc = "\n"
        spc2 = "\n\n"

        global bash_cmd

        if chk_state.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}".format(bish, za, spc, y, x, a, spc2, za))
        if chk_state2.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}".format(bish, zb, spc, y, x, b, spc2, zb))
        if chk_state3.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}".format(bish, zg, spc, y, x, g, spc2, zg))
        if chk_state4.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}".format(bish, zh, spc, y, x, h, spc2, zh))
        if chk_state.get() & chk_state2.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}".format(bish, za, zb, spc, y, x, a, b, spc2, za, zb))
        if chk_state.get() & chk_state3.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}".format(bish, za, zg, spc, y, x, a, g, spc2, za, zg))
        if chk_state.get() & chk_state4.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}".format(bish, za, zh, spc, y, x, a, h, spc2, za, zh))
        if chk_state2.get() & chk_state3.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}".format(bish, zb, zg, spc, y, x, b, g, spc2, zb, zg))
        if chk_state2.get() & chk_state4.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}".format(bish, zb, zh, spc, y, x, b, h, spc2, zb, zh))
        if chk_state3.get() & chk_state4.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}".format(bish, zg, zh, spc,  y, x, g, h, spc2, zg, zh))
        if chk_state.get() & chk_state2.get() & chk_state3.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(bish, za, zb, zg, spc, y, x, a, b, g, spc2, za, zb, zg))
        if chk_state.get() & chk_state2.get() & chk_state4.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(bish, za, zb, zh, spc, y, x, a, b, h, spc2, za, zb, zh))
        if chk_state.get() & chk_state3.get() & chk_state4.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(bish, za, zg, zh, spc, y, x, a, g, h, spc2, za, zg, zh))
        if chk_state2.get() & chk_state3.get() & chk_state4.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(bish, zb, zg, zh, spc, y, x, b, g, h, spc2, zb, zg, zh))
        if chk_state.get() & chk_state2.get() & chk_state3.get() & chk_state4.get() == TRUE:
            bash_cmd = ("{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(bish, za, zb, zg, zh, spc, y, x, a, b, g, h, spc2,
                                                                    za, zb, zg, zh))
        combo_fmt = ''.join(map(str, bash_cmd))

        dd_exe_f = open("/Users/hunterhartline/PycharmProjects/uSDgui/execute.sh", "w")

        for i in range(1):
            dd_exe_f.write(combo_fmt)
        dd_exe_f.close()

        print("")
        print(".")
        time.sleep(.5)

        print("..")
        time.sleep(.5)

        print("...")
        time.sleep(.5)

        print(" ^^^^^^^^^^^^^^^^^^^^ ")
        print(" ^!flashing card(s)!^ ")
        print(" ^^^^^^^^^^^^^^^^^^^^ ")

        # self.subprocess_flash() function was demoted to nest in flash() -- this function you're perusing now
        dd = subprocess.Popen(['/Users/hunterhartline/PycharmProjects/uSDgui/execute.sh'], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        output = dd.communicate()[0].decode('utf-8')

        # output printed for debugging
        print(output)

        if chk_state8.get() == TRUE:
            print("...")
            print("..")
            print(".")
            print("program will auto-close in: 3 sec --->change in preferences<---")
            time.sleep(3)
            root.destroy()
        elif chk_state8.get() == FALSE:
            print("Done flashing cards!")

    def usdsel1(self):
        if chk_state.get() == TRUE:
            st1 = "uSD1"

        elif chk_state.get() == FALSE:
            st1 = "---"
        us1.config(text=str(st1))

    def usdsel2(self):

        if chk_state2.get() == TRUE:
            st2 = "uSD2"

        elif chk_state2.get() == FALSE:
            st2 = "---"
        us2.config(text=str(st2))

    def usdsel3(self):
        if chk_state3.get() == TRUE:
            st3 = "uSD3"

        elif chk_state3.get() == FALSE:
            st3 = "---"
        us3.config(text=str(st3))

    def usdsel4(self):
        if chk_state4.get() == TRUE:
            st4 = "uSD4"

        elif chk_state4.get() == FALSE:
            st4 = "---"
        us4.config(text=str(st4))

    def filebox(self):
        cs = vp.get()
        dp = "/"
        self.ch = ""

        if chk_state6.get() == TRUE:
            self.ch = cs
        elif chk_state6.get() == FALSE:
            self.ch = dp

        root.filename = filedialog.askopenfile(initialdir=self.ch,
                                               title="Select image to duplicate",
                                               filetypes=(("image files", "*.img"), ("all files", "*.*")))
        selection = str(root.filename)

        if selection == "None":
            selfile.config(text="-----")

            chk_state.set(False)
            chk_state2.set(False)
            chk_state3.set(False)
            chk_state4.set(False)
            self.invoke()

        elif selection != "None" and chk_state5.get() == TRUE:
            selfile.config(text=os.path.basename(os.path.normpath(selection))[:-28])

            chk_state.set(True)
            chk_state2.set(True)
            chk_state3.set(True)
            chk_state4.set(True)
            self.invoke()

        elif selection != "None" and chk_state5.get() == FALSE:
            selfile.config(text=os.path.basename(os.path.normpath(selection))[:-28])

            chk_state.set(False)
            chk_state2.set(False)
            chk_state3.set(False)
            chk_state4.set(False)
            self.invoke()


def pathselect():
    cs = vp.get()
    dp = "/"
    if chk_state6.get() == TRUE:
        popup_path()
        ch = cs
    elif chk_state6.get() == FALSE:
        ch = dp


def optbox():
    prefwin = Toplevel()
    prefwin.title("Preferences")
    prefwin.geometry("440x325")
    prefwin.configure(bg="darkseagreen1")

    msg = Message(prefwin, text="* PROGRAM PREFERENCES", bg="darkseagreen1", pady="50")
    msg.pack()

    autochk = Checkbutton(prefwin, text="Automatically select all microSD drives after selecting source file",
                          padx="10", background="darkseagreen1", fg="black", font="Bold", var=chk_state5)
    autochk.pack(anchor="w")

    autoclose = Checkbutton(prefwin, text="Automatically close program after successfully flashing cards", padx="10",
                            bg="darkseagreen1", fg="black", var=chk_state8, command="NOTHING")
    autoclose.pack(anchor="w")

    screenboot = Checkbutton(prefwin, text="Maximize program window upon opening",
                             padx="10", bg="darkseagreen1", fg="black", var=chk_state9, command="NOTHING")
    screenboot.pack(anchor="w")

    defpath = Checkbutton(prefwin, text="Specify an alternative default path", padx="10", bg="darkseagreen1",
                          fg="black", var=chk_state6, command=pathselect)
    defpath.pack(anchor="w")

    closewarning = Checkbutton(prefwin, text="Select to receive warning before closing program", padx="10",
                               bg="darkseagreen1", fg="black", var=chk_state7)
    closewarning.pack(anchor="w")

    darkmode = Checkbutton(prefwin, text="Select to switch color scheme to dark version", padx="10", bg="darkseagreen1",
                           fg="black", var=chk_state10, command="Nothing")
    darkmode.pack(anchor="w")


def popup_path():
    poppath = Toplevel()
    poppath.title("Alternate Path")
    poppath.geometry("598x185")
    poppath.configure(bg="rosybrown")

    fl = Message(poppath, text="Path:", bg="rosybrown", pady="15")
    fl.pack(side=TOP)

    e1 = Entry(poppath, width=300, textvariable=vp)
    e1.pack(padx="15")
    e1.focus_set()

    browse_butt = Button(poppath, text="Browse", highlightbackground="rosybrown", padx="10", pady="3", command=browsing)
    browse_butt.pack(side=TOP, padx="35", pady="12")

    ok_button = Button(poppath, text=" Okay ", highlightbackground="rosybrown", pady="3", command=poppath.destroy)
    ok_button.pack()

    canc_button = Button(poppath, text="Cancel", highlightbackground="rosybrown", pady="3",
                         command=popup_cancel)
    canc_button.pack()


def browsing():
    root.filename2 = filedialog.askdirectory(initialdir="/",
                                             title="Select desired path")
    bp = str(root.filename2)
    print(bp)
    vp.set(bp)


def popup_cancel():
    chk_state6.set(False)
    vp.set("/")
    if chk_state6.get() == FALSE:
        poppath.destroy()


def on_closing():
    if chk_state7.get() or stoprequest.is_set():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    elif chk_state7.get() == FALSE:
        root.destroy()


def max_screen_boot():
    if chk_state9.get() == TRUE:
        root.attributes('-fullscreen', True)


def dev_detect(cmd):
    return Popen(cmd.split(), stdout=PIPE).communicate()[0]


def dev_ion():
    global disk
    global disks

    disks = {False: [], True: []}
    for disk in loading(dev_detect('diskutil list -plist'))['WholeDisks']:
        disks[loading(dev_detect('diskutil info -plist ' + disk))['Internal']].append(disk)

    print("Internal disks: " + ' '.join(disks[True]))
    print("External disks: " + ' '.join(disks[False]))
    time.sleep(0.1)

    [card_ind1.pack() if disk == "disk2" else card_ind1.pack_forget() for disks in disks]

    [card_ind2.pack() if disk == "disk3" else card_ind2.pack_forget() for disks in disks]

    [card_ind3.pack() if disk == "disk4" else card_ind3.pack_forget() for disks in disks]

    [card_ind4.pack() if disk == "disk5" else card_ind4.pack_forget() for disks in disks]


def dev_status():

    global stoprequest

    stoprequest = threading.Event()

    while not stoprequest.isSet():
        try:
            dev_ion()
            print("******!USB/SD DEVICE DETECTION IS CURRENTLY RUNNING IN BACKGROUND!******")
            time.sleep(0.8)
        except EOFError:
            continue


if __name__ == "__main__":

    # threading is setup for concurrent processing of removable storage devices
    thread_dev_det = threading.Thread(target=dev_status)
    thread_dev_det.daemon = True
    thread_dev_det.start()

    # necessary root declaration to start main code block
    root = Tk()

    # calls on_closing function upon attempting to close main window
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # quick invoke of alt path window for variables
    poppath = Toplevel()
    poppath.withdraw()

    vp = StringVar()

    img_path = Image.open('/Users/hunterhartline/PycharmProjects/uSDgui/kard.png').convert("RGB")
    icon3 = ImageTk.PhotoImage(img_path)

    card_ind1 = Label(root, image=icon3, highlightbackground="DarkSeaGreen1", highlightthickness="0", borderwidth="0",
                      bg="DarkSeaGreen1")
    card_ind2 = Label(root, image=icon3, highlightthickness="0", borderwidth="0")
    card_ind3 = Label(root, image=icon3, highlightthickness="0", borderwidth="0")
    card_ind4 = Label(root, image=icon3, highlightthickness="0", borderwidth="0")

    us4 = Label(root, bg="DarkOliveGreen4", fg="deepskyblue4")
    us4.pack(side=BOTTOM)

    us3 = Label(root, bg="DarkOliveGreen4", fg="deepskyblue4")
    us3.pack(side=BOTTOM)

    us2 = Label(root, bg="DarkOliveGreen4", fg="deepskyblue4")
    us2.pack(side=BOTTOM)

    us1 = Label(root, bg="DarkOliveGreen4", fg="deepskyblue4")
    us1.pack(side=BOTTOM)

    dupltxt = Label(root, text="will flash to  >>>", bg="DarkOliveGreen4", fg="whitesmoke")
    dupltxt.pack(side=BOTTOM)

    selfile = Label(root, bg="DarkOliveGreen4", fg="coral")
    selfile.pack(side=BOTTOM)

    filetxt = Label(root, text="File:", bg="DarkOliveGreen4", fg="whitesmoke")
    filetxt.pack(side=BOTTOM)

# code block corresponding to all button variable boolean declarations
    chk_state = BooleanVar()
    chk_state2 = BooleanVar()
    chk_state3 = BooleanVar()
    chk_state4 = BooleanVar()
    chk_state5 = BooleanVar()
    chk_state6 = BooleanVar()
    chk_state7 = BooleanVar()
    chk_state8 = BooleanVar()
    chk_state9 = BooleanVar()
    chk_state10 = BooleanVar()

# sub-menu call for preference options at top
    menu = Menu(root)
    root.config(menu=menu)
    subMenu = Menu(menu)
    menu.add_cascade(label='Main', menu=subMenu)
    subMenu.add_command(label="Preferences", command=optbox)
    subMenu.add_separator()
    subMenu.add_command(label="Exit", command=exit)

# main GUI window configuration
    root.title("teslatickle's uSD Duplicator")
    root.configure(background="DarkOliveGreen4")
    root.geometry("255x455")

# class HButtons declared in main body
    c = HButtons(root)

# codes 'esc' to exit GUI/application
    root.bind('<Escape>', lambda e: root.destroy())

# must be present for tkinter/GUI to work
    root.mainloop()
