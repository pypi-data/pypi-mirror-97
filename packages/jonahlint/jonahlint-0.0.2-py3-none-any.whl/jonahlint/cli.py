from pathlib import Path
from typing import Union

import click

from jonahlint.profanity_analyzer import ProfanityAnalyzer
from jonahlint.profanity_checker import ProfanityChecker
from jonahlint.sources_finder import SourcesFinder
from jonahlint import __version__


def get_profane_words():
    profane_words_path = Path(__file__).parent / "resources" / "profane_words.txt"
    with open(profane_words_path, mode="r") as pd:
        profane_words = pd.readlines()
    return [word.strip() for word in profane_words]


@click.command()
@click.pass_context
@click.argument("source", type=click.Path(exists=True))
@click.version_option(__version__)
def jonahlint_cli(ctx: click.Context, source: Union[str, Path]):
    inner_sources = SourcesFinder.find_sources(Path(source))
    profanity_checker = ProfanityChecker(get_profane_words())
    reports_dict = {
        source: ProfanityAnalyzer.analyze_file(
            path=source, profanity_checker=profanity_checker
        ) for source in inner_sources
    }
    reports_dict = {
        source: reports for source, reports in reports_dict.items() if len(reports) != 0
    }
    if len(reports_dict) == 0:
        return
    for source, reports in reports_dict.items():
        for report in reports:
            click.echo(
                f"{source}:{report.line_number}: {report.error_id}: {report.message}"
            )
    ctx.exit(1)
