from argparse import ArgumentParser, BooleanOptionalAction

from src import angel


def parse_args():
    parser = ArgumentParser(description="Shoulder Angel")
    parser.add_argument("--config_path", default="./config/config.yaml",
                        help="Path to config yaml file")
    parser.add_argument("--run_rule", default="single",
                        help="Rule when the app should shout down.\n"
                             "Options:\n"
                             "'single' -app will quit after one check\n"
                             "'loop' -app will keep checking periodically\n")
    parser.add_argument("--check_interval", default=5,
                        type=float,
                        help="Minutes between checks (applicable when looping)")
    parser.add_argument("--debug", default=False,
                        action=BooleanOptionalAction,
                        help="Set logger level to debug")

    arguments = parser.parse_args()

    return arguments


if __name__ == "__main__":
    args = parse_args()
    angel.Angel(args).run()
