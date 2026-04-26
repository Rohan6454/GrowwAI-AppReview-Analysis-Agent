import pytest
from agent.cli import build_parser


def test_cli_parser_ingest():
    parser = build_parser()
    args = parser.parse_args(['ingest', '--source', 'google_play', '--input', 'test.csv'])
    assert args.command == 'ingest'
    assert args.source == 'google_play'
    assert args.input == 'test.csv'


def test_cli_parser_clean():
    parser = build_parser()
    args = parser.parse_args(['clean', '--db', 'data/reviews.db'])
    assert args.command == 'clean'
    assert args.db == 'data/reviews.db'


def test_cli_parser_cluster():
    parser = build_parser()
    args = parser.parse_args(['cluster', '--db', 'data/reviews.db'])
    assert args.command == 'cluster'
    assert args.db == 'data/reviews.db'


def test_cli_parser_report():
    parser = build_parser()
    args = parser.parse_args(['report', '--db', 'data/reviews.db'])
    assert args.command == 'report'
    assert args.db == 'data/reviews.db'


def test_cli_parser_email():
    parser = build_parser()
    args = parser.parse_args(['email', '--db', 'data/reviews.db'])
    assert args.command == 'email'
    assert args.db == 'data/reviews.db'
