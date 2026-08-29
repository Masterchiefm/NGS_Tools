import os
import re
import time
import select
import subprocess

CONDA_HOME = os.path.join(os.environ["HOME"], "miniconda3")
CONDA_BIN = os.path.join(CONDA_HOME, "bin", "conda")
MAMBA_BIN = os.path.join(CONDA_HOME, "bin", "mamba")
ENV_NAME = "NGS"
PYTHON_VERSION = "3.9"

# anaconda 镜像按优先级排列，探测失败自动切换到下一个
# 注意：阿里云目前尚未同步 anaconda 仓库（路径 404），探测会自动跳过；
#      中科大源会重定向至南京大学镜像，两者均保留作为备用
ANACONDA_MIRRORS = [
    ("北京大学", "https://mirrors.pku.edu.cn/anaconda"),
    ("上海交通大学", "https://mirror.sjtu.edu.cn/anaconda"),
    ("中国科学技术大学", "https://mirrors.ustc.edu.cn/anaconda"),
    ("南京大学", "https://mirrors.nju.edu.cn/anaconda"),
    ("阿里云", "https://mirrors.aliyun.com/anaconda"),
]
# 官方源，仅在所有镜像都不可用时作为最后手段
OFFICIAL_MINICONDA_URL = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
PROBE_PATH = "/pkgs/main/linux-64/repodata.json"

# 实时输出回调，GUI 通过 set_progress_callback 注册；未注册时仅打印到控制台
_progress_callback = None

# 最近一次 check() 的汇总结果，供安装对话框展示
LAST_SUMMARY = []   # 每个组件一行结论
LAST_FAILED = []    # 异常组件名列表


def set_progress_callback(fn):
    """注册实时输出回调 fn(msg)，传 None 取消"""
    global _progress_callback
    _progress_callback = fn


def _dispatch(msg):
    if _progress_callback:
        try:
            _progress_callback(msg)
        except Exception:
            pass


def log(msg):
    text = "[checkEnv {}] {}".format(time.strftime("%H:%M:%S"), msg)
    print(text, flush=True)
    _dispatch(text)


def log_line(raw):
    """转发子命令的实时输出行"""
    print(raw, flush=True)
    _dispatch(raw)


