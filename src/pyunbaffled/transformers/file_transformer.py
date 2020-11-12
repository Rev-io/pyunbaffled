from os import getcwd
import json
from schemas.repository import Repository
from parsers.file_parser import FileParser


def transform(input_file, outfile, encoder):
    with FileParser(input_file, 'rb', Repository(getcwd(), "structure_code"),
                    Repository(getcwd(), "module")) as parser:

        records = []
        for record in parser:
            records.append(record)

        with open(outfile, 'w') as fp:
            json.dump({"records": records}, cls=encoder, fp=fp)
