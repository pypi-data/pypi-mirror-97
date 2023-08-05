from dataclasses import dataclass


@dataclass
class ProfanityReport:

    error_id: str
    line_number: int
    message: str