def run(cmd, timeout=None):
    """执行命令，实时转发输出，返回(返回码, 合并输出)"""
    cmd = os.path.expanduser(cmd) if isinstance(cmd, str) else cmd
    try:
        proc = subprocess.Popen(cmd, shell=isinstance(cmd, str),
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except OSError as e:
        return 1, str(e)
    deadline = time.time() + timeout if timeout else None
    fd = proc.stdout.fileno()
    output = bytearray()
    pending = b""
    while True:
        ready, _, _ = select.select([fd], [], [], 1.0)
        if ready:
            chunk = os.read(fd, 8192)
            if not chunk:
                break
            output.extend(chunk)
            pending += chunk
            *lines, pending = pending.replace(b"\r", b"\n").split(b"\n")
            for line in lines:
                text = line.decode("utf-8", errors="replace").strip()
                if text:
                    log_line(text)
        if deadline and time.time() > deadline:
            proc.kill()
            proc.wait()
            log("命令超时已终止: {}".format(cmd))
            return 124, output.decode("utf-8", errors="replace")
    if pending.strip():
        text = pending.decode("utf-8", errors="replace").strip()
        if text:
            log_line(text)
    code = proc.wait()
    return code, output.decode("utf-8", errors="replace")


def probe(url, timeout=15):
    """用小范围请求探测镜像是否可用，-f 使 curl 在 HTTP 错误时返回非零"""
    code, _ = run(["curl", "-fsSL", "--connect-timeout", "5",
                   "--max-time", str(timeout), "-r", "0-99",
                   "-o", "/dev/null", url])
    return code == 0


def pick_mirror():
    """按优先级探测镜像，返回第一个可用的 (名称, 地址)，全部失败返回 (None, None)"""
    for name, base in ANACONDA_MIRRORS:
        log("探测镜像: {} ({})".format(name, base))
        if probe(base + PROBE_PATH):
            log("镜像可用: {}".format(name))
            return name, base
        log("镜像不可用，尝试下一个")
    return None, None


def download_miniconda(dest):
    """依次从各镜像下载 Miniconda 安装脚本，全部失败时回退官方源"""
    candidates = [(name, base + "/miniconda/Miniconda3-latest-Linux-x86_64.sh")
                  for name, base in ANACONDA_MIRRORS]
    candidates.append(("官方源", OFFICIAL_MINICONDA_URL))
    for name, url in candidates:
        log("从 {} 下载 Miniconda...".format(name))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        code, _ = run(["wget", "-c", "--timeout=30", "--tries=3", "-q",
                       "-O", dest, url], timeout=1800)
        if code == 0 and os.path.isfile(dest) and os.path.getsize(dest) > 10 * 1024 * 1024:
            log("下载完成: {} ({:.1f} MB)".format(name, os.path.getsize(dest) / 1048576))
            return True
        log("从 {} 下载失败".format(name))
    return False


def updateCondaMirror():
    """写入 .condarc，镜像自动切换；全部不可用时保留默认官方源"""
    name, base = pick_mirror()
    condarc = os.path.join(os.environ["HOME"], ".condarc")
    if base:
        with open(condarc, "w") as f:
            f.write("""channels:
  - defaults
show_channel_urls: true
default_channels:
  - {base}/pkgs/main
  - {base}/pkgs/r
  - {base}/pkgs/msys2
custom_channels:
  conda-forge: {base}/cloud
  msys2: {base}/cloud
  bioconda: {base}/cloud
  menpo: {base}/cloud
  pytorch: {base}/cloud
  pytorch-lts: {base}/cloud
  simpleitk: {base}/cloud""".format(base=base))
        log("已切换 conda 镜像到: {}".format(name))
    else:
        log("警告: 所有镜像均不可用，conda 使用官方默认源")
    run([CONDA_BIN, "clean", "-i", "-y"], timeout=300)


def install_miniconda():
    """下载并静默安装 Miniconda"""
    installer = os.path.join(CONDA_HOME, "miniconda.sh")
    if not download_miniconda(installer):
        log("错误: Miniconda 所有下载源均失败，请检查网络后重试")
        return False
    log("开始安装 Miniconda...")
    code, output = run(["bash", installer, "-b", "-u", "-p", CONDA_HOME], timeout=1800)
    os.remove(installer)
    if code != 0:
        log("错误: Miniconda 安装失败:\n" + output)
        return False
    run([CONDA_BIN, "init", "bash"], timeout=120)
    log("Miniconda 安装完成")
    return True


def create_env():
    """创建 NGS 分析环境，优先使用 mamba 加速"""
    log("创建 {} 环境 (python {})...".format(ENV_NAME, PYTHON_VERSION))
    runner = MAMBA_BIN if os.path.isfile(MAMBA_BIN) else CONDA_BIN
    code, output = run([runner, "create", "-n", ENV_NAME,
                        "python={}".format(PYTHON_VERSION), "-y"], timeout=3600)
    if code != 0:
        log("错误: 环境创建失败:\n" + output)
        return False
    log("环境创建完成")
    return True


def install_mamba():
    code, output = run([CONDA_BIN, "install", "conda-forge::mamba", "-y"], timeout=1800)
    if code != 0:
        log("警告: mamba 安装失败(不影响后续流程，将改用 conda):\n" + output)
        return False
    return True


def checkConda():
    if os.path.isfile(CONDA_BIN):
        _, output = run([CONDA_BIN, "info"])
        if "conda version" in output:
            log("### Conda ready ###")
    else:
        log("未检测到 Miniconda，开始安装(下载约需几分钟，进度见实时输出)")
        if not install_miniconda():
            return False

    _, envs = run([CONDA_BIN, "env", "list"])
    if "\n" + ENV_NAME not in envs and ENV_NAME + " " not in envs:
        # 确保 mamba 可用后再建环境
        _, minfo = run([MAMBA_BIN, "info"]) if os.path.isfile(MAMBA_BIN) else (1, "")
        if "mamba version" not in minfo:
            updateCondaMirror()
            install_mamba()
        if not create_env():
            return False
    else:
        log("### 环境 {} 已存在 ###".format(ENV_NAME))

    _, minfo = run([MAMBA_BIN, "info"]) if os.path.isfile(MAMBA_BIN) else (1, "")
    if "mamba version" in minfo:
        log("### mamba ready ###")
    else:
        updateCondaMirror()
        install_mamba()
    return True


def detect_bcl2fastq():
    """返回 (是否可用, 版本描述或失败原因)"""
    code, output = run([CONDA_BIN, "run", "-n", ENV_NAME, "bcl2fastq", "-v"])
    lines = [l.strip() for l in output.splitlines() if l.strip()]
    ver = next((l for l in lines if l.lower().startswith("bcl2fastq")), None)
    if code == 0 and ("Illumina" in output or ver):
        return True, ver or "bcl2fastq"
    return False, "退出码 {0}, 输出末尾: {1}".format(code, lines[-1] if lines else "(无输出)")


def checkBCL2Fq():
    ok, info = detect_bcl2fastq()
    if ok:
        log("### bcl2fastq 就绪: {} ###".format(info))
        return True, info
    log("未检测到 bcl2fastq({}), 开始安装".format(info))
    updateCondaMirror()
    runner = MAMBA_BIN if os.path.isfile(MAMBA_BIN) else CONDA_BIN
    code, output = run([runner, "install", "-n", ENV_NAME, "-c", "dranew",
                        "bcl2fastq", "-y"], timeout=3600)
    ok, info = detect_bcl2fastq()
    if ok:
        log("### bcl2fastq 安装成功: {} ###".format(info))
        return True, info
    tail = "\n".join([l for l in output.splitlines() if l.strip()][-15:])
    log("错误: bcl2fastq 安装失败(退出码 {0})，安装日志末尾:\n{1}".format(code, tail or "(无输出)"))
    return False, info


def detect_crispresso():
    """返回 (是否可用, 版本描述或失败原因)；--version 输出格式随版本变化，用正则提取"""
    code, output = run([CONDA_BIN, "run", "-n", ENV_NAME, "CRISPResso", "--version"])
    m = re.search(r"CRISPResso\D*(\d[\w.\-]*)", output, re.I)
    if code == 0 and ("[CRISPResso" in output or m):
        return True, "CRISPResso " + (m.group(1) if m else "未知版本")
    if code != 0:
        # 老版本 --version 参数不被识别时，用 --help 兜底判断
        code, output = run([CONDA_BIN, "run", "-n", ENV_NAME, "CRISPResso", "--help"])
        if code == 0 and "amplicon" in output.lower():
            return True, "CRISPResso (版本未知)"
    lines = [l for l in output.splitlines() if l.strip()]
    return False, "退出码 {0}, 输出末尾: {1}".format(code, lines[-1] if lines else "(无输出)")


def checkCRISPResso2():
    ok, info = detect_crispresso()
    if ok:
        log("### CRISPResso 就绪: {} ###".format(info))
        log(time.ctime())
        return True, info
    log("未检测到 CRISPResso({}), 开始安装".format(info))
    updateCondaMirror()
    run([CONDA_BIN, "config", "--add", "channels", "bioconda"])
    run([CONDA_BIN, "config", "--add", "channels", "conda-forge"])
    runner = MAMBA_BIN if os.path.isfile(MAMBA_BIN) else CONDA_BIN
    code, output = run([runner, "install", "-n", ENV_NAME, "-c", "bioconda",
                        "CRISPResso2", "-y"], timeout=7200)
    ok, info = detect_crispresso()
    if ok:
        log("### CRISPResso 安装成功: {} ###".format(info))
        log(time.ctime())
        return True, info
    tail = "\n".join([l for l in output.splitlines() if l.strip()][-15:])
    log("错误: CRISPResso2 安装失败(退出码 {0})，安装日志末尾:\n{1}".format(code, tail or "(无输出)"))
    log(time.ctime())
    return False, info


def _summarize(components):
    """输出各组件结论汇总，返回整体是否成功"""
    global LAST_SUMMARY, LAST_FAILED
    LAST_SUMMARY, LAST_FAILED = [], []
    log("=" * 46)
    log("环境检查结果汇总:")
    all_ok = True
    for name, ok, info in components:
        line = "  [{mark}] {name:<14} {info}".format(
            mark="√" if ok else "×", name=name, info=info if ok else "失败(" + info + ")")
        log(line)
        LAST_SUMMARY.append(line)
        if not ok:
            all_ok = False
            LAST_FAILED.append(name)
    log("=" * 46)
    if all_ok:
        log("全部组件就绪，环境可用!")
    else:
        log("异常组件: {}。可关闭窗口后重试；仍失败请把上方日志复制发给维护者。".format(
            ", ".join(LAST_FAILED)))
    return all_ok


def check():
    conda_ok = checkConda()
    if not conda_ok:
        return _summarize([("conda/NGS环境", False, "详见上方日志")])
    bcl_ok, bcl_info = checkBCL2Fq()
    cr_ok, cr_info = checkCRISPResso2()
    return _summarize([
        ("conda/NGS环境", True, "就绪"),
        ("bcl2fastq", bcl_ok, bcl_info),
        ("CRISPResso2", cr_ok, cr_info),
    ])


if __name__ == "__main__":
    check()
