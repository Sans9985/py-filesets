from sys import argv
from os import makedirs
from os.path import dirname
from typing import Never

def getfile(file: str) -> bytes:
	with open(file, 'rb') as f:
		return f.read()

def verify(raw_file: bytes) -> None | Never:
	max_offset: int = int.from_bytes(raw_file[4:8])
	if not raw_file[max_offset - 1] == 0x98:
		raise Exception("not a valid python package")

def decode(raw_file: bytes) -> None:
	fc: int = int.from_bytes(raw_file[0:4])
	fo: int = int.from_bytes(raw_file[4:8])
	ho: int = 8

	for _ in range(fc):
		i: int = 0
		while raw_file[ho+i] != 0: i += 1

		file_name = str(raw_file[ho:ho+i], "utf-8")
		ho += i + 1

		dn: str = dirname(file_name)
		if dn != '': makedirs(dn, exist_ok=True)

		fs: int = int.from_bytes(raw_file[ho:ho + 8])
		ho += 8
		if fs == 0:
			with open(file_name, 'w') as f: ...
		else:
			with open(file_name, 'wb') as f:
				f.write(raw_file[fo:fo + fs])

		print(f"extracted: {file_name} ({fs:0,} bytes)")

		fo += fs

def main(file: str) -> None:
	f: bytes = getfile(file)
	verify(f)
	decode(f)

if __name__ == '__main__':
    if len(argv) != 2: exit("please give me exactly one file to decode...")

    main(argv[1])