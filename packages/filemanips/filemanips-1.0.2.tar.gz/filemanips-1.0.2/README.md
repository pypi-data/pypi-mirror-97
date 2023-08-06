# `filemanips`

`filemanips` is a library that helps with copying, moving, and deleting files. Yes, other file manipulation libraries exist (there are even built-in ones), but this one works without throwing errors that others do, by satisfying certain preconditions automatically, or correctly choosing a function to use.

## Usage

Use the public functions to copy, move, and delete files and folders.

```python
from filemanips import copy, move, delete

copy("source_file_0", "/opt/ploopy/dest_file")  # Copies source_file_0 into /opt/ploopy/, creating any nonexistent folders along the way, with the destination file named dest_file

copy("source_file_1", "/opt/ploopy/dest_folder/")  # Copies source_file_1 into /opt/ploopy/dest_folder/, creating any nonexistent folders along the way, with the destination file named source_file_1

copy("source_folder_0", "/opt/ploopy/dest_folder")  # Copies source_folder_0 into /opt/ploopy/, creating any nonexistent folders along the way, with the destination folder named dest_folder

copy("source_folder_1", "/opt/ploopy/dest_folder/")  # Copies source_folder_1 into /opt/ploopy/dest_folder/, creating any nonexistent folders along the way, with the destination folder named source_folder_1

move("source_file_2", "/opt/ploopy/dest_file")  # Moves source_file_2 into /opt/ploopy/, creating any nonexistent folders along the way, with the destination file named dest_file

move("source_file_3", "/opt/ploopy/dest_folder/")  # Moves source_file_3 into /opt/ploopy/dest_folder/, creating any nonexistent folders along the way, with the destination file named source_file_3

move("source_folder_2", "/opt/ploopy/dest_folder")  # Moves source_folder_2 into /opt/ploopy/, creating any nonexistent folders along the way, with the destination folder named dest_folder

move("source_folder_3", "/opt/ploopy/dest_folder/")  # Moves source_folder_3 into /opt/ploopy/dest_folder/, creating any nonexistent folders along the way, with the destination folder named source_folder_3

delete("source_file_4")  # Deletes the file source_file_4

delete("source_folder_4")  # Deletes the folder source_folder_4 and everything in it
```
