import argparse
import sys
from agent import db


def build_parser():
    parser = argparse.ArgumentParser(
        description='App Review Insights Analyzer CLI'
    )
    subparsers = parser.add_subparsers(dest='command')

    ingest = subparsers.add_parser('ingest', help='Ingest reviews from a source')
    ingest.add_argument('--source', required=True, help='Source name (google_play, app_store, csv)')
    ingest.add_argument('--input', required=True, help='Input file path or source identifier')

    clean = subparsers.add_parser('clean', help='Clean and normalize ingested review data')
    clean.add_argument('--db', required=True, help='Path to the SQLite database')

    cluster = subparsers.add_parser('cluster', help='Cluster cleaned reviews into themes')
    cluster.add_argument('--db', required=True, help='Path to the SQLite database')

    report = subparsers.add_parser('report', help='Generate an executive report')
    report.add_argument('--db', required=True, help='Path to the SQLite database')

    email = subparsers.add_parser('email', help='Generate an email draft')
    email.add_argument('--db', required=True, help='Path to the SQLite database')

    init = subparsers.add_parser('init-db', help='Initialize the database schema')
    init.add_argument('--db', required=True, help='Path to the SQLite database')

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == 'ingest':
        print(f'Ingesting from {args.source} using {args.input}')
    elif args.command == 'clean':
        print(f'Cleaning database: {args.db}')
    elif args.command == 'cluster':
        print(f'Clustering reviews in database: {args.db}')
    elif args.command == 'report':
        print(f'Generating report using database: {args.db}')
    elif args.command == 'email':
        print(f'Generating email draft using database: {args.db}')
    elif args.command == 'init-db':
        db.init_db(args.db)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
