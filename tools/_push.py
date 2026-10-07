#!/usr/bin/env python3
# 用 dulwich 提交并推送到 GitHub（绕过损坏的 git CLI）。token 仅运行时从 keychain 读取，不落盘。
import os, subprocess, glob
from dulwich.repo import Repo
from dulwich import porcelain

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER = "leo-bone"
REPO = "HowToInvestBetter"

def get_token():
    return subprocess.run(["security", "find-internet-password", "-w", "-s", "github.com"],
                         capture_output=True, text=True).stdout.strip()

def main():
    token = get_token()
    if not token:
        print("ERROR: 无法读取 github 凭证"); return 1

    repo = Repo(HERE)
    # 设默认分支为 main
    repo.refs.set_symref(b"HEAD", b"refs/heads/main")

    # 暂存所有非 .git 文件
    files = []
    for f in glob.glob(os.path.join(HERE, "**"), recursive=True):
        if os.path.isfile(f) and ".git" not in f.split(os.sep):
            rel = os.path.relpath(f, HERE)
            files.append(rel)
    # dulwich add 需要字节路径
    porcelain.add(repo, files)
    print(f"[ok] 已暂存 {len(files)} 个文件")

    # 提交
    msg = ("内容做细：扩充薄弱章节(01/02/04/08/09) + 新增4个细分专题章(21基金选择/22固收/"
           "23全球ETF/24衍生品杠杆)，总量 234→302 条；补齐 EPUB/PDF/lint；对标 HowToLiveBetter")
    porcelain.commit(repo, message=msg.encode("utf-8"),
                    author=b"leo-bone <57990177@qq.com>",
                    committer=b"leo-bone <57990177@qq.com>")
    print("[ok] 已提交")

    # 推送
    url = f"https://{OWNER}:{token}@github.com/{OWNER}/{REPO}.git"
    try:
        result = porcelain.push(repo, remote_location=url,
                               refspecs=[b"refs/heads/main:refs/heads/main"])
        print("[ok] 推送结果:", result)
    except Exception as e:
        print("[ERROR] 推送失败:", repr(e))
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
