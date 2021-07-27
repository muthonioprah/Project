import os
from PIL import Image
import time

UPLOAD_FOLDER = os.getcwd() + '/static/images/uploads'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_upload(fileObj):

    file = fileObj

    if file.filename == "":
        return None

    if file and allowed_file(file.filename):
        img = Image.open(file)
        new_width = 250
        new_height = 250
        size = (new_width, new_height)
        img.thumbnail(size)

        # create a timestamp
        stamped = time.time()

        fname = str(stamped) + file.filename

        # save the image
        img.save(os.path.join(UPLOAD_FOLDER,fname+".png"), format="PNG")

        # print("the image",img.format)
        return '/static/images/uploads/'+ str(stamped) + file.filename + ".png"
        

    else:
        return None

        # 0717804443