#!/usr/bin/env python3
import logging
import precommit_diffcheck

def main():
	logging.basicConfig(level=logging.DEBUG)
	for diffline in precommit_diffcheck.removedlines():
		print(
			"{diffline.filename}: {diffline.linenumber} {op} {diffline.content}".format(
				diffline=diffline, op="+" if diffline.added else "-"))

if __name__ == "__main__":
	main()
