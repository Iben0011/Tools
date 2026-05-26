#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件删除脚本：在当前目录下，按名称递增顺序，对文件进行操作。
支持两种模式：
1. 隔n删除1个：保留n个，删除1个，重复进行
2. 隔n保留1个：删除n个，保留1个，重复进行

默认处理.jpg文件，n由控制台输入，未输入则为1。
"""

import os
import sys

def get_file_extension(filename):
    """
    获取文件的扩展名（最后一个点之后的部分）
    
    Args:
        filename: 文件名
    
    Returns:
        str: 扩展名（包含点），如果没有扩展名则返回空字符串
    """
    last_dot = filename.rfind('.')
    if last_dot == -1 or last_dot == 0:
        return ''
    return filename[last_dot:]

def get_matching_files(extension):
    """
    获取当前目录下所有匹配扩展名的文件，并按名称递增排序
    
    Args:
        extension: 文件扩展名（如 '.jpg'）
    
    Returns:
        list: 按名称排序的文件名列表
    """
    if extension and not extension.startswith('.'):
        extension = '.' + extension
    
    files = []
    for f in os.listdir('.'):
        if os.path.isfile(f):
            if extension:
                if get_file_extension(f).lower() == extension.lower():
                    files.append(f)
            else:
                files.append(f)
    
    files.sort(key=str.lower)
    return files

def process_files(files, n, mode, dry_run=False):
    """
    根据模式处理文件
    
    Args:
        files: 文件列表（已排序）
        n: 间隔数
        mode: 模式，'delete' 表示隔n删除1个，'keep' 表示隔n保留1个
        dry_run: 是否为试运行模式
    
    Returns:
        tuple: (删除的文件列表, 保留的文件列表)
    """
    if n <= 0:
        print("错误：间隔数n必须为正整数")
        return [], files
    
    to_delete = []
    to_keep = []
    
    if mode == 'delete':
        # 模式1：隔n删除1个（保留n个，删除1个，重复）
        # 模式：保留n个，删除1个，保留n个，删除1个...
        cycle_size = n + 1
        for idx, filename in enumerate(files):
            position_in_cycle = idx % cycle_size
            if position_in_cycle < n:
                # 前n个位置，保留
                to_keep.append(filename)
            else:
                # 第n+1个位置，删除
                to_delete.append(filename)
    else:  # mode == 'keep'
        # 模式2：隔n保留1个（删除n个，保留1个，重复）
        # 模式：删除n个，保留1个，删除n个，保留1个...
        cycle_size = n + 1
        for idx, filename in enumerate(files):
            position_in_cycle = idx % cycle_size
            if position_in_cycle == n:
                # 第n+1个位置（索引n），保留
                to_keep.append(filename)
            else:
                # 其他位置，删除
                to_delete.append(filename)
    
    if dry_run:
        print(f"\n[试运行模式] 将删除以下 {len(to_delete)} 个文件:")
        # 显示前30个删除的文件
        for i, f in enumerate(to_delete):
            if i < 30:
                print(f"  [删除] {f}")
            elif i == 30:
                print(f"  ... 还有 {len(to_delete) - 30} 个文件")
                break
        
        print(f"\n将保留 {len(to_keep)} 个文件:")
        for i, f in enumerate(to_keep):
            if i < 30:
                print(f"  [保留] {f}")
            elif i == 30:
                print(f"  ... 还有 {len(to_keep) - 30} 个文件")
                break
        
        return to_delete, to_keep
    
    # 实际删除文件
    deleted_count = 0
    for filename in to_delete:
        try:
            os.remove(filename)
            print(f"已删除: {filename}")
            deleted_count += 1
        except Exception as e:
            print(f"删除失败 {filename}: {e}")
    
    print(f"\n操作完成！共删除 {deleted_count} 个文件，保留 {len(to_keep)} 个文件。")
    print(f"删除比例: {deleted_count}/{len(files)} = {deleted_count/len(files)*100:.1f}%")
    return to_delete, to_keep

def show_preview(files, n, mode):
    """
    显示操作预览，让用户更直观地理解将要执行的操作
    
    Args:
        files: 文件列表
        n: 间隔数
        mode: 操作模式
    """
    print("\n" + "="*60)
    print("操作预览（前30个文件）:")
    print("="*60)
    
    if mode == 'delete':
        print(f"模式: 隔{n}删除1个（保留{n}个，删除1个，重复）")
        cycle_size = n + 1
        for i, filename in enumerate(files[:30]):
            position = i % cycle_size
            if position < n:
                status = "📁 保留"
            else:
                status = "❌ 删除"
            print(f"  {i+1:3d}. {status} | {filename}")
    else:
        print(f"模式: 隔{n}保留1个（删除{n}个，保留1个，重复）")
        cycle_size = n + 1
        for i, filename in enumerate(files[:30]):
            position = i % cycle_size
            if position == n:
                status = "📁 保留"
            else:
                status = "❌ 删除"
            print(f"  {i+1:3d}. {status} | {filename}")
    
    if len(files) > 30:
        print(f"  ... 共 {len(files)} 个文件")
    print("="*60)

def main():
    """主函数"""
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 获取文件扩展名
    print("\n请输入要操作的文件扩展名（直接回车则默认 .jpg）:")
    ext_input = input("扩展名: ").strip()
    if not ext_input:
        extension = '.jpg'
    else:
        if not ext_input.startswith('.'):
            extension = '.' + ext_input
        else:
            extension = ext_input
    
    # 选择操作模式（放在输入n之前）
    print("\n请选择操作模式：")
    print("  1. 隔n删除1个（保留n个，删除1个，重复）")
    print("  2. 隔n保留1个（删除n个，保留1个，重复）")
    
    while True:
        mode_input = input("请选择 (1 或 2，直接回车则默认 1): ").strip()
        if not mode_input or mode_input == '1':
            mode = 'delete'
            break
        elif mode_input == '2':
            mode = 'keep'
            break
        else:
            print("错误：请输入 1 或 2！")
    
    # 获取间隔数n（小写）
    while True:
        print(f"\n请输入间隔数n：")
        n_input = input("n (正整数，直接回车则默认 1): ").strip()
        if not n_input:
            n = 1
            break
        try:
            n = int(n_input)
            if n > 0:
                break
            else:
                print("错误：n 必须是正整数！")
        except ValueError:
            print("错误：请输入有效的数字！")
    
    # 模式描述
    if mode == 'delete':
        mode_desc = f"隔{n}删除1个（保留{n}个，删除1个）"
    else:
        mode_desc = f"隔{n}保留1个（删除{n}个，保留1个）"
    
    # 获取匹配的文件
    files = get_matching_files(extension)
    
    if not files:
        print(f"\n当前目录下没有找到扩展名为 '{extension}' 的文件。")
        return
    
    print(f"\n找到 {len(files)} 个扩展名为 '{extension}' 的文件。")
    print(f"操作模式: {mode_desc}")
    
    # 显示预览
    show_preview(files, n, mode)
    
    # 计算统计信息
    cycle_size = n + 1
    if mode == 'delete':
        will_delete = len(files) // cycle_size
        will_keep = len(files) - will_delete
    else:
        will_keep = len(files) // cycle_size
        will_delete = len(files) - will_keep
    
    print(f"\n统计信息:")
    print(f"  总文件数: {len(files)}")
    print(f"  将删除: {will_delete} 个")
    print(f"  将保留: {will_keep} 个")
    
    # 危险警告
    if will_delete > 0:
        print("\n⚠️  警告：此操作将永久删除文件！")
        confirm = input("确认要继续吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消。")
            return
        
        # 询问是否试运行
        dry_run_input = input("\n是否先试运行查看详细效果？(y/N): ")
        dry_run = dry_run_input.lower() == 'y'
        
        # 执行操作
        process_files(files, n, mode, dry_run)
    else:
        print("没有文件需要删除。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已被用户中断。")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误: {e}")
        sys.exit(1)
