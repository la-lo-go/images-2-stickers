# Images 2 Stickers
Using Python and the [.wastickers compressed files format](https://fileinfo.com/extension/wastickers) by Viko & Co. convert images to stickers packs for Whatsapp and iMessage.

## Prerequisites

 1. [Python 3+](https://www.python.org/downloads/)
 2. Sticker Maker app (Download: [iOS](https://apps.apple.com/mx/app/sticker-maker-studio/id1443326857)/[Android](https://play.google.com/store/apps/details?id=com.marsvard.stickermakerforwhatsapp&hl=es&gl=US))


## Steps

1. Clone (or download) the repository: 
	``` bash
	git clone https://github.com/la-lo-go/images-to-stickers
	```
  
2. Install the packages:
	``` bash
	python -m pip install -r requirements.txt
	```

## How to use the program
 1. Into the `input` folder copy **all** the images you want to convert (3 minimum) and an icon image as `icon.png` or `icon.jpg`.
 2. Run the main.py file.
 3. Input the *name of the sticker package* and the *author*.
 4. Transfer the `.wastickers` files to your phone.
 5. Open the files with the Sticker Maker app and add them to Whatsapp.

## Roadmap

 - [X] Automatically create multiple packs with just one click regardless of the number of photos.
 - [ ] Create different packs based on the files organization.
 - [ ] Add .gif support.

## License
[Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/)

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://www.mozilla.org/en-US/MPL/2.0/)


