from os import getcwd
import json
from ..parsers.file_parser import FileParser


def transform(input_file, outfile, encoder, structureCodeRepository,
              moduleRepository):
    with FileParser(input_file, 'rb', structureCodeRepository,
                    moduleRepository) as parser:
        records = []
        for record in parser:
            records.append(record)

        with open(outfile, 'w') as fp:
            json.dump({"records": records}, cls=encoder, fp=fp)
