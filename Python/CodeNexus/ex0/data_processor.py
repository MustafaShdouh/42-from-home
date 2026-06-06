import abc
import typing


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self.name: str = "Data Processor"
        self._data: list[tuple[int, str]] = []
        self.total_processed: int = 0

    def remaining(self) -> int:
        return len(self._data)

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

    def _is_log_dict(self, data: typing.Any) -> bool:
        return (
            isinstance(data, dict)
            and all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            )
        )

    def validate(self, data: typing.Any) -> bool:
        if self._is_log_dict(data):
            return True
        if isinstance(data, list):
            return all(
                self._is_log_dict(x) for x in data
            )
        return False

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if isinstance(data, dict):
            if not self._is_log_dict(data):
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
                self._is_log_dict(x) for x in data
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


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    print(
        "Trying to validate input '42': "
        f"{numeric.validate(42)}"
    )
    print(
        "Trying to validate input 'Hello': "
        f"{numeric.validate('Hello')}"
    )
    print(
        "Test invalid ingestion of string 'foo' "
        "without prior validation:"
    )
    try:
        numeric.ingest("foo")
    except ValueError as e:
        print(f"Got exception: {e}")

    data_num: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {data_num}")
    numeric.ingest(data_num)
    print("Extracting 3 values...")
    i = 0
    while i < 3:
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")
        i += 1

    print("\nTesting Text Processor...")
    text = TextProcessor()
    print(
        "Trying to validate input '42': "
        f"{text.validate(42)}"
    )
    data_text: list[str] = ['Hello', 'Nexus', 'World']
    print(f"Processing data: {data_text}")
    text.ingest(data_text)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(
        "Trying to validate input 'Hello': "
        f"{log.validate('Hello')}"
    )
    data_log: list[dict[str, str]] = [
        {'log_level': 'NOTICE',
         'log_message': 'Connection to server'},
        {'log_level': 'ERROR',
         'log_message': 'Unauthorized access!!'}
    ]
    print(f"Processing data: {data_log}")
    log.ingest(data_log)
    print("Extracting 2 values...")
    i = 0
    while i < 2:
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")
        i += 1
