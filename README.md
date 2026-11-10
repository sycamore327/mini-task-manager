# 迷你任务管理器

一个零依赖的 Windows 命令行小工具：用系统自带的 `tasklist` 命令读取正在运行的进程，看看谁在偷偷吃你的内存。

## 功能

- 内存排行榜 TOP 15（按单个进程）
- 按程序合并排行（几十个 `svchost` 算一家）
- 按关键字查某个程序的所有进程
- 纯终端输出，用方块条直观显示内存占比

## 运行

需要 Windows 和 Python 3.8 以上，不需要安装任何第三方库。

```bash
python mini_task_manager.py
```

然后按提示输入 `1`、`2`、`3` 或 `0`。

## 原理

- 调用 Windows 自带的 `tasklist /FO CSV /NH`，把输出解析成进程列表
- 中文系统下 `tasklist` 使用 GBK 编码，脚本按 GBK 解码
- 内存列形如 `1,993,680 K`，去掉逗号后换算成 MB

## 注意

- 只支持 Windows
- 内存数值来自 `tasklist`，是粗略值，和任务管理器可能略有差异
- 不联网、不写文件、不需要管理员权限

## 文件

```text
mini_task_manager.py   主程序
```
