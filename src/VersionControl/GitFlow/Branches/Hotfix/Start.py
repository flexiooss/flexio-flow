from pathlib import Path
import shlex, subprocess
import os
import shutil



class Start:
    def __init__(self):
        pass

    @staticmethod
    def process(dir_path: Path):
        workdir: Path = Path('/tmp/flexio_flow_tests')
        shutil.rmtree(workdir)
        workdir.mkdir()

        print(workdir.as_posix())

        subprocess.Popen(["pwd"])
        os.chdir(workdir)
        # subprocess.Popen(["cd", workdir.as_posix()])
        subprocess.Popen(["pwd"])
        subprocess.Popen(["git", "flow", "init"])
