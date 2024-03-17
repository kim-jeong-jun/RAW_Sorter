# RAW_Sorter
Made for heavy camera users.
RAW file sorting code written in Python.

## Function
1. This code gather all RAW image files(*.NEF, *.DNG, and *.JPG) in subfolder of your input folder.
2. The sorted folder generates as the manner below. (Regards as EXIF file data.)
   'camera name'/'year'/'year-month-date'
3. If there is redundant files, this code makes redundant subfolder under each folder.
4. If there is more than two redundant files, this code will negelect and do not move that file.

# HOW TO USE
1. type 'python3 ~/sort.py'
2. type input directory:
3. type destination directory:
4. Waiting for moving
5. Check the result!

### Disclaimer
1. This code use 'os.move' for moving files. Please check the file is safely backed up.
2. This code makes '~/Redundant' directory when there is redundant files. But it does not check the checksum of files. It only regards the file name. So you have to delete manually.
3. The directory naming of this code based on the camera manufacturer's sense.
