import abc
import typing


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self.name: str = "Data Processor"
        self._data: list[tuple[int, str]] = []
        self.total_processed: int = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        ...

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        return self._data.pop(0)


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Numeric Processor"

    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(
                isinstance(x, (int, float)) for x in data
            )
        return False

    def ingest(
        self, data: int | float | list[int | float]
    ) -> None:
        if isinstance(data, (int, float)):
            self._data.append(
                (self.total_processed, str(data))
            )
            self.total_processed += 1
        elif isinstance(data, list):
            if not all(
                isinstance(x, (int, float)) for x in data
            ):
                raise ValueError("Improper numeric data")
            for item in data:
                self._data.append(
                    (self.total_processed, str(item))
                )
                self.total_processed += 1
        else:
            raise ValueError("Improper numeric data")


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Text Processor"

    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(
                isinstance(x, str) for x in data
            )
        return False

    def ingest(self, data: str | list[str]) -> None:
        if isinstance(data, str):
            self._data.append(
                (self.total_processed, data)
            )
            self.total_processed += 1
        elif isinstance(data, list):
            if not all(
                isinstance(x, str) for x in data
            ):
                raise ValueError("Improper text data")
            for item in data:
                self._data.append(
                    (self.total_processed, item)
                )
                self.total_processed += 1
        else:
            raise ValueError("Improper text data")


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Log Processor"

    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, dict):
            if all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            ):
                return True
        if isinstance(data, list):
            return all(
                isinstance(x, dict)
                and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in x.items()
                )
                for x in data
            )
        return False

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if isinstance(data, dict):
            if not all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            ):
                raise ValueError("Improper log data")
            log_str = (
                f"{data['log_level']}: "
                f"{data['log_message']}"
            )
            self._data.append(
                (self.total_processed, log_str)
            )
            self.total_processed += 1
        elif isinstance(data, list):
            if not all(
                isinstance(x, dict)
                and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in x.items()
                )
                for x in data
            ):
                raise ValueError("Improper log data")
            for entry in data:
                log_str = (
                    f"{entry['log_level']}: "
                    f"{entry['log_message']}"
                )
                self._data.append(
                    (self.total_processed, log_str)
                )
                self.total_processed += 1
        else:
            raise ValueError("Improper log data")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(
        self, proc: DataProcessor
    ) -> None:
        self._processors.append(proc)

    def process_stream(
        self, stream: list[typing.Any]
    ) -> None:
        for element in stream:
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    break
            else:
                print(
                    "DataStream error - Can't process "
                    f"element in stream: {element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            print(
                f"{proc.name}: total "
                f"{proc.total_processed} items "
                f"processed, remaining "
                f"{len(proc._data)} on processor"
            )


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===\n")

    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    print("Registering Numeric Processor\n")
    numeric = NumericProcessor()
    ds.register_processor(numeric)

    batch: list[typing.Any] = [
        'Hello world',
        [3.14, -1, 2.71],
        [{'log_level': 'WARNING',
          'log_message':
          'Telnet access! Use ssh instead'},
         {'log_level': 'INFO',
          'log_message':
          'User wil is connected'}],
        42,
        ['Hi', 'five']
    ]
    print(
        "Send first batch of data on stream: "
        f"{batch}"
    )
    ds.process_stream(batch)
    ds.print_processors_stats()

    print("\nRegistering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    ds.register_processor(text)
    ds.register_processor(log)

    print("Send the same batch again")
    ds.process_stream(batch)
    ds.print_processors_stats()

    print(
        "\nConsume some elements from the data "
        "processors: Numeric 3, Text 2, Log 1"
    )
    i = 0
    while i < 3:
        numeric.output()
        i += 1
    j = 0
    while j < 2:
        text.output()
        j += 1
    log.output()
    ds.print_processors_stats()
