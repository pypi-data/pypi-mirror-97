# Utilities
Library containing all kinds of python utilities.

## Install
`$ pip install dvdp.utils`

## Data
### DataSaver
`from dvdp.utils.data import DataSaver`  
Helps with saving large datasets with images (or other np.arrays) to disk.
It also allows you to load them with DataSaver.load_data().

### fetch images
`from dvdp.utils.data import fetch_images`  
Fetch all images from a directory.  
Load them as a list of numpy arrays or a list Paths.