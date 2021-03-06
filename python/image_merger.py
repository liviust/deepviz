
from __future__ import division

from PIL import Image
import numpy as np
import os

# Get all the images from a directory and make a
# single big picture out of them.

# Each image must already have this size
imsize  = 64;
imfname = 'images.csv';

dirname = '../imgs/facespics_{0}/'.format( imsize );

with open( 'images.csv' ) as myfile:
  fnames = myfile.readlines();

# === Obtain the number of iamges
totalimgs = len( fnames );
print( 'There are {0} images in total'.format( totalimgs ) );

# === Determine the size of the big image tile

# The closest squre number
closest_sqroot = np.ceil( np.sqrt( totalimgs ) );
closest_square = closest_sqroot ** 2;

per_row = closest_sqroot;                # How many imgs we can fit per row
nrows   = closest_sqroot;   # How many rows we need

print( 'There are {0} images per row, and {1} rows'.format(per_row, nrows ));

# === Create a large array to put the images in
bigtile = np.zeros( (imsize*nrows, per_row*imsize, 3), dtype=np.uint8 );
imcounter = 0;

# Loop through the images again
for f in fnames:
  f = f.strip();

  # Read the image
  im = Image.open( dirname + f );
  im = np.asarray( im, dtype="uint8" )

  # What is the row of this image?
  imrow = np.floor( imcounter / per_row )
  imcol = (imcounter % per_row)

  # print( 'Working on image {0}: {1}, size {2}'.format( imcounter, f, im.shape ) );
  # print( 'The row is {0} and the column is {1}'.format( imrow, imcol ));

  bigtile[ imrow*imsize:(imrow+1)*imsize, imsize*imcol:imsize*(imcol+1), 0:3 ] = im[:,:,0:3];
  imcounter = imcounter + 1;

# Keep only the images that we actually read
bigtile = bigtile[:, 1:(imcounter-1)*imsize, :];

#Save the numpy array as a big image
im = Image.fromarray( bigtile );
im.save('../imgs/facespics_{0}/bigtile.jpg'.format(imsize));

