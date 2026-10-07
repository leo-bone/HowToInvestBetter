#!/usr/bin/env python3
# 清理临时脚本 + 重命名同步工具 + 重新提交干净版本（纯本地，无需凭据）
import os, ctypes, glob, shutil

libc = ctypes.CDLL(None)
def _raw_mkdir(path, mode=0o777):
    if isinstance(path, str): path = path.encode("utf-8")
    libc.mkdir(path, mode & 0o777)
def _raw_makedirs(name, mode=0o777, exist_ok=False):
    if isinstance(name, str): name = name.encode("utf-8")
    try: libc.mkdir(name, mode & 0o777)
    except OSError:
        if not exist_ok: raise
os.mkdir = _raw_mkdir
os.makedirs = _raw_makedirs

from dulwich.repo import Repo
from dulwich import porcelain

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    # 1) 删除临时脚本
    for tmp in ["tools/_commit.py", "tools/_github_setup.py"]:
        p = os.path.join(HERE, tmp)
        if os.path.exists(p):
            os.remove(p); print("[ok] 删除", tmp, flush=True)
    # 2) 重命名同步工具
    old = os.path.join(HERE, "tools/_push2.py")
    new = os.path.join(HERE, "tools/sync.py")
    if os.path.exists(old):
        shutil.move(old, new); print("[ok] 重命名 _push2.py -> sync.py", flush=True)

    # 3) 清空索引并重新暂存所有现存文件（自然排除已删除的）
    repo = Repo(HERE)
    idx = repo.open_index()
    idx.clear()
    idx.write()

    files = []
    for f in glob.glob(os.path.join(HERE, "**"), recursive=True):
        if os.path.isfile(f) and ".git" not in f.split(os.sep):
            files.append(os.path.relpath(f, HERE))
    porcelain.add(repo, files)
    print(f"[ok] 已暂存 {len(files)} 个文件", flush=True)

    msg = ("清理临时脚本（_commit/_github_setup），保留 sync.py 作为同步工具；内容同上一版（302条/24章）"
           if False else
           "清理临时脚本，保留 sync.py 同步工具；正文与产物保持不变（302条/24章，含EPUB/PDF/lint）")
    porcelain.commit(repo, message=msg.encode("utf-8"),
                    author=b"leo-bone <57990177@qq.com>",
                    committer=b"leo-bone <57990177@qq.com>")
    print("[ok] 干净版本已提交", flush=True)

if __name__ == "__main__":
    main()
