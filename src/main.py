from tkinter import Tk

import label

# make window
root = Tk()
root.title("Image Converter")
root.state("zoomed")

root.update_idletasks()

win_size = (root.winfo_width(), root.winfo_height())

# create tk label
label.Initailizing(root, win_size)
label.placeLabels(root)

root.mainloop()
