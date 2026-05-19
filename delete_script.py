#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件删除脚本：在当前目录下，按名称递增顺序，每隔N个文件删除一个。
默认处理.jpg文件，N由控制台输入，未输入则为1。
规则：从第一个文件开始先保留，然后每隔N个删除一个（即保留第1个，删除第N+1个，保留第2N+1个...）
N=1时：保留1个，删除1个，保留1个，删除1个...（交替进行）
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
    # 找到最后一个点的位置
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
    # 确保扩展名以点开头
    if extension and not extension.startswith('.'):
        extension = '.' + extension
    
    # 获取所有匹配的文件
    files = []
    for f in os.listdir('.'):
        if os.path.isfile(f):
            if extension:
                # 比较扩展名（忽略大小写）
                if get_file_extension(f).lower() == extension.lower():
                    files.append(f)
            else:
                # 如果没有指定扩展名，则匹配所有文件
                files.append(f)
    
    # 按名称排序（使用自然排序，不区分大小写）
    files.sort(key=str.lower)
    
    return files

def delete_every_nth(files, n, dry_run=False):
    """
    每隔N个文件删除一个
    规则：从第一个文件开始保留，然后每隔N个删除一个
    即：保留索引0，删除索引n，保留索引2n，删除索引3n...
    
    Args:
        files: 文件列表（已排序）
        n: 间隔数
        dry_run: 是否为试运行模式
    
    Returns:
        tuple: (删除的文件列表, 保留的文件列表)
    """
    if n <= 0:
        print("错误：间隔数N必须为正整数")
        return [], files
    
    to_delete = []
    to_keep = []
    
    for idx, filename in enumerate(files):
        # 索引从0开始
        # 当索引能被n整除时，表示需要删除的位置
        # n=1: 索引0保留，索引1删除，索引2保留，索引3删除...
        # n=2: 索引0保留，索引1保留，索引2删除，索引3保留，索引4保留，索引5删除...
        if idx % n == 0:
            to_keep.append(filename)  # 索引0, n, 2n, 3n... 的位置保留
        else:
            # 需要判断是否在删除位置上
            # 实际删除的是：索引1,2,...,n-1 中的？等等，需要重新理解
            pass
    
    # 重新实现正确的逻辑
    to_delete = []
    to_keep = []
    
    for idx, filename in enumerate(files):
        # 按组划分，每组有n个保留 + 1个删除？
        # 用户需求：每隔n个删除一个，从第一个开始保留
        # 所以模式是：保留n个，删除1个，保留n个，删除1个...
        # 当n=1时：保留1个，删除1个，保留1个，删除1个...
        # 当n=2时：保留2个，删除1个，保留2个，删除1个...
        # 当n=3时：保留3个，删除1个，保留3个，删除1个...
        
        # 计算当前位置在周期中的偏移
        cycle_size = n + 1  # 每个周期有n个保留和1个删除
        position_in_cycle = idx % cycle_size
        
        if position_in_cycle < n:
            # 在前n个位置，保留
            to_keep.append(filename)
        else:
            # 在第n+1个位置（最后一个），删除
            to_delete.append(filename)
    
    if dry_run:
        print(f"\n[试运行模式] 将删除以下 {len(to_delete)} 个文件:")
        for f in to_delete:
            print(f"  [删除] {f}")
        print(f"\n将保留 {len(to_keep)} 个文件:")
        # 只显示前20个保留的文件，避免输出过多
        for i, f in enumerate(to_keep):
            if i < 20:
                print(f"  [保留] {f}")
            elif i == 20:
                print(f"  ... 还有 {len(to_keep) - 20} 个文件")
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
        # 确保扩展名以点开头
        if not ext_input.startswith('.'):
            extension = '.' + ext_input
        else:
            extension = ext_input
    
    # 获取间隔数N
    while True:
        print(f"\n请输入间隔数N（每隔N个文件删除一个，从第一个文件开始先保留）：")
        n_input = input("N (正整数，直接回车则默认 1): ").strip()
        if not n_input:
            n = 1
            break
        try:
            n = int(n_input)
            if n > 0:
                break
            else:
                print("错误：N 必须是正整数！")
        except ValueError:
            print("错误：请输入有效的数字！")
    
    # 获取匹配的文件
    files = get_matching_files(extension)
    
    if not files:
        print(f"\n当前目录下没有找到扩展名为 '{extension}' 的文件。")
        return
    
    print(f"\n找到 {len(files)} 个扩展名为 '{extension}' 的文件。")
    print(f"删除规则: 从第一个文件开始保留，然后每 {n} 个文件删除一个")
    print(f"具体模式: 保留 {n} 个 -> 删除 1 个 -> 保留 {n} 个 -> 删除 1 个...")
    
    if n == 1:
        print("说明: N=1 表示保留1个，删除1个，交替进行")
    
    # 显示前几个文件作为预览
    print("\n文件排序预览（前20个）:")
    for i, f in enumerate(files[:20]):
        print(f"  {i+1:3d}. {f}")
    if len(files) > 20:
        print(f"  ... 共 {len(files)} 个文件")
    
    # 计算将删除的文件数量
    cycle_size = n + 1
    will_delete = len(files) // cycle_size
    print(f"\n预计将删除 {will_delete} 个文件，保留 {len(files) - will_delete} 个文件")
    
    # 危险警告
    if will_delete > 0:
        print("\n⚠️  警告：此操作将永久删除文件！")
        confirm = input("确认要继续吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消。")
            return
        
        # 询问是否试运行
        dry_run_input = input("\n是否先试运行查看效果？(y/N): ")
        dry_run = dry_run_input.lower() == 'y'
        
        # 执行删除操作
        delete_every_nth(files, n, dry_run)
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