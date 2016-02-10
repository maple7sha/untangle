# Maple7sha

# Get the path to master directory and iterate 
# For each .jpg file, extract the time info, and put them into folders of different months
# (in the future, may put them into different locations)

# What if not enough space? 
# Remove duplications by comparing hashes using dictionary ? 
import sys
import os
import re
import fnmatch
import time
import datetime
import shutil
from os.path import join, getsize
from PIL import Image
from PIL import ExifTags

img_re = re.compile(r'.+\.(jpg|jpeg|mp4|mov)$', re.IGNORECASE)

class SortImage:
    def __init__(self, path, output):
        self.path = path
        self.output = output
        # create path if not exist
        if not os.path.exists(output):
            os.mkdir(output)

    def start(self):
        print self.path
        for root, dirs, files in os.walk(self.path):
            for name in files:
                filepath = join(root, name)
                if img_re.match(name):
                    if os.path.getsize(filepath) <= 100 * 1024:
                        name = "small_" + name
                        print "Start: images less than 100k detected"
                    target = join(self.output, self.getDate(filepath))
                    self.move(filepath, target, name)

    def getDate(self, ImagePath):
        try:
            img = Image.open(ImagePath)
            exif = {
                ExifTags.TAGS[k] : v
                for k, v in img._getexif().items()
                if k in ExifTags.TAGS
            }
            return exif['DateTimeOriginal'].split(" ")[0][:-3].replace(':', '_')
        except: 
            print "GETDATE: No DateTimeOriginal (key) exists in this image; resort to creating date"
            dt = datetime.datetime.strptime(time.ctime(os.path.getctime('/Volumes/Maple2TB/Recovery/Recover0/recup_dir.100/f633809968.jpg')), "%a %b %d %H:%M:%S %Y")
            return str(dt.year) + '_' + str(dt.month)

    # move given files to target directory
    def move(self, filepath, target, name):
        if not os.path.exists(target):
            os.mkdir(target)
        targetname = join(target, name)
        if os.path.exists(targetname):
            print "MOVE: Same name encountered"
            targetname = "_" + targetname
        shutil.copy(filepath, targetname)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "3 arguments expected, with the 2nd being the root path; {0} given \n".format(len(sys.argv))
        raise
    else: 
        si = SortImage(sys.argv[-2], sys.argv[-1])
        print "Path to sort images: ", si.path
        si.start()
