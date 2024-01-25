
    Docker layered images can now be produced via the `guix pack --format=docker --max-layers=N' command, providing a
    Docker image with many of the store paths being on their own layer to improve sharing between images.  The image is
    realized into the GNU store as a gzipped tarball.  Here is a simple example that generates a layered Docker image
    for the `hello' package:
    
         guix pack --format=docker --max-layers=N --symlink=/usr/bin/hello=bin/hello hello
    
    The `guix system image' can now produce layered Docker image by passing `--max-layers=N'.
    
    See `info "(guix) Invoking guix pack"' and `info "(guix) System Images"' for more information.
