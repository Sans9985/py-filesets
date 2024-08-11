# py-filesets

this repo has 2 files:

## merger.py
simply puts whatever files you give it into an `output.pac` file.

example:
```
python merger.py file1.txt folder\*
```

this script takes 'infinite' parameters, and accepts wildcards.

## separator.py
does the opposite as `merger.py`

example:
```
python separator.py test.pac
```

this script can only handle one `.pac` file at a time.

these scripts will also print the files that they're working with.

(example output of `merger.py`)
```
Reading file 'file1.txt'...
Reading file 'file2.txt'...
Reading file 'image.bmp'...
 -> 'file1.txt' (14 bytes)
 -> 'file2.txt' (20 bytes)
 -> 'image.bmp' (307,254 bytes)
```