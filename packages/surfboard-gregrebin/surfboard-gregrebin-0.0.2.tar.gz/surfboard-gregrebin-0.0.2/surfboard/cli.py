from surfboard.app import Application, FilterParams
from argparse import ArgumentParser


def auto_filter_params(original_func):
    """ From a function that accepts app, args and filter_params returns a function that accepts only app and args,
    meanwhile filter_params is derived from args """
    def decorated_func(app: Application, args):
        filter_params = FilterParams(
            number=args.number_filter, keyword=args.keyword_filter, group=args.group_filter, skill=args.skill,
            category=args.category)
        original_func(app, args, filter_params)
    return decorated_func


def run_cli():
    app: Application = Application()

    main_parser = ArgumentParser()
    main_parser.add_argument("file")
    main_parser.add_argument("-n", "--number_filter", type=int)
    main_parser.add_argument("-k", "--keyword_filter")
    main_parser.add_argument("-g", "--group_filter")
    main_parser.add_argument("-s", "--skill")
    main_parser.add_argument("-c", "--category")
    main_parser.set_defaults(func=open_cli)

    subparsers = main_parser.add_subparsers()

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=list_cli)

    group_parser = subparsers.add_parser("group")
    group_parser.add_argument("group_name")
    group_parser.add_argument("-f", "--force", action="store_true")
    group_parser.add_argument("-r", "--rewrite", action="store_true")
    group_parser.set_defaults(func=group_cli)

    list_group_parser = subparsers.add_parser("list_group")
    list_group_parser.set_defaults(func=list_group_cli)

    count_parser = subparsers.add_parser("count")
    count_parser.add_argument("count_param")
    count_parser.set_defaults(func=count_cli)

    args = main_parser.parse_args()
    args.func(app, args)


def open_cli(app: Application, args):
    try:
        app.open(args.file)
    except FileNotFoundError:
        app.load()
        app.save(args.file)


@auto_filter_params
def list_cli(app: Application, args, filter_params):
    open_cli(app, args)
    for project in app.list(filter_params):
        print(project)


@auto_filter_params
def group_cli(app: Application, args, filter_params):
    open_cli(app, args)
    app.group_multi(args.group_name, args.force, args.rewrite, filter_params)
    app.save(args.file)


@auto_filter_params
def list_group_cli(app: Application, args, filter_params):
    open_cli(app, args)
    for project in app.list(filter_params):
        print(project)
        group = input("Project group:")
        app.group_single(group, project.number)
    app.save(args.file)


@auto_filter_params
def count_cli(app: Application, args, filter_params):
    open_cli(app, args)
    for entry in app.count(args.count_param, filter_params):
        print(entry)
