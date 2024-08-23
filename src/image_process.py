from tkinter import filedialog, messagebox
import cv2 as cv
from PIL import Image, ImageTk
import numpy as np


def selectFile() -> str | None:
    # read path
    path = filedialog.askopenfilename(
        title="file open",
        filetypes=(("all files (image)", "*.*"), ("image file", "*.png")),
    )

    if path:
        return path
    else:
        messagebox.showinfo("file open", "failed to open file")
        return


def openImageFile(
    file_path: str, win_size: tuple[int, int]
) -> tuple[tuple[int, int], ImageTk.PhotoImage] | tuple[None, None]:
    global cv_image

    # read image to cv
    cv_image = cv.imread(file_path)
    if cv_image is None:
        return (None, None)

    # size check
    image_size = cv_image.shape[:2]
    if image_size[1] > win_size[0] * 2 / 3 or image_size[0] > win_size[1] * 2 / 3:
        messagebox.showinfo("big image", "image is too big")
        return (None, None)

    # get photoimage from cv
    tk_image = cvToTk(cv_image)

    return (image_size, tk_image)


def cvToTk(image) -> ImageTk.PhotoImage:
    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    tk_image = ImageTk.PhotoImage(pil_image)

    return tk_image


def imageTransfer(pos: list[list[float]], image_size: str):
    # get output size
    size = image_size.split("x")

    # perspective transform process
    point1 = np.float32(pos)
    point2 = np.float32(
        [[0, 0], [int(size[0]), 0], [0, int(size[1])], [int(size[0]), int(size[1])]]
    )

    m = cv.getPerspectiveTransform(point1, point2)
    result = cv.warpPerspective(cv_image, m, (int(size[0]), int(size[1])))

    return result


def saveImageFile(image: ImageTk.PhotoImage) -> None:
    # photoimage to pil image
    pil_image = ImageTk.getimage(image)
    pil_image.save("output/output.png", format="png")
