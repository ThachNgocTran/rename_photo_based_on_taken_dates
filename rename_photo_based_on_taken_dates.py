import PIL.Image
import os
import os.path
import shutil
import os.path

input_dir = r"Processed"
output_dir = r"Processed_Out"
path_date_taken_dict = {}
date_takens = []
date_takens_index_dict = {}

strange_files = []

unknown_index = 0

def get_index():
    global unknown_index
    unknown_index += 1
    return unknown_index

allowed_exts = ["jpg", "jpeg", "png"]
EXIF_TAKEN_DATE = 36867

for current_folder, sub_folders, files in os.walk(input_dir):
    for file in files:
        file_path = (r"%s\%s" % (current_folder, file)).lower()
        file_ext = os.path.splitext(file_path)[1]                       # if no extension, still receive ''.
        if file_ext in allowed_exts:
            print("Processing [%s]" % (file_path))
            img = PIL.Image.open(file_path)
            if isinstance(img, PIL.PngImagePlugin.PngImageFile):        # No "Taken Date" for PNG file.
                date_taken = "UnknownDateTaken_%s" % (get_index())
            elif isinstance(img, PIL.JpegImagePlugin.JpegImageFile):
                exif = img._getexif()
                if not exif is None and EXIF_TAKEN_DATE in exif:        # Some JPG don't contain EXIF. Some do but doesn't have field "Date Taken".
                    date_taken = exif[EXIF_TAKEN_DATE]
                else:
                    date_taken = "UnknownDateTaken_%s" % (get_index())
            else:
                raise ValueError("Unsupported file type.")
            path_date_taken_dict[file_path] = date_taken
            date_takens.append(date_taken)

            img.close()
        else:
            strange_files.append(file_path)

if len(strange_files) > 0:
    print("Those files are not processed: [%s]" % (strange_files))

date_takens = sorted(date_takens)

for idx, date_taken in enumerate(date_takens):
    date_takens_index_dict[date_taken] = idx

print("Preparing to copy.")

for  file in path_date_taken_dict.keys():
    date_taken = path_date_taken_dict[file]
    index = date_takens_index_dict[date_taken]
    file_ext = file_ext = os.path.splitext(file)[1]
    print("Copying [%s]" % (file))
    if date_taken.startswith("UnknownDateTaken"):
        target_file_name = r"%s\Image_%s_(UnknownDateTaken)%s" % (output_dir, index, file_ext)
    else:
        target_file_name = r"%s\Image_%s%s" % (output_dir, index, file_ext)
    shutil.copy2(file, target_file_name)
