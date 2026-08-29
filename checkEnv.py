import os
import time
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


def log(msg):
    print("[checkEnv {}] {}".format(time.strftime("%H:%M:%S"), msg), flush=True)


def run(cmd, timeout=None):
    """执行命令并返回(返回码, 合并输出)，统一处理 ~ 路径展开"""
    cmd = os.path.expanduser(cmd) if isinstance(cmd, str) else cmd
    try:
        result = subprocess.run(cmd, shell=isinstance(cmd, str), timeout=timeout,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode("utf-8", errors="replace")
        return result.returncode, output
    except subprocess.TimeoutExpired:
        return 124, "命令超时: {}".format(cmd)
    except OSError as e:
        return 1, str(e)


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
        log("未检测到 Miniconda，开始安装(过程中前台可能长时间无输出，请耐心等待)")
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


def checkBCL2Fq():
    _, output = run([CONDA_BIN, "run", "-n", ENV_NAME, "bcl2fastq", "-v"])
    print(output)
    if "Illumina" in output:
        log("### bcl2fastq ready ###")
        return output
    log("未安装bcl2fastq，开始安装")
    updateCondaMirror()
    runner = MAMBA_BIN if os.path.isfile(MAMBA_BIN) else CONDA_BIN
    code, output = run([runner, "install", "-n", ENV_NAME, "-c", "dranew",
                        "bcl2fastq", "-y"], timeout=3600)
    if code != 0:
        log("错误: bcl2fastq 安装失败:\n" + output)


def checkCRISPResso2():
    code, _ = run([CONDA_BIN, "run", "-n", ENV_NAME, "CRISPResso", "--help"])
    if code == 0:
        log("### CRISPResso ready ###")
        log(time.ctime())
        return 0
    log("未安装CRISPResso，开始安装")
    updateCondaMirror()
    run([CONDA_BIN, "config", "--add", "channels", "bioconda"])
    run([CONDA_BIN, "config", "--add", "channels", "conda-forge"])
    runner = MAMBA_BIN if os.path.isfile(MAMBA_BIN) else CONDA_BIN
    code, output = run([runner, "install", "-n", ENV_NAME, "-c", "bioconda",
                        "CRISPResso2", "-y"], timeout=7200)
    if code != 0:
        log("错误: CRISPResso2 安装失败:\n" + output)
    log(time.ctime())


def check():
    if not checkConda():
        return
    checkBCL2Fq()
    checkCRISPResso2()


if __name__ == "__main__":
    check()
