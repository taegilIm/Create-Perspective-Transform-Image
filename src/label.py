import tkinter as tk

import image_process

win_size = ()

pos: list[list[float]] = [[0, 0], [0, 0], [0, 0], [0, 0]]
index = 0

points_id: list[int] = []

image_id: int = 0

# output size
image_size = ["640x480", "800x600", "1024x768", "1280x720", "1366x768", "1920x1080"]


def Initailizing(root: tk.Tk, size: tuple[int, int]):
    global win_size, win_root, canvas, file_button, save_file_button, execute_button, position

    win_root = root
    win_size = size

    canvas = tk.Canvas(root, width=1366, height=766)
    canvas.pack(fill="both", expand=True)

    # image section
    canvas.create_rectangle(
        10, 10, win_size[0] * 2 / 3, win_size[1] * 5 / 6, width=2, fill=""
    )

    # buttons define
    file_button = tk.Button(root, text="open image file", command=onOpenFile)
    save_file_button = tk.Button(root, text="save image file", command=onSaveFile)
    execute_button = tk.Button(root, text="execute", command=onExecuteButtonClick)

    # position section
    canvas.create_rectangle(
        win_size[0] * 2 / 3 + 20,
        10,
        win_size[0] - 10,
        win_size[1] / 2,
        width=2,
        fill="",
    )
    position = tk.Label(
        root,
        text="x1: 0, y1: 0\nx2: 0, y2: 0\nx3: 0, y3: 0\nx4: 0, y4: 0",
        font=("Arial", 20),
        justify="left",
    )


def placeLabels(root: tk.Tk):
    # place labels
    file_button.place(x=10, y=win_size[1] * 5 / 6 + 30)
    save_file_button.place(x=10, y=win_size[1] * 5 / 6 + 30)
    execute_button.place(x=10, y=win_size[1] * 5 / 6 + 30)
    position.place(x=win_size[0] * 2 / 3 + 30, y=20)

    # adjust position
    root.update_idletasks()

    btn_size1 = file_button.winfo_width()
    btn_size2 = save_file_button.winfo_width() + btn_size1

    save_file_button.place(x=30 + btn_size1, y=win_size[1] * 5 / 6 + 30)
    execute_button.place(x=50 + btn_size2, y=win_size[1] * 5 / 6 + 30)


# event process funtions
def onLMBClick(event: tk.Event):
    global index

    # dots color
    color = ["red", "orange", "yellow", "pink"]

    # clicked position
    pos[index] = [event.x, event.y]
    position.config(
        text=f"x1: {pos[0][0]}, y1: {pos[0][1]}\nx2: {pos[1][0]}, y2: {pos[1][1]}\nx3: {pos[2][0]}, y3: {pos[2][1]}\nx4: {pos[3][0]}, y4: {pos[3][1]}"
    )

    # make dots
    circle_id = canvas.create_oval(
        event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill=color[index]
    )
    points_id.append(circle_id)

    if len(points_id) > 4:
        del_points = points_id.pop(0)
        canvas.delete(del_points)

    index = (index + 1) % 4


def onOpenFile():
    global tk_image, image_id

    if image_id != 0:
        canvas.delete(image_id)

    # get file path
    file_path = image_process.selectFile()
    if file_path is None:
        return

    # get image
    image_size, tk_image = image_process.openImageFile(file_path, win_size)
    if image_size is None:
        return

    # image create
    image_id = canvas.create_image(10, 10, anchor="nw", image=tk_image)
    canvas.tag_bind(image_id, "<Button-1>", onLMBClick)


def onExecuteButtonClick():
    global new_window, listbox, image_size

    if len(points_id) < 4:
        return

    # create new window
    new_window = tk.Toplevel(win_root)
    new_window.title("set size")
    new_window.geometry("400x300")

    listbox = tk.Listbox(new_window)
    for i in image_size:
        listbox.insert(tk.END, i)

    listbox.bind("<<ListboxSelect>>", onExcute)

    listbox.place(x=10, y=10)


def onExcute(event):
    global transf_image, image_result, image_id

    index = listbox.curselection()

    if index:
        # get transformed image
        transf_image = image_process.imageTransfer(pos, listbox.get(index))
        image_result = image_process.cvToTk(transf_image)

        canvas.delete(image_id)
        image_id = canvas.create_image(10, 10, anchor="nw", image=image_result)

        # delete points
        for i in points_id:
            canvas.delete(i)
            points_id.remove(i)

        position.config(text="x1: 0, y1: 0\nx2: 0, y2: 0\nx3: 0, y3: 0\nx4: 0, y4: 0")

    new_window.destroy()


def onSaveFile():
    try:
        image_process.saveImageFile(image_result)
    except NameError:
        return
