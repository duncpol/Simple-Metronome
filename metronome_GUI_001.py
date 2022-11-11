import time
from datetime import datetime
import simpleaudio as sa
import threading
from tkinter import *

click_accented = sa.WaveObject.from_wave_file("click_accented_long.wav")
click_normal = sa.WaveObject.from_wave_file("click_normal.wav")


# get beats per minute value
def get_bpm(*args):
    try:
        bpm_value = int(text_bpm.get())
        return bpm_value
    except ValueError:
        print("Invalid bpm entry")
        return 0


def get_tpb(*args):
    # print('ticks per beat arguments: ' + str(args))
    try:
        tpb_value = int(text_tpb.get())
        print('ticks per bar: {}'.format(tpb_value))
        return tpb_value
    except ValueError:
        print("Invalid tpb entry")
        return 0


def more_than_2_threads():
    return len(threading.enumerate()) > 2


def tick(tick_enabled):
    bpm_value = get_bpm()
    print('bpm value: ' + str(bpm_value))
    tpb_value = get_tpb()

    # print('{}, {}'.format(bpm_value, tick_enabled))
    print('accented click enabled: {}'.format(accent_enabled.get()))
    t0 = datetime.now()
    num_of_ticks = 0

    if bpm_value == 0 or tpb_value == 0:
        return
    time_per_beat = 60 / bpm_value  # time in [s]

    while tick_enabled:
        # print(bpm_value)
        if more_than_2_threads():
            break
        if tpb_value == 0:
            break

        if accent_enabled.get():
            start = time.time()
            play_click_accented = click_accented.play()  # plays 0.05s
            play_click_accented.wait_done()
            num_of_ticks += 1
            if more_than_2_threads():
                break
            end = time.time()
            delay = end - start
            # print(delay)
            if delay < time_per_beat:
                time.sleep(time_per_beat - delay)  # click_accented_long.waw is 0.03s longer
        else:
            start = time.time()
            play_click_normal = click_normal.play()  # plays 0.02s
            play_click_normal.wait_done()
            num_of_ticks += 1
            end = time.time()
            delay = end - start
            # print(delay)
            if more_than_2_threads():
                break
            time.sleep(time_per_beat - delay)

        for i in range(tpb_value - 1):
            start = time.time()
            if more_than_2_threads():
                break
            play_click_normal = click_normal.play()  # plays 0.02s
            play_click_normal.wait_done()
            num_of_ticks += 1
            end = time.time()
            delay = end - start
            time.sleep(time_per_beat - delay)

    if tick_enabled:
        t1 = datetime.now()
        t_delta = t1 - t0
        print("\n\n")
        print("Number of ticks: " + str(num_of_ticks))
        print("Time passed: " + str(t_delta))
        print("\n\n")

def tick_threaded(enabled):
    if get_bpm() < 15:
        text_bpm.set(15)
    if get_bpm() > 450:
        text_bpm.set(450)

    num_of_ticks = 0
    thread = threading.Thread(target=tick, args=(enabled,))
    thread.start()
    num_of_ticks += 1
    if more_than_2_threads():
        # print(threading.get_ident())
        threading.enumerate()[1].join()

    # print(thread.getName())
    # print(thread.name)

    print(threading.enumerate())
    # if tick_stopped:
    # threading.Event().set()


def exit_tick_threaded():
    if len(threading.enumerate()) > 1:
        print(threading.get_ident())
        threading.enumerate()[1].join()


window = Tk()
window.title("Metronome")

window.geometry("500x300+1300+100")

# beats per minute label
lab_bpm = Label(window,
                text="BPM value", font=("Arial", 14))
lab_bpm.place(bordermode=INSIDE, relx=0.05, rely=0.05,
              relwidth=0.24, relheight=0.15)

#  ticks per bar label
lab_tpb = Label(window,
                text="Ticks per bar", font=("Arial", 14))
lab_tpb.place(bordermode=OUTSIDE, relx=0.5, rely=0.05,
              relwidth=0.24, relheight=0.15)

# beats per minute entry
text_bpm = StringVar()
ent_set_bpm = Entry(window, textvariable=text_bpm,
                    font=("Arial", 16, "bold"))
ent_set_bpm.insert(0, text_bpm.get())
ent_set_bpm.place(relx=0.05, rely=0.20,
                  relwidth=0.24, relheight=0.15)
default_bpm = "120"
text_bpm.set(default_bpm)
text_bpm.trace('w', get_bpm)

#  ticks per bar entry
text_tpb = StringVar()
ent_set_tpb = Entry(window, textvariable=text_tpb,
                    font=("Arial", 16, "bold"))
ent_set_tpb.place(relx=0.5, rely=0.20,
                  relwidth=0.24, relheight=0.15)
default_tpb = "4"
text_tpb.set(default_tpb)
text_tpb.trace('w', get_tpb)

# accent 1st note CheckButton
accent_enabled = BooleanVar()
chkbut_accent = Checkbutton(window, text="Accent first note", font=("Arial", 14),
                            variable=accent_enabled)
chkbut_accent.place(relx=0.05, rely=0.5, relheight=0.1)
chkbut_accent.select()

# play button
but_play = Button(window, text="PLAY", font=("Arial", 16, "bold"),
                  command=lambda: tick_threaded(True))
but_play.place(relx=0.5, rely=0.8, relwidth=0.24, relheight=0.15)

# stop button
but_stop = Button(window, text="STOP", font=("Arial", 16, "bold"),
                  command=lambda: tick_threaded(False))
but_stop.place(relx=0.75, rely=0.8, relwidth=0.24, relheight=0.15)

window.mainloop()

print("away from mainloop")
