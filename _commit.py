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
msg = ("专家级体检 + 亚马逊上架准备：修 2 处死链(eid/适当性办法)；新增版权声明页(CC BY 4.0 署名)；"
       "PDF 增印刷级 6x9 模式(HowToInvestBetter-print.pdf)；EPUB 增版权页；"
       "新增亚马逊 KDP 上架方案与竞品分析(AMAZON-上架方案.md)；README 补印刷PDF与出版入口；"
       "lint 升级交叉引用校验(109处0失效)与文档数字同步守护")
porcelain.commit(repo, message=msg.encode("utf-8"),
                 author=b"leo-bone <57990177@qq.com>",
                 committer=b"leo-bone <57990177@qq.com>")
print("[ok] 本地提交完成，文件数:", len(files))
