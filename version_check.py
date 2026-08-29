"""版本检查后台线程，避免 conda run 启动耗时阻塞界面"""
import os
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal


class VersionCheckThread(QThread):
    ready = pyqtSignal(str)

    def __init__(self, cmd, capture="stdout", parent=None):
        """capture: 'stdout' 读取标准输出；'stderr' 读取标准错误（如 bcl2fastq -v）"""
        self.cmd = os.path.expanduser(cmd)
        self.capture = capture
        super().__init__(parent)

    def run(self):
        try:
            if self.capture == "stderr":
                proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.PIPE)
                data = proc.stderr.read()
            else:
                proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL)
                data = proc.stdout.read()
        except OSError:
            data = b""
        self.ready.emit(data.decode("utf-8", errors="replace"))
