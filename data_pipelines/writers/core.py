from abc import ABC, abstractmethod
import json
import csv


class BaseWriter(ABC):
    @abstractmethod
    def write(self, data, file_path, **kwargs):
        pass


class CSVWriter(BaseWriter):
    def write(self, data, file_path, **kwargs):
        with open(file_path, "w") as f:
            row = next(data)
            fieldnames = row.keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(row)
            writer.writerows(data)


class JSONWriter(BaseWriter):
    def write(self, data, file_path, **kwargs):
        with open(file_path, "w") as f:
            for line in data:
                line = json.dumps(line) + "\n"
                f.write(line)


def writer_factory(writer_type):

    mapper = {"json": JSONWriter(), "csv": CSVWriter()}
    try:
        return mapper[writer_type]

    except KeyError:
        raise KeyError(f"File Extension not Recognized: {writer_type}")
