import os
import time
import subprocess
def checkConda():
    condaInfo = os.popen(" ~/miniconda3/bin/conda info")
    if "conda version" in condaInfo.read():
        print("### Conda ready ###")
    else:
        installer = str(time.time())
        with open(installer,"w") as f:
            f.write("""#!/bin/bash
rm -rf /tmp/miniconda.sh*
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
bash /tmp/miniconda.sh -b -f
            """)
        os.system("bash ./" + installer)
        os.system("rm -rf " + installer)
        print("done")
        print(time.ctime())

def updateCondaMirror():
    with open(os.environ["HOME"]+"/.condarc","w") as f:
        f.write("""channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud""")
        os.system(" ~/miniconda3/bin/conda clean -i -y")

def checkBCL2Fq():
    bclInfo = subprocess.Popen(['~/miniconda3/bin/conda run bcl2fastq -v'],shell=True,stderr=subprocess.PIPE)
    verion = str(bclInfo.stderr.read())
    print(verion)
    if "Illumina" in verion:
        print("### bcl2fastq ready ###")
        return verion

    else:
        print("未安装bcl2fastq")
        updateCondaMirror()
        print("开始安装")
        os.system(" ~/miniconda3/bin/conda install -c dranew bcl2fastq -y")

def checkCRISPResso2():
    info = os.system(" ~/miniconda3/bin/conda run CRISPResso --help")
    print(info)
    if info == 0:
        print("### CRISPResso ready ###")
        print(time.ctime())
        return 0

    else:
        print("未安装CRISPResso")
        updateCondaMirror()
        print("开始安装")
        os.system(" ~/miniconda3/bin/conda  config --add channels bioconda")
        os.system(" ~/miniconda3/bin/conda  config --add channels conda-forge")
        os.system(" ~/miniconda3/bin/conda install -c bioconda CRISPResso2 -y")
        print(time.ctime())

def check():
    checkConda()
    checkBCL2Fq()
    checkCRISPResso2()

if __name__ == "__main__":
    # updateCondaMirror()
    check()
