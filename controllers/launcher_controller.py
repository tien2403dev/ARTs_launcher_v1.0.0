from PyQt5.QtCore import QTimer

from services.update_service import UpdateService


class LauncherController:
    def __init__(self, window):
        self.window = window
        self.service = UpdateService()

    def start(self):
        self.window.show()

        QTimer.singleShot(
            300,
            self.run
        )

    def run(self):
        try:
            self.service.write_log("Launcher started")
            self.service.validate_server()

            server_ver, local_ver = self.service.get_versions()

            self.service.write_log(f"Server version: {server_ver}")
            self.service.write_log(f"Local version: {local_ver}")

            if self.service.need_update():
                if self.service.is_core_running():
                    self.window.set_error(
                        "ARTs App đang mở.\n"
                        "Vui lòng đóng app rồi mở lại ARTs_App.exe."
                    )
                    return

                self.window.set_status(
                    f"Đang cập nhật phiên bản {server_ver}..."
                )

                self.service.copy_package()

                self.window.set_done(
                    "Cập nhật hoàn tất. Đang mở ứng dụng..."
                )

            else:
                self.window.set_status(
                    "Phiên bản đã mới nhất. Đang mở ứng dụng..."
                )

            self.service.start_core_app()
            self.service.write_log("Core app started")

            QTimer.singleShot(
                800,
                self.window.close
            )

        except Exception as e:
            self.service.log_exception()

            self.window.set_error(
                "Không thể mở ARTs App.\n\n"
                f"Lỗi: {e}\n\n"
                f"Log:\n{self.service.log_file}"
            )