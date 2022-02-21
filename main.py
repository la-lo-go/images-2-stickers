# Program developed by la-lo-go (https://github.com/la-lo-go)
# This program is licensed under the Mozilla Public License 2.0 (https://www.mozilla.org/en-US/MPL/2.0/)

import glob
import os
import re
import sys
from zipfile import ZipFile

from PIL import Image


def main():
    inputFolder = './input/'
    tempFolder = createFolder('temp')
    
    # Clean console
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdin.reconfigure(encoding='utf-8')
    print('<------------------- IMAGES TO STICKERS ------------------->\n')
    
    # Get all images from the input folder
    files = get_files(inputFolder)

    # Get icon from list
    iconPath = get_icon(files)
    print('Icon image: OK')
    
    # Extract icon image from list
    files.remove(iconPath)
    
    # Check if there is at least 1 image
    check_len_files(files)
    print('Images quantity: OK')
    
    # Convert icon
    imageConverter(tempFolder, iconPath, 'png')
    
    # Get author and fileName
    author = input('\nAuthor for the package: ')
    fileName = input('Package name: ')

    # Create temp folder
    createFolder(tempFolder)
    
    # Create folder to save .wasticker files
    outFolder = createFolder(fileName)

    # Split in equal list of 30 max
    files_list = splitList(files)

    # Convert and save
    for k, fs in enumerate(files_list):
        k = '-' + str(k + 1) if k > 0 else ''

        # Convert files to stickers
        filesToStickers(tempFolder, fs)

        # Zip files
        zipFiles(tempFolder, outFolder, fileName, author, k)
    
    # Remove icon files from temp folder 
    os.remove(tempFolder + 'icon.png')
    os.removedirs(tempFolder)
    
    # Close program
    input('\nType anything to exit: ')

def createFolder(folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    return './'+folder+'/'

def get_files(inFolder):
    """Returns all the files from the input folder with certains extensions

    Args:
        inFolder (str): path to the input folder

    Returns:
        list of images paths
    """
    # Get all images in folder (not icon file)
    formats = ['*.jpg', '*.png', '*.webp']
    formatsPath = [inFolder + e for e in formats]
    grabbed = [glob.glob(e) for e in formatsPath]

    # Join formats
    return grabbed[0] + grabbed[1] + grabbed[2]


def get_icon(filesPath):
    """Gets the icon path from the filesPath list

    Args:
        filesPath (list[srt]): list of images paths

    Raises:
        Exception: if the icon.png/jpg image is not in the list

    Returns:
        Path to the icon
    """
    r = re.compile('.*icon\.(jpg|png)')
    try:
        return list(filter(r.match, filesPath))[0]
    except IndexError:
        print('Icon image: FAILED')
        raise Exception('ERROR: ICON FILE IS MISSING OR NOT FOUND, please be sure that is there is an icon.png/jpg in the input folder')

def check_len_files(files):
    if len(files) == 0:
        print('Images quantity: FAILED')
        raise Exception('ERROR: There are no images in the input folder')

def imageConverter(outputFolder, filePath, img_format):
    """Converts the image pass by their path to an icon or a webp sticker

    Args:
        outputFolder (str): path to the output folder
        filePath (str): path the image 
        img_format (str): extension of the image
                    --> 'png': for the icon
                    --> 'webp': for the stickers
    Raises:
        Exception: if the passed extension is not supported
    """
    # Front image, passed as parameter
    imgFR = Image.open(filePath).convert('RGBA')

    if img_format == 'webp':  # Stickers
        savePath = outputFolder + extractName(filePath) + '.webp'

        # Transparent blank image
        imgBlank = Image.new('RGBA', (512, 512))

        # Resize the dimensions of any vertical images
        if isVertical(imgFR):
            imgFR = resizeVertical(imgFR)

        # Resize horizontal or squared images
        else:
            imgFR = resizeHorizontal(imgFR)

        # Convert to sticker and save it
        toStaticSticker(imgFR, imgBlank, savePath)

    elif img_format == 'png':  # Icon
        imgFR.resize((96, 96)).save(outputFolder + 'icon.png', img_format='png')

    else:  # Not accepted format
        raise Exception('ERROR: Invalid image format: ' + img_format)

    # Uncomment the line below for debugging purposes
    # print('-> '+filePath+' converted')


def extractName(path):
    """Returns the name of the image, without the extension

    Args:
        path (str): path to the images

    Returns:
        name of the image
    """
    # os.sep is the separator used by the system, '/' or '\'
    return path.split(os.sep)[1].split('.')[0]


def splitList(paths_list):
    """Splits the list into lists of 30 paths and the leftovers

    Args:
        paths_list (list[srt]): list of images paths

    Returns:
        list of list of paths with a max length of 30
    """
    return [paths_list[x:x + 30] for x in range(0, len(paths_list), 30)]


def filesToStickers(outputFolder, imgs_path):
    """Converts all files from a list to stickers and
    save it into a temporary a folder"""
    for img in imgs_path:
        imageConverter(outputFolder, img, 'webp')
    
    # add blank images if there is less than three images
    length = len(imgs_path)
    if length > 0 and length < 3:
        for i in range(length):
            savePath = './temp/blank'+i+'.webp'
            Image.new('RGBA', (512, 512)).save(savePath)
            imageConverter(outputFolder, savePath, 'webp')


def isVertical(img):
    return True if img.width < img.height else False


def resizeVertical(img):
    return img.resize(((img.width * 512) // img.height, 512))


def isSmaller(img):
    return True if img.width < 512 else False


def resizeHorizontal(img):
    return img.resize((512, (img.height * 512) // img.width))


def toStaticSticker(img1, img2, savePath):
    """Converts any image to a 512x512px .webp image while
    maintaining the aspect ratio of the original image

    Args:
        img1 (image): image on the front (user provided)
        img2 (image): image of the back (blank)
        savePath (str): path where the image will be saved
    """
    # Front image dimensions
    img1_w, img1_h = img1.size

    # Paste to the center
    center = ((512 - img1_w) // 2, (512 - img1_h) // 2)
    img2.paste(img1, center, mask=img1)

    # Save
    img2.save(savePath)


def zipFiles(folder_temp, folder_out, zipName, author, k):
    """Adds all the files passed to a .wastickers file and
    deletes them from the temporary directory"""
    zipName_n = folder_out + zipName + k + '.wastickers'

    with ZipFile(zipName_n, 'w') as z:
        # Move to temp folder
        os.chdir(folder_temp)

        # Write txt files
        z.writestr('author.txt', author)
        z.writestr('title.txt', zipName+k)
        z.write('./icon.png')

        for f in glob.glob('*.webp'):
            z.write(f)  # write in .wasticker
            os.remove(f)  # remove from temp folder

        # Return to root folder
        os.chdir('../')

        print('\n' + zipName_n + ' saved:')
        z.printdir()


if __name__ == '__main__':
    main()
