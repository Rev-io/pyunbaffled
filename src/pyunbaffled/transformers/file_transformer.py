from os import getcwd
import json
from schema.repository import Repository
from parsers.file_parser import FileParser
from encoder.key_value_encoder import KeyValueEncoder


def transform(input_file, outfile):
    with FileParser(input_file, 'rb', Repository(getcwd(), "structure_code"),
                    Repository(getcwd(), "module")) as parser:

        records = []
        for record in parser:
            records.append(record)

        with open(outfile, 'w') as fp:
            json.dump({"records": records}, cls=KeyValueEncoder, fp=fp)
