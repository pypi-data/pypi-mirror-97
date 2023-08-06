import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, NoReturn

from appdirs import user_config_dir

import pypk


def load_custom_config(path: Path) -> Dict[str, str]:
    config = json.loads(path.read_text())
    if not isinstance(config, dict):
        raise ValueError("the config object must be a flat dictionary")
    return config


def try_load_default_config() -> Dict[str, str]:
    config_path = Path(user_config_dir("pypk", "Pyrite AI")).joinpath("config.json")
    try:
        config = json.loads(config_path.read_text())
    except FileNotFoundError:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w") as f:
            json.dump({}, f)
        return {}
    except (OSError, json.decoder.JSONDecodeError):
        print("[Warning] failed to read default config file: invalid JSON")
        return {}
    else:
        return config


def exit_with_status(msg: str, code: int = 1) -> NoReturn:
    print(msg, file=sys.stderr)
    sys.exit(code)


def main():
    parser = ArgumentParser()
    parser.add_argument("package", help="Path to root package directory")
    parser.add_argument("-c", "--config", help="Path to config file")
    parser.add_argument("-a", "--author", help="Author's name")
    parser.add_argument("-e", "--email", help="Author's email")
    parser.add_argument("-v", "--version", default="3.6.0", help="Minimum Python version supported")

    args = parser.parse_args()

    try:
        if args.config is not None:
            config = load_custom_config(Path(args.config))
        else:
            config = try_load_default_config()
    except Exception as e:
        exit_with_status(f"Failed to load config: '{e}'")

    author = args.author if args.author else config.get("author")
    email = args.email if args.email else config.get("email")
    version = args.version if args.version else config.get("version")

    if author is None:
        exit_with_status("[Error] 'author' must be specified in either the config or via command line")
    if email is None:
        exit_with_status("[Error] 'email' must be specified in either the config or via command line")
    if version is None:
        exit_with_status("[Error] 'version' must be specified in either the config or via command line")

    pypk.create(Path(args.package), author, email, version)


if __name__ == "__main__":
    main()
