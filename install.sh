#!/usr/bin/env bash
# ============================================================
# NGS_Tools 一键安装/更新脚本
#
# 用法(任选其一):
#   bash <(curl -sL https://gitee.com/MasterChiefm/NGS_Tools/raw/master/install.sh)
#   git clone 本仓库后: bash install.sh
#
# 功能:
#   1. 自动获取最新版本号与安装包(优先 gitee, 失败自动切换 GitHub)
#   2. 安装到 ~/.ngs_tools (已安装则覆盖升级, 分析环境不受影响)
#   3. 赋予可执行权限, 创建应用菜单 .desktop 入口
#
# 可选环境变量:
#   GITEE_TOKEN   gitee 私人令牌(公开仓库无需提供)
#   PREFIX        安装目录, 默认 ~/.ngs_tools
# ============================================================
set -u -o pipefail

GITEE_REPO="${GITEE_REPO:-MasterChiefm/NGS_Tools}"
GITHUB_REPO="${GITHUB_REPO:-Masterchiefm/NGS_Tools}"
INSTALL_DIR="${PREFIX:-$HOME/.ngs_tools}"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/ngs_tools.desktop"
GITEE_API="${GITEE_API:-https://gitee.com/api/v5}"
GITHUB_API="${GITHUB_API:-https://api.github.com}"
GITHUB_PROXY="${GITHUB_PROXY:-https://gh-proxy.com/}"   # GitHub 直连失败时的加速前缀, 置空可禁用
GITEE_TOKEN="${GITEE_TOKEN:-}"

log() { echo "[NGS_Tools $(date +%H:%M:%S)] $*"; }
fail() { echo "[错误] $*" >&2; exit 1; }

command -v curl >/dev/null 2>&1 || fail "缺少 curl, 请先安装 (sudo apt install curl)"
command -v tar  >/dev/null 2>&1 || fail "缺少 tar"

http() { curl -fsSL --connect-timeout 10 --max-time 60 "$1"; }
download() { curl -sS -L --connect-timeout 15 --max-time 1800 --retry 3 -o "$2" "$1"; }

# ------------------------------------------------------------
# 1. 获取最新版本信息, 优先 gitee
# ------------------------------------------------------------
tag=""; asset_url=""; source=""

get_gitee() {
    local url="$GITEE_API/repos/$GITEE_REPO/releases/latest"
    [ -n "$GITEE_TOKEN" ] && url="$url?access_token=$GITEE_TOKEN"
    local json
    json=$(http "$url") || return 1
    tag=$(printf '%s' "$json" | grep -o '"tag_name"[^,]*' | head -1 | sed 's/.*:\s*"\(.*\)"/\1/')
    asset_url=$(printf '%s' "$json" | grep -o '"browser_download_url"[^,}]*' |
                grep 'NGS_Tools.*\.tar\.gz' | head -1 | sed 's/.*:\s*"\([^"]*\)"/\1/')
    [ -n "$tag" ] && [ -n "$asset_url" ]
}

get_github() {
    local json
    json=$(http "$GITHUB_API/repos/$GITHUB_REPO/releases/latest") || return 1
    tag=$(printf '%s' "$json" | grep -o '"tag_name"[^,]*' | head -1 | sed 's/.*:\s*"\(.*\)"/\1/')
    asset_url=$(printf '%s' "$json" | grep -o '"browser_download_url"[^,}]*' |
                grep 'NGS_Tools.*\.tar\.gz' | head -1 | sed 's/.*:\s*"\([^"]*\)"/\1/')
    [ -n "$tag" ] && [ -n "$asset_url" ]
}

log "查询最新版本..."
if get_gitee; then
    source="gitee"
else
    log "gitee 查询失败, 尝试 GitHub..."
    get_github || fail "无法从 gitee 与 GitHub 获取版本信息, 请检查网络"
    source="github"
fi
log "最新版本: $tag (来自 $source)"

# ------------------------------------------------------------
# 2. 下载安装包, gitee 优先, github 直连/加速双保险
# ------------------------------------------------------------
workdir=$(mktemp -d) || fail "无法创建临时目录"
trap 'rm -rf "$workdir"' EXIT
archive="$workdir/NGS_Tools.tar.gz"

download_asset() {
    local url="$1"
    download "$url" "$archive" || return 1
    [ "$(stat -c%s "$archive" 2>/dev/null || echo 0)" -gt 10485760 ]
}

log "开始下载安装包(约 100MB, 请耐心等待)..."
if [ "$source" = "gitee" ]; then
    download_asset "$asset_url" || { log "gitee 下载失败, 尝试 GitHub..."; source="github"; }
fi
if [ "$source" = "github" ]; then
    if [ -n "$GITHUB_PROXY" ]; then
        download_asset "${GITHUB_PROXY}${asset_url}" || download_asset "$asset_url" || fail "安装包下载失败, 请检查网络后重试"
    else
        download_asset "$asset_url" || fail "安装包下载失败, 请检查网络后重试"
    fi
fi
log "下载完成 ($(du -h "$archive" | cut -f1))"

old_version=""
[ -f "$INSTALL_DIR/VERSION" ] && old_version=$(cat "$INSTALL_DIR/VERSION")

# ------------------------------------------------------------
# 3. 覆盖安装到 ~/.ngs_tools
# ------------------------------------------------------------
log "解压并安装到 $INSTALL_DIR ..."
tar -xzf "$archive" -C "$workdir" || fail "安装包解压失败"
[ -f "$workdir/NGS_Tools/NGS_Tools" ] || fail "安装包内容异常, 缺少主程序"
mkdir -p "$INSTALL_DIR"
cp -rf "$workdir/NGS_Tools/." "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/NGS_Tools"
echo "$tag" > "$INSTALL_DIR/VERSION"

# 补充图标(安装包内未包含, 下载失败不影响使用)
if [ ! -f "$INSTALL_DIR/icon.ico" ]; then
    download "https://gitee.com/$GITEE_REPO/raw/master/icon.ico" "$INSTALL_DIR/icon.ico" 2>/dev/null ||
    download "${GITHUB_PROXY}https://raw.githubusercontent.com/$GITHUB_REPO/master/icon.ico" "$INSTALL_DIR/icon.ico" 2>/dev/null ||
    rm -f "$INSTALL_DIR/icon.ico"
fi

# ------------------------------------------------------------
# 4. 创建应用菜单入口
# ------------------------------------------------------------
mkdir -p "$DESKTOP_DIR"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=NGS_Tools
Comment=NGS 小工具箱 — 基因编辑效果分析
Exec=$INSTALL_DIR/NGS_Tools
Path=$INSTALL_DIR
Icon=$INSTALL_DIR/icon.ico
Terminal=false
Categories=Science;Biology;Qt;
StartupNotify=true
EOF
chmod 644 "$DESKTOP_FILE"
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$DESKTOP_DIR" 2>/dev/null
command -v gio >/dev/null 2>&1 && gio set "$DESKTOP_FILE" metadata::trusted true 2>/dev/null

if [ -n "$old_version" ]; then
    if [ "$old_version" = "$tag" ]; then
        log "已重新安装当前版本 $tag (覆盖安装)"
    else
        log "升级完成: $old_version -> $tag"
    fi
else
    log "全新安装完成"
fi
log "  程序目录 : $INSTALL_DIR"
log "  版本     : $tag"
log "  菜单入口 : 应用列表中的 \"NGS_Tools\" ($DESKTOP_FILE)"
log "  也可直接运行: $INSTALL_DIR/NGS_Tools"
log "首次使用请在程序内点击\"安装分析环境\"以部署 conda 分析环境"
