import argparse
from pathlib import Path

from app.ml.training import train_models


def main() -> None:
    parser = argparse.ArgumentParser(description="Train repository quality prediction models.")
    parser.add_argument("--input", type=Path, help="Optional labeled CSV training dataset")
    parser.add_argument("--output", type=Path, default=Path("./models"))
    args = parser.parse_args()
    print(train_models(args.output, args.input))


if __name__ == "__main__":
    main()

