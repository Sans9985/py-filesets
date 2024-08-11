from glob import glob
from os.path import isdir
from sys import argv

def build_table(*files: tuple[str, bytes, int]) -> bytes:
	o: int = 0
	file_h: bytearray = bytearray()

	for f in files:
		x = bytearray()
		s: bytearray = bytearray.fromhex(hex(f[2])[2:].rjust(16, '0'))
		x += bytearray(list(map(ord, [*f[0]]))) + b'\0' + s
		file_h += x
		o += f[2]

	b: bytearray = bytearray.fromhex(hex(len(files))[2:].rjust(8, '0'))
	c: bytearray = bytearray(file_h)
	c = b + bytearray.fromhex(hex((1 + ((len(c) + 8) // 1024)) * 1024)[2:].rjust(8, '0')) + c
	return c

b: list[tuple[str, bytes, int]] = []

def getfile(pattern: str) -> list[tuple[str, bytes, int]]:
	files: list[str] = glob(pattern, recursive=True, include_hidden=True)

	for file in files:
		if isdir(".\\" + file):
			getfile(file + "\\*")
			continue
		try:
			print(f"Reading file '{file}'...")
			with open(file, 'rb') as f: b.append((file, (s := f.read()), len(s)))
		except FileNotFoundError:
			print(f"file '{file}' not found...")
			b.append(('', b'', 0))

def main() -> None:
	args: list[str] = argv[1:]

	if len(args) == 0: exit("please give me at least one file to pack...")

	for arg in args: getfile(arg)

	header: bytearray = build_table(*b)

	with open('output.pac', 'wb') as f:
		f.write(header.ljust((1 + (len(header) // 1024)) * 1024 - 1, b'\0') + b'\x98')
		for data in b:
			print(f" -> '{data[0]}' ({data[2]:0,} bytes)")
			f.write(data[1])


if __name__ == '__main__': main()