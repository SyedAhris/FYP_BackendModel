import cv2
import random
import numpy as np
def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    tl = line_thickness or round(0.002 * max(img.shape[0:2])) + 1  # line thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
    return img

def preprocess(img, input_shape, letter_box=True):
    """img:         input image in numpy array
       input_shape: [height, width] of input image, this is the target shape for the model
       letter_box:  control whether to apply letterbox resizing """
    if letter_box:
        img_h, img_w, _ = img.shape                    #img is opened with opencv, in shape(h, w, c), this is the original image shape
        new_h, new_w = input_shape[0], input_shape[1]  # desired input shape for the model
        offset_h, offset_w = 0, 0                      # initialize the offset
        if (new_w / img_w) <= (new_h / img_h):         # if the resizing scale of width is lower than that of height
            new_h = int(img_h * new_w / img_w)         # get a new_h that is with the same resizing scale of width
            offset_h = (input_shape[0] - new_h) // 2   # update the offset_h
        else:
            new_w = int(img_w * new_h / img_h)         # if the resizing scale of width is higher than that of height, update new_w
            offset_w = (input_shape[1] - new_w) // 2   # update the offset_w
        resized = cv2.resize(img, (new_w, new_h))      # get resized image using new_w and new_h
        img = np.full((input_shape[0], input_shape[1], 3), 127, dtype=np.uint8) # initialize a img with pixel value 127, gray color
        img[offset_h:(offset_h + new_h), offset_w:(offset_w + new_w), :] = resized
    else:
        img = cv2.resize(img, (input_shape[1], input_shape[0]))

    return img

def scale_coords(img_shape, coords, img_orig_shape):
    """Rescale coordinates to original image shape"""
    height, width = img_orig_shape[:2]

    # Rescale bounding boxes to original image shape
    ratio = min(img_shape[1] / width, img_shape[0] / height)
    pad_x = (img_shape[1] - width * ratio) / 2
    pad_y = (img_shape[0] - height * ratio) / 2
    coords[:, [0, 2]] -= pad_x
    coords[:, [1, 3]] -= pad_y
    coords[:, :4] /= ratio
    coords[:, :4] = np.clip(coords[:, :4], 0, img_orig_shape[:2])

    # Fix for boxes that go outside of the image boundaries
    coords[:, [0, 2]] = np.clip(coords[:, [0, 2]], 0, img_orig_shape[1])
    coords[:, [1, 3]] = np.clip(coords[:, [1, 3]], 0, img_orig_shape[0])

    return coords
