import sys
import io
import json
import re
import csv
import subprocess
import string
import random

# Constants
PROGRAM_NAME = "BC125AT-Perl Helper"
PROGRAM_CMD = "bc125at-perl-helper"
PROGRAM_VERSION = "1.2.4"
PROGRAM_AUTHOR = "Max Loiacono"
PROGRAM_URL = "https://github.com/itsmaxymoo/bc125at-perl-helper"

__OPERATION_TO_CSV = 0
__OPERATION_TO_TXT = 1


def _main():
	# Basics
	print(PROGRAM_NAME + "\nVersion " + PROGRAM_VERSION + " by " + PROGRAM_AUTHOR + "\n")

	# CliArgs handler
	if len(sys.argv) < 2:
		_command_help()
	elif sys.argv[1] == "c" and len(sys.argv) == 4:
		_convert(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == "r" and len(sys.argv) == 3:
		_scanner_read(sys.argv[2])
	elif sys.argv[1] == "w" and len(sys.argv) == 3:
		_scanner_write(sys.argv[2])
	elif sys.argv[1] == "clean" and len(sys.argv) == 3:
		_clean_csv(sys.argv[2])
	else:
		_command_help()

	exit(0)


def _command_help():
	print("Usage:\n\t" + PROGRAM_CMD + " <command> <1?> <2?>\n")
	print("Please specify a command:")
	print("\tr <out file>\t\tRead channels from the scanner and output a CSV file.")
	print("\tw <CSV file>\t\tWrite a CSV file directly to the scanner.")
	print("\tc <in file> <out file>\tConvert a bc125at-perl file to CSV or vice-versa.")
	print("\tclean <CSV file>\tReset any channels without a frequency set.")
	exit(1)


def _write_out(out_file_name, out_data):
	try:
		f = open(out_file_name, "w")
		f.write(out_data)
		f.close()
		print("Success! Wrote file to: " + out_file_name)
	except:
		print("ERROR: Could not write file: " + out_file_name)
		exit(1)


def _bc125at2json(in_data):
	# Convert text to JSON
	in_data = re.sub("(\s(?=[a-z_]* => '))|(\s(?==> '))", "\"", in_data)
	in_data = in_data.replace("=> '", ": '")
	in_data = in_data.replace("'", "\"")
	in_data = in_data.replace("\"pri\": \"0\",", "\"pri\": \"0\"")
	in_data = in_data.replace("\"pri\": \"1\",", "\"pri\": \"1\"")
	in_data = re.sub("},\s*]", "}]", in_data)

	try:
		in_data = json.loads(in_data)
		return in_data
	except:
		print("ERROR: Could not parse file. Did you modify it?")
		exit(1)


def _list2bc125at(in_data):
	# Setup output file
	out_data = "[\n"

	# Generate output data
	ind = 1
	for c in in_data:
		out_data += "{\n"
		out_data += "cmd => 'CIN',\n"
		out_data += "index => '" + str(ind) + "',\n"
		if len(c[0]) > 16:
			print("ERROR: \"" + c[0] + "\" is longer than 16 characters!")
			exit(1)
		out_data += "name => '" + c[0] + "',\n"
		out_data += "frq => '" + c[1] + "',\n"
		if c[2] not in ["FM", "NFM", "AM", "AUTO"]:
			print("ERROR: Unknown modulation: \"" + c[2] + "\"")
			exit(1)
		out_data += "mod => '" + c[2] + "',\n"
		out_data += "ctcss_dcs => '" + c[3] + "',\n"
		if int(c[4]) < 0:
			print("ERROR: Delay must be >=0!")
			exit(1)
		out_data += "dly => '" + c[4] + "',\n"
		if c[5] != "0" and c[5] != "1":
			print("ERROR: Lockout must be either 0 or 1!")
			exit(1)
		out_data += "lout => '" + c[5] + "',\n"
		if c[6] != "0" and c[6] != "1":
			print("ERROR: Priority must be either 0 or 1!")
			exit(1)
		out_data += "pri => '" + c[6] + "',\n"
		out_data += "},\n"

		ind += 1
	out_data += "]\n"

	return out_data


def _json2csv(in_json):
	out_data = "Name,Frequency,Modulation,CTCSS Tone,Delay,Locked Out,Priority\n"

	try:
		for c in in_json:
			out_data += "\"" + c["name"] + "\"" + "," + "\"" + c["frq"] + "\"" + "," + "\"" + c["mod"] + "\"" + "," + "\"" + c["ctcss_dcs"] + "\"" + "," + "\"" + c["dly"] + "\"" + "," + "\"" + c["lout"] + "\"" + "," + "\"" + c["pri"] + "\"" + "\n"
	except:
		print("ERROR: Could not convert file. Did you modify it?")
		exit(1)

	return out_data


def _list2csv(in_list):
	return _json2csv(_bc125at2json(_list2bc125at(in_list)))


def _csv2list(in_data):
	# Convert CSV to TXT
	in_data = in_data.replace("Name,Frequency,Modulation,CTCSS Tone,Delay,Locked Out,Priority\n", "")
	in_data = in_data.replace("Name,Frequency,Modulation,\"CTCSS Tone\",Delay,\"Locked Out\",Priority\n", "")
	# Read CSV
	in_data = csv.reader(io.StringIO(in_data))
	in_data = list(in_data)

	if len(in_data) != 500:
		print("ERROR: Total channels does not equal 500! (" + str(len(in_data)) + ")")
		exit(1)
	
	return in_data


def _read_file(in_file_name):
	# Test input files
	in_file = None
	try:
		in_file = open(in_file_name)
		in_file.read(4)
		in_file.seek(0)
	except:
		print("ERROR: Could not read file: " + in_file_name)
		exit(1)

	in_data = in_file.read()
	in_file.close()

	return in_data


def _convert(in_file, out_file):
	# Test input files
	operation = None
	if in_file.lower().endswith('.csv'):
		operation = __OPERATION_TO_TXT
	else:
		operation = __OPERATION_TO_CSV

	# Begin conversion
	print("Converting " + in_file + " to " + ("CSV" if operation == __OPERATION_TO_CSV else "Text"))

	in_data = _read_file(in_file)
	out_data = None

	if operation == __OPERATION_TO_CSV:
		in_data = _bc125at2json(in_data)
		
		# Write CSV
		out_data = _json2csv(in_data)
	else:
		in_data = _csv2list(in_data)

		out_data = _list2bc125at(in_data)
		
	_write_out(out_file, out_data)


def rand_string(length):
	return "".join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))


