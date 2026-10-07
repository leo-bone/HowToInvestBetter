#!/usr/bin/env python3
# 本地提交（无需 token）：把全部内容存入本地 git，等待后续推送
import os, glob
from dulwich.repo import Repo
from dulwich import porcelain

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    repo = Repo(HERE)
    # 设默认分支为 main（dulwich 1.2 没有 set_symref，直接写 HEAD 文件）
    head_path = os.path.join(HERE, ".git", "HEAD")
    with open(head_path, "wb") as f:
        f.write(b"ref: refs/heads/main\n")

    files = []
    for f in glob.glob(os.path.join(HERE, "**"), recursive=True):
        if os.path.isfile(f) and ".git" not in f.split(os.sep):
            files.append(os.path.relpath(f, HERE))
    porcelain.add(repo, files)
    print(f"[ok] 已暂存 {len(files)} 个文件", flush=True)

    msg = ("内容做细：扩充薄弱章节(01/02/04/08/09) + 新增4个细分专题章(21基金选择/22固收/"
           "23全球ETF/24衍生品杠杆)，总量 234→302 条；补齐 EPUB/PDF/lint；对标 HowToLiveBetter")
    porcelain.commit(repo, message=msg.encode("utf-8"),
                    author=b"leo-bone <57990177@qq.com>",
                    committer=b"leo-bone <57990177@qq.com>")
    print("[ok] 本地提交完成（尚未推送）", flush=True)

if __name__ == "__main__":
    main()
