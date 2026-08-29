"""版本检查后台线程与判定逻辑，避免 conda run 启动耗时阻塞界面

判定原则: 以命令退出码为准, 输出内容仅用于提取版本号做展示;
新旧版本输出格式不同(CRISPResso2 新版 --version 无方括号), 不能依赖固定子串判断
"""
import os
import re
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal


def _tail(text, lines=5):
    """取输出末尾的非空行，用于失败时展示原因"""
    ls = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n".join(ls[-lines:]) if ls else "(无输出)"


def parse_bcl2fastq(rc, text):
    """bcl2fastq -v 的版本信息在 stderr；返回 (是否可用, 版本显示, 失败原因)"""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    ver_line = next((l for l in lines if l.lower().startswith("bcl2fastq")), None)
    if rc == 0 and ("Illumina" in text or ver_line):
        return True, ver_line or "bcl2fastq", ""
    return False, "未安装", "bcl2fastq 不可用(退出码 {0})，命令输出末尾:\n{1}".format(rc, _tail(text))


def parse_crispresso(rc, text):
    """CRISPResso --version 输出格式随版本变化，按退出码+版本号正则判定"""
    m = re.search(r"CRISPResso\D*(\d[\w.\-]*)", text, re.I)
    if rc == 0 and ("[CRISPResso" in text or m):
        return True, "CRISPResso " + (m.group(1) if m else "未知版本"), ""
    if rc == 0 and "CRISPResso" in text:
        return True, "CRISPResso (版本号未识别)", ""
    return False, "未安装", "CRISPResso 不可用(退出码 {0})，命令输出末尾:\n{1}".format(rc, _tail(text))


PARSERS = {"bcl2fastq": parse_bcl2fastq, "crispresso": parse_crispresso}


class VersionCheckThread(QThread):
    ready = pyqtSignal(bool, str, str)   # (是否可用, 版本显示文本, 失败原因)

    def __init__(self, cmd, kind, parent=None):
        """kind: 'bcl2fastq' 或 'crispresso'，决定用哪个解析器"""
        self.cmd = os.path.expanduser(cmd)
        self.kind = kind
        super().__init__(parent)

    def run(self):
        try:
            proc = subprocess.Popen(self.cmd, shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            raw = proc.stdout.read().decode("utf-8", errors="replace")
            rc = proc.wait()
        except OSError as e:
            rc, raw = 1, str(e)
        print(raw, flush=True)
        ok, display, reason = PARSERS[self.kind](rc, raw)
        self.ready.emit(ok, display, reason)
