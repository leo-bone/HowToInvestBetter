import os, ctypes, glob
libc = ctypes.CDLL(None)
def _raw_mkdir(p, mode=0o777):
    if isinstance(p, str):
        p = p.encode("utf-8")
    libc.mkdir(p, mode & 0o777)
os.mkdir = _raw_mkdir

from dulwich.repo import Repo
from dulwich import porcelain

HERE = "/Users/leo/WorkBuddy/2026-10-07-11-42-35/HowToInvestBetter"
repo = Repo(HERE)
files = []
for f in glob.glob(os.path.join(HERE, "**"), recursive=True):
    if os.path.isfile(f) and ".git" not in f.split(os.sep):
        files.append(os.path.relpath(f, HERE))
porcelain.add(repo, files)
msg = ("中文版 KDP 上架准备：署名改为 leo-bone；新增竖版封面 cover-book.png(1600x2560) 供 EPUB/PDF/KDP；"
       "新增 KDP-中文版填报表.md（书名/简介/关键词/分类/定价/步骤）；EPUB/PDF 接入竖版封面与版权页并重建")
porcelain.commit(repo, message=msg.encode("utf-8"),
                 author=b"leo-bone <57990177@qq.com>",
                 committer=b"leo-bone <57990177@qq.com>")
print("[ok] 本地提交完成，文件数:", len(files))
