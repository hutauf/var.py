# var.py
script that copies and changes text files based on a config file

For example, you have a text file with a script for ffmpeg which extracts mp3 from avi

ffmpeg -i myinputfile1.avi -vn output.mp3

put this text file somewhere, add a var.conf next to it, write in "in=name_of_textfile" and "out=files"
Then "$myinputfile1.avi" and then a long list of actual inputfiles

Then run the var.py-script, which will create a new script file for every inputfile you put into the var.conf

Also works for multiple variables, like inputfiles and settings for example.

The cool thing is it also works great on large files, as it will read the files line-by-line and not the complete file at once!