def _scanner_read(outFile):
	print("Reading from scanner...")

	f = rand_string(36)
	subprocess.call(["sudo", "bc125at-perl", "driver"])
	subprocess.call(["sudo", "bc125at-perl", "channel", "read", "--file=/tmp/" + f + ".txt"])
	_convert("/tmp/" + f + ".txt", outFile)


def _scanner_write(inFile):
	print("Writing to scanner...")

	if not inFile.lower().endswith(".csv"):
		print("ERROR: File must end with .csv")
		exit(1)

	f = rand_string(36)
	_convert(inFile, "/tmp/" + f + ".txt")
	subprocess.call(["sudo", "bc125at-perl", "driver"])
	subprocess.call(["sudo", "bc125at-perl", "channel", "write", "--file=/tmp/" + f + ".txt"])


def _clean_csv(inFile):
	print("Cleaning " + inFile)
	if not inFile.lower().endswith(".csv"):
		print("ERROR: File must end with .csv")
		exit(1)

	fc = _read_file(inFile)
	fc = _csv2list(fc)

	for i in range(0, len(fc)):
		if fc[i][1] in ["0.000", "0"]:
			fc[i] = ["", "0.000", "AUTO", "0", "2", "1", "0"]

	fc = _list2csv(fc)
	_write_out(inFile, fc)
