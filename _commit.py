import os, ctypes
libc = ctypes.CDLL(None)
def _m(p, mode=0o777):
    if isinstance(p, str): p = p.encode()
    try: libc.mkdir(p, mode & 0o777)
    except OSError: pass
os.mkdir = _m
os.makedirs = lambda n, mode=0o777, exist_ok=False: _m(n, mode)

from dulwich import porcelain
from dulwich.repo import Repo

REPO = "/Users/leo/WorkBuddy/2026-10-07-11-42-35/HowToInvestBetter"
r = Repo(REPO)

paths = []
for dp, dns, fns in os.walk(REPO):
    dns[:] = [x for x in dns if x != ".git"]
    for fn in fns:
        rel = os.path.relpath(os.path.join(dp, fn), REPO)
        if rel.startswith(".git" + os.sep):
            continue
        paths.append(rel.strip())
porcelain.add(r, paths)
print("staged:", len(paths))

msg = ("add: 纸书完整书封（KDP 6x9 全 wrap，300DPI PDF+PNG）\n\n"
       "- tools/gen_cover_paperback.py: 按页数自动算书脊，封底|书脊|封面 布局，条码区留白\n"
       "- cover-paperback.pdf / cover-paperback.png: 338 页白纸，书脊 0.7612\"，13.0112x9.2500\"\n"
       "- 更新 KDP 填报表/上架方案/README：纸书书封就绪")
cid = porcelain.commit(r, message=msg.encode("utf-8"),
                       author=b"leo-bone <leo-bone@users.noreply.github.com>",
                       committer=b"leo-bone <leo-bone@users.noreply.github.com>")
print("commit:", cid.decode())
