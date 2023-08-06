"""Flywheel utilities and common helpers."""
import importlib.metadata as importlib_metadata
import re
import typing as t
from pathlib import Path
from tempfile import SpooledTemporaryFile

__version__ = importlib_metadata.version(__name__)


# FORMATTERS


PLURALS = {
    "study": "studies",
    "series": "series",
    "analysis": "analyses",
}


def pluralize(singular: str, plural: str = "") -> str:
    """Return plural for given singular noun."""
    if plural:
        PLURALS[singular.lower()] = plural.lower()
    return PLURALS.get(singular, f"{singular}s")


def quantify(num: int, singular: str, plural: str = "") -> str:
    """Return "counted str" for given num and word: (3,'file') => '3 files'."""
    if num == 1:
        return f"1 {singular}"
    plural = pluralize(singular, plural)
    return f"{num} {plural}"


def hrsize(size: int) -> str:
    """Return human-readable file size for given number of bytes."""
    fsize, unit, decimals = float(size), "B", 0
    for unit in "BKMGTPEZY":
        decimals = 0 if unit == "B" or round(fsize) > 9 else 1
        if round(fsize) < 100 or unit == "Y":
            break
        fsize /= 1024.0
    return f"{fsize:.{decimals}f}{unit}"


def hrtime(seconds: int) -> str:
    """Return human-readable time duration for given number of seconds."""
    remainder = seconds
    parts: t.List[str] = []
    units = {"y": 31536000, "w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
    for unit, seconds_in_unit in units.items():
        quotient, remainder = divmod(remainder, seconds_in_unit)
        if len(parts) > 1 or (parts and not quotient):
            break
        if quotient or (unit == "s" and not parts):
            parts.append(f"{int(quotient)}{unit}")
    return " ".join(parts)


def str_to_python_id(raw_string: str) -> str:
    """Convert any string to a valid python identifier in a reversible way."""

    def char_to_hex(match: t.Match) -> str:
        return f"__{ord(match.group(0)):02x}__"

    raw_string = re.sub(r"^[^a-z_]", char_to_hex, raw_string, flags=re.I)
    return re.sub(r"[^a-z_0-9]{1}", char_to_hex, raw_string, flags=re.I)


def python_id_to_str(python_id: str) -> str:
    """Convert a python identifier back to the original/normal string."""

    def hex_to_char(match: t.Match) -> str:
        return chr(int(match.group(1), 16))

    return re.sub(r"__([a-f0-9]{2})__", hex_to_char, python_id)


# PARSERS


def parse_hrsize(value: str) -> int:
    """Return number of bytes for given human-readable file size."""
    pattern = r"(?P<num>\d+(\.\d*)?)\s*(?P<unit>([KMGTPEZY]i?)?B?)"
    match = re.match(pattern, value, flags=re.I)
    if match is None:
        raise ValueError(f"Cannot parse human-readable size: {value}")
    num = float(match.groupdict()["num"])
    unit = match.groupdict()["unit"].upper().rstrip("BI") or "B"
    units = {u: 1024 ** i for i, u in enumerate("BKMGTPEZY")}
    return int(float(num) * units[unit])


def parse_hrtime(value: str) -> int:
    """Return number of seconds for given human-readable time duration."""
    parts = value.split()
    units = {"y": 31536000, "w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
    seconds = 0
    regex = re.compile(r"(?P<num>\d+)(?P<unit>[ywdhms])", flags=re.I)
    for part in parts:
        match = regex.match(part)
        if match is None:
            raise ValueError(f"Cannot parse human-readable time: {part}")
        num, unit = match.groups()
        seconds += int(num) * units[unit.lower()]
    return seconds


URL_RE = re.compile(
    r"^"
    r"(?P<scheme>[^:]+)://"
    r"((?P<username>[^:]+):(?P<password>[^@]+)@)?"
    r"(?P<host>[^:/?#]*)"
    r"(:(?P<port>\d+))?"
    r"((?P<path>/[^?#]+))?"
    r"(\?(?P<query>[^#]+))?"
    r"(#(?P<fragment>.*))?"
    r"$"
)


def parse_url(url: str, pattern: t.Pattern = URL_RE) -> t.Dict[str, str]:
    """Return dictionary of fields parsed from a URL."""
    match = pattern.match(url)
    if not match:
        raise ValueError(f"Invalid URL: {url}")
    parsed = {k: v for k, v in match.groupdict().items() if v is not None}
    params = parsed.pop("query", "")
    if params:
        # store query params directly on the result
        for param in params.split("&"):
            if "=" not in param:
                param = f"{param}="
            key, value = param.split("=", maxsplit=1)
            if "," in value:
                value = value.split(",")
            parsed[key] = value
    return attrify(parsed)


# DICTS


class AttrDict(dict):
    """Dictionary with attribute access to valid-python-id keys."""

    def __getattr__(self, name: str):
        """Return dictionary keys as attributes."""
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc


def attrify(data):
    """Return data with dicts cast to attrdict for dot notation access."""
    if isinstance(data, dict):
        return AttrDict((key, attrify(value)) for key, value in data.items())
    if isinstance(data, list):
        return [attrify(elem) for elem in data]
    return data


def flatten_dotdict(deep: dict, prefix: str = "") -> dict:
    """Flatten dictionary using dot-notation: {a: b: c} => {a.b: c}."""
    flat = {}
    for key, value in deep.items():
        key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten_dotdict(value, prefix=key))
        else:
            flat[key] = value
    return flat


def inflate_dotdict(flat: dict) -> dict:
    """Inflate flat dot-notation dictionary: {a.b: c} => {a: b: c}."""
    deep = node = {}  # type: ignore
    for key, value in flat.items():
        parts = key.split(".")
        path, key = parts[:-1], parts[-1]
        for part in path:
            node = node.setdefault(part, {})
        node[key] = value
        node = deep
    return deep


# FILES

SPOOLED_TMP_MAX_SIZE = 1 << 20  # 1MB

AnyPath = t.Union[str, Path]
AnyFile = t.Union[AnyPath, t.IO]


class BinFile:
    """File class for accessing local files and file-like objects similarly."""

    def __init__(
        self, file: t.Union[AnyFile, "BinFile"], write: bool = False, metapath: str = ""
    ) -> None:
        """Open a file for reading or writing.

        Args:
            file (str|Path|file): The local path to open or a file-like object.
            metapath (str, optional): Override the exposed metapath attribute if given.
            write (bool, optional): Whether to open for writing. Default: False.
        """
        self.file: t.IO = None  # type: ignore
        self.localpath = None
        self.file_open = False
        self.file_write = write
        mode, check = ("wb", "writable") if write else ("rb", "readable")
        if isinstance(file, (str, Path)):
            self.file_open = True
            self.localpath = str(file)
            file = Path(self.localpath).open(mode=mode)
        elif isinstance(file, BinFile):
            file = t.cast(t.IO, file.file)
        if not hasattr(file, check) or not getattr(file, check)():
            raise ValueError(f"File {file!r} is not {check}")
        self.file = file
        self.metapath = metapath or self.localpath

    def close(self) -> None:
        """Close file or seek to the start of buffers."""
        if self.file_open:
            self.file.close()
        else:
            self.file.seek(0)

    def __getattr__(self, name: str):
        """Return attrs proxied from the file."""
        return getattr(self.file, name)

    def __iter__(self):
        """Iterate over lines."""
        return self.file.__iter__()

    def __next__(self):
        """Get next line."""
        return self.file.__next__()

    def __enter__(self) -> "BinFile":
        """Enter 'with' context."""
        return self

    def __exit__(self, exc_cls, exc_val, exc_trace) -> None:
        """Close file when exiting 'with' context."""
        self.close()

    def __repr__(self) -> str:
        """Return string representation of the File."""
        file_str = self.metapath or f"{type(self.file).__name__}/{hex(id(self.file))}"
        return f"{type(self).__name__}('{file_str}', write={self.file_write})"


class TempFile(SpooledTemporaryFile):
    """Extend SpooledTemporaryFile class with readable and writable methods."""

    def __init__(self, max_size: int = SPOOLED_TMP_MAX_SIZE):
        """Simplified interface to create a SpooledTemporaryFile instance."""
        super().__init__(max_size=max_size)

    @staticmethod
    def readable() -> bool:
        """Return that the file is readable."""
        return True

    @staticmethod
    def writable() -> bool:
        """Return that the file is writable."""
        return True
