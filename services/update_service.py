import os
import sys
import subprocess
import traceback
from datetime import datetime
from pathlib import Path


APP_NAME = "ARTs_App"
LOCAL_FOLDER_NAME = "ARTs_App"
CORE_EXE_NAME = "ARTs_Core.exe"


class UpdateService:
    def __init__(self):
        self.server_root = self.get_server_root()

        self.server_package = self.server_root / "package"
        self.server_version = self.server_package / "version.txt"
        self.server_db = self.server_root / "database" / "app.db"

        self.local_root = Path(os.environ["LOCALAPPDATA"]) / LOCAL_FOLDER_NAME
        self.local_version = self.local_root / "version.txt"
        self.local_exe = self.local_root / CORE_EXE_NAME

        # self.log_file = self.local_root / "logs" / "launcher.log"
        self.server_logs = self.server_root / "logs"
        self.log_file = self.server_logs / "launcher.log"

    def get_server_root(self):
        if getattr(sys, "frozen", False):
            return Path(sys.executable).parent

        return Path(__file__).resolve().parents[1]

    def write_log(self, message):
        try:
            self.log_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"{message}\n"
                )
        except Exception:
            pass

    def read_text(self, path):
        try:
            if path.exists():
                return path.read_text(encoding="utf-8").strip()
        except Exception:
            pass

        return ""

    # def validate_server(self):
    #     if not self.server_package.exists():
    #         raise FileNotFoundError(
    #             f"Không tìm thấy thư mục package:\n{self.server_package}"
    #         )
    #
    #     if not self.server_version.exists():
    #         raise FileNotFoundError(
    #             f"Không tìm thấy file version.txt:\n{self.server_version}"
    #         )
    #
    #     if not self.server_db.exists():
    #         raise FileNotFoundError(
    #             f"Không tìm thấy database:\n{self.server_db}"
    #         )
    def validate_server(self):
        if not self.server_package.exists():
            raise FileNotFoundError(
                f"Không tìm thấy thư mục package:\n{self.server_package}"
            )

        if not self.server_version.exists():
            raise FileNotFoundError(
                f"Không tìm thấy file version.txt:\n{self.server_version}"
            )

        self.server_db.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def get_versions(self):
        server_ver = self.read_text(self.server_version)
        local_ver = self.read_text(self.local_version)

        return server_ver, local_ver

    def need_update(self):
        server_ver, local_ver = self.get_versions()

        return (
            server_ver != local_ver
            or not self.local_exe.exists()
        )

    def is_core_running(self):
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {CORE_EXE_NAME}"],
            capture_output=True,
            text=True,
            shell=False
        )

        return CORE_EXE_NAME.lower() in result.stdout.lower()

    def copy_package(self):
        self.local_root.mkdir(
            parents=True,
            exist_ok=True
        )

        cmd = [
            "robocopy",
            str(self.server_package),
            str(self.local_root),
            "/MIR",
            "/R:2",
            "/W:1",
            "/NFL",
            "/NDL",
            "/NJH",
            "/NJS",
            "/NP",
        ]

        self.write_log("Run robocopy: " + " ".join(cmd))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=False
        )

        self.write_log(f"Robocopy return code: {result.returncode}")

        if result.stdout:
            self.write_log(result.stdout)

        if result.stderr:
            self.write_log(result.stderr)

        if result.returncode >= 8:
            raise RuntimeError(
                f"Copy app thất bại. Robocopy code: {result.returncode}"
            )

    def start_core_app(self):
        if not self.local_exe.exists():
            raise FileNotFoundError(
                f"Không tìm thấy file chạy app:\n{self.local_exe}"
            )

        env = os.environ.copy()
        env["ARTS_DB_PATH"] = str(self.server_db)
        env["ARTS_SERVER_ROOT"] = str(self.server_root)

        subprocess.Popen(
            [str(self.local_exe)],
            env=env,
            cwd=str(self.local_root)
        )

    def log_exception(self):
        self.write_log(traceback.format_exc())
