# gimp_macro_save

macro for gimp to save image with numbered suffix

When saving an image file the script appends a suffix at the end of the filename
with the form '_gp_nn', with nn as a number {'01' .. '99'}.
If this suffix already exists, nn is incremented.
If there is no such suffix, '_gp_01' is appended.

image.jpg       -> image_gp_01.jpg or
image_gp_32.jpg -> image_gp_33.jpg

But take care, that the script by itself does not check if it is overwriting an existing file !
If you are saving 'image_gp_32.jpg' with this macro, and 'image_gp_33.jpg' exists, then 'image_gp_33.jpg' may be overwritten.

The macro will appear in the file menu as 'Save with __gp__NN & clean'

Path for macros:
C:\Program Files\GIMP 2.9\lib\gimp\2.0\plug-ins
or
..\PortableApps\GIMPPortable\App\gimp\lib\gimp\2.0\plug-ins
