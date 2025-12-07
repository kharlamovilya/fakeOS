import sys
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from os_sim.cli.main import main


if __name__ == "__main__":
    main()
