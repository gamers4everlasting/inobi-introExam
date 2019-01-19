import image_slicer
import io
import zipfile


tiles = image_slicer.slice('a.jpg', 25)
image_slicer.save_tiles(tiles, directory='./',\
prefix='a', format='JPG')
print (tiles)
