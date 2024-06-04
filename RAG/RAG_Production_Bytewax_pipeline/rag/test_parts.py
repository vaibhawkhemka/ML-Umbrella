import datetime
import json
from pathlib import Path
from typing import Iterable

from bytewax.inputs import DynamicSource, StatelessSourcePartition


def json_generator(json_files: list[Path]) -> list[dict]:
    for json_file in json_files:
        with json_file.open(encoding='utf-8') as f:
            data = json.load(f)

        yield list(data["Posts"].items())

# # Define paths to your JSON files
# json_files = [Path("C:/Users/vaibh/OneDrive/Desktop/veritus/Veritus_RAG/rag/data/paul.json")]

# # Test the json_generator function
# for item_list in json_generator(json_files):
#     for item in item_list:
#         print(item)
class JSONPartition(StatelessSourcePartition):
    def __init__(self, json_files: list[str]):
        json_files = [Path(json_file) for json_file in json_files]
        self._generator = json_generator(json_files=json_files)

    def next_batch(self, _sched: datetime) -> Iterable[dict]:
        while True:
            return next(self._generator)


class JSONSource(DynamicSource):
    def __init__(self, json_files: list[str]):
        self._json_files = json_files

    def build(
        self, now: datetime.datetime, worker_index: int, worker_count: int
    ) -> JSONPartition:
        num_files_per_worker = len(self._json_files) // worker_count
        num_leftover_files = len(self._json_files) % worker_count

        start_index = worker_index * num_files_per_worker
        end_index = start_index + num_files_per_worker
        if worker_index == worker_count - 1:
            end_index += num_leftover_files

        return JSONPartition(self._json_files[start_index:end_index])
    



# # Assuming you have a list of JSON file paths
# json_files = [
#     "C:/Users/vaibh/OneDrive/Desktop/veritus/Veritus_RAG/rag/data/paul.json",
#     # Add more file paths if needed
# ]

# # Instantiate the source
# json_source = JSONSource(json_files=json_files)

# # Assuming you have 4 workers
# num_workers = 4

# # Create partitions for each worker
# for i in range(num_workers):
#     partition = json_source.build(
#         now=datetime.datetime.now(),
#         worker_index=i,
#         worker_count=num_workers
#     )
#     # Now you can use the partition for each worker as needed
