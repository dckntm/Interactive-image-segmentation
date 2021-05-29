from PIL import Image


def compare(reference: Image.Image, ouput: Image.Image) -> None:
    h1, w2, img1 = reference.height, reference.width, reference.load()
    h2, w2, img2 = ouput.height, ouput.width, ouput.load()

    if (h1 != h2 or w2 != w2):
        raise Exception('Cannot compare following images')

    obj_correct_pixels = 0
    bck_correct_pixels = 0
    obj_union_count = 0

    for i in range(w2):
        for j in range(h1):
            pixel1 = img1[i, j]
            pixel2 = img2[i, j]

            if (isinstance(pixel1, int) == True):
                intensity1 = pixel1
            else:
                intensity1 = pixel1[0] + pixel1[1] + pixel1[2]
            if (isinstance(pixel2, int) == True):
                intensity2 = pixel2
            else:
                intensity2 = pixel2[0] + pixel2[1] + pixel2[2]

            if (intensity1 > 0 and intensity2 > 0):
                obj_correct_pixels += 1
            if (intensity1 > 0 or intensity2 > 0):
                obj_union_count += 1
            if (intensity1 == 0 and intensity2 == 0):
                bck_correct_pixels += 1

    return \
        obj_correct_pixels / (w2 * h1), \
        bck_correct_pixels / (w2 * h1), \
        (obj_correct_pixels + bck_correct_pixels) / (w2 * h1), \
        obj_correct_pixels / obj_union_count
