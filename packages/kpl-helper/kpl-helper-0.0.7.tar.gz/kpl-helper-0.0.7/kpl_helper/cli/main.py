import argparse
from kpl_helper.save import save_model, save_dataset


def main():
    parser = argparse.ArgumentParser(prog="khelper")
    sub = parser.add_subparsers(title="khelper sub command")

    save = sub.add_parser("save")
    save_sub = save.add_subparsers(title="Content")

    parser.set_defaults(func=lambda x: parser.print_help())
    save.set_defaults(func=lambda x: save.print_help())

    d = save_sub.add_parser("dataset")
    d.set_defaults(func=_save_dataset)
    d.add_argument("--name", "-n", help="Set the dataset name", required=True)
    d.add_argument("--desc", "-d", help="Description for the dataset", required=False)
    d.add_argument("--path", "-p", help="Path to dataset", required=True)
    d.add_argument("--as_serialized", "-s", action='store_true', help='upload as kpl-dataset format dataset')

    p = save_sub.add_parser("model")
    p.set_defaults(func=_save_model)
    p.add_argument("--name", "-n", help="Set the model name", required=True)
    p.add_argument("--desc", "-d", help="Description for the dataset", required=False)
    p.add_argument("--path", "-p", help="Path to model", required=True)

    args = parser.parse_args()
    args.func(args)


def _save_model(args):
    save_model(args.path, args.name, args.desc)


def _save_dataset(args):
    save_dataset(args.path, args.name, args.desc, args.as_serialized)


if __name__ == "__main__":
    main()
