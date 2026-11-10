"""
迷你任务管理器 v0.1
------------------------
用 tasklist 命令抓取电脑里所有正在运行的程序，
看看谁在偷偷吃你的内存。

运行方法：在 cmd 里进入这个文件夹，输入
    python mini_task_manager.py
"""

import csv
import io
import subprocess


def get_processes():
    """运行 tasklist 命令，把一坨文字整理成程序列表"""
    result = subprocess.run(
        ["tasklist", "/FO", "CSV", "/NH"],  # CSV 格式、不要表头，方便用程序读
        capture_output=True,
    )
    # Windows 中文系统里 tasklist 输出用的是 GBK 编码
    text = result.stdout.decode("gbk", errors="ignore")

    procs = []
    for row in csv.reader(io.StringIO(text)):
        if len(row) < 5:
            continue
        # 内存那一列长这样："1,993,680 K"，把数字挑出来换成整数
        digits = "".join(ch for ch in row[4] if ch.isdigit())
        mem_kb = int(digits) if digits else 0
        procs.append({"name": row[0], "pid": row[1], "mem_kb": mem_kb})
    return procs


def draw_bar(value, top, width=32):
    """按比例画横条：内存越大，条越长"""
    if top <= 0:
        return ""
    return "█" * max(int(width * value / top), 1)


def show_header(procs):
    total_mb = sum(p["mem_kb"] for p in procs) / 1024
    print()
    print("=" * 72)
    print(f"  当前共 {len(procs)} 个进程，内存粗略合计约 {total_mb:,.0f} MB")
    print("=" * 72)


def show_single(procs):
    """选项 1：按单个进程排名"""
    show_header(procs)
    top_list = sorted(procs, key=lambda p: p["mem_kb"], reverse=True)[:15]
    top = top_list[0]["mem_kb"] if top_list else 0
    print(f"  {'名次':<4}{'程序':<34}{'PID':>8}{'内存':>10}   占用条")
    print("-" * 72)
    for i, p in enumerate(top_list, 1):
        mb = p["mem_kb"] / 1024
        print(f"  {i:<4}{p['name']:<34}{p['pid']:>8}{mb:>7.0f} MB   {draw_bar(p['mem_kb'], top)}")
    if top_list:
        print(f"\n  内存冠军：{top_list[0]['name']}（{top_list[0]['mem_kb'] / 1024:.0f} MB）")


def show_grouped(procs):
    """选项 2：同名程序先合并（比如几十个 svchost 算一家）"""
    totals = {}
    counts = {}
    for p in procs:
        totals[p["name"]] = totals.get(p["name"], 0) + p["mem_kb"]
        counts[p["name"]] = counts.get(p["name"], 0) + 1
    items = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:15]
    top = items[0][1] if items else 0

    print()
    print("=" * 72)
    print("  按程序合并排行（同名的进程算一家）")
    print("=" * 72)
    print(f"  {'名次':<4}{'程序':<30}{'个数':>6}{'内存合计':>12}   占用条")
    print("-" * 72)
    for i, (name, kb) in enumerate(items, 1):
        mb = kb / 1024
        print(f"  {i:<4}{name:<30}{counts[name]:>6}{mb:>9.0f} MB   {draw_bar(kb, top)}")


def search(procs):
    """选项 3：查某个程序的所有进程"""
    key = input("  输入关键字（比如 svchost、edge）: ").strip().lower()
    if not key:
        print("  没输入关键字，算啦～")
        return
    hits = [p for p in procs if key in p["name"].lower()]
    if not hits:
        print(f"  没找到名字里带 “{key}” 的进程（试试英文名）")
        return
    hits.sort(key=lambda p: p["mem_kb"], reverse=True)
    total_mb = sum(p["mem_kb"] for p in hits) / 1024
    print(f"\n  名字带 “{key}” 的进程共 {len(hits)} 个，内存合计 {total_mb:.0f} MB：")
    for p in hits[:20]:
        print(f"    PID {p['pid']:>7}   {p['mem_kb'] / 1024:>7.1f} MB   {p['name']}")
    if len(hits) > 20:
        print(f"    ……还有 {len(hits) - 20} 个没显示")


def main():
    print("=" * 72)
    print("  迷你任务管理器 v0.1 —— 看看谁在偷偷吃你的内存")
    print("=" * 72)
    while True:
        print()
        print("  1. 内存排行榜 TOP 15（单个进程）")
        print("  2. 按程序合并排行（几十个 svchost 合成一家算）")
        print("  3. 查某个程序的所有进程")
        print("  0. 退出")
        choice = input("  选哪个？> ").strip()

        if choice == "0":
            print("  拜拜～ 无聊了再来看看内存排行榜")
            break
        try:
            procs = get_processes()
        except Exception as e:
            print(f"  出错了：{e}")
            continue

        if choice == "1":
            show_single(procs)
        elif choice == "2":
            show_grouped(procs)
        elif choice == "3":
            search(procs)
        else:
            print("  没有这个选项哦，再选一次～")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  拜拜～")
