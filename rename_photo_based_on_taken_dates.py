import PIL.Image
import shutil, os.path
from typing import List, Dict
from argparse import ArgumentParser
import functools

parser = ArgumentParser()
parser.add_argument("-i", "--input-dir", dest="input_dir", help="Input directory")
parser.add_argument("-o", "--output-dir", dest="output_dir", default="", help="Output directory")

args = parser.parse_args()

input_dir = args.input_dir
output_dir = "%s_Out" % (input_dir) if len(args.output_dir) == 0 else args.output_dir
file_path_date_taken_dict: Dict[str, str] = {}

unknown_index = 0
UNKNOWN_DATE_TAKEN = "UnknownDateTaken"

def get_index() -> str:
    global unknown_index
    unknown_index += 1
    return "%s_%s" % (UNKNOWN_DATE_TAKEN, unknown_index)

allowed_exts = {".jpg", ".jpeg", ".png"}
EXIF_TAKEN_DATE = 36867

print("*** Start ***")

try:
    for current_folder, sub_folders, files in os.walk(input_dir):
        for file_path in files:
            file_path = (r"%s\%s" % (current_folder, file_path)).lower()
            file_ext = os.path.splitext(file_path)[1]                       # If no extension, still receive ''.
            if file_ext in allowed_exts:
                print("Found [%s]..." % (file_path))
                img = PIL.Image.open(file_path)
                if isinstance(img, PIL.PngImagePlugin.PngImageFile):        # No "Taken Date" for PNG file.
                    date_taken = get_index()
                elif isinstance(img, PIL.JpegImagePlugin.JpegImageFile):
                    exif = img._getexif()
                    if not exif is None and EXIF_TAKEN_DATE in exif:        # Some JPG don't contain EXIF. Some do but doesn't have field "Date Taken".
                        date_taken = exif[EXIF_TAKEN_DATE]
                    else:
                        date_taken = get_index()
                else:
                    raise ValueError("File type doesn't match file extension. [%s]" % (file_path))

                file_path_date_taken_dict[file_path] = date_taken
                img.close()

    date_takens: List[str] = sorted(file_path_date_taken_dict.values())
    date_taken_index_dict: Dict[str, int] = {}

    for idx, date_taken in enumerate(date_takens):
        date_taken_index_dict[date_taken] = idx

    for (file_path, date_taken) in file_path_date_taken_dict.items():
        index = date_taken_index_dict[date_taken]
        file_ext = os.path.splitext(file_path)[1]
        target_file_name = r"%s\Image_%s%s%s" % (output_dir, index, "_(%s)" % (UNKNOWN_DATE_TAKEN) if date_taken.startswith(UNKNOWN_DATE_TAKEN) else "", file_ext)
        print("Copying to [%s]..." % (target_file_name))
        shutil.copy2(file_path, target_file_name)

    print("Statistics: Found [%s] files. [%s] don't have Taken Date." % \
          (len(file_path_date_taken_dict.keys()),
           functools.reduce(lambda val, ele: val + 1 if ele.startswith(UNKNOWN_DATE_TAKEN) else val, file_path_date_taken_dict.values(), 0)))
    print("*** Executed ok ***")

except Exception as e:
    print("*** Exception: [%s] ***" % (str(e)))

print("*** End ***")
