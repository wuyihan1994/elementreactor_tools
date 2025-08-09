#!/usr/bin/env python3
"""
化学方程式反应物回填工具 - 修复版

修复问题：确保反应物正确回填到reactants列中
"""

import csv
import re
import sys
from pathlib import Path


def parse_reactants_from_equation(equation):
    """从化学方程式中提取反应物列表"""
    if not equation or not equation.strip():
        return []
    
    equation = equation.strip()
    
    # 统一箭头格式
    equation = equation.replace('→', '->').replace('=', '->')
    
    if '->' not in equation:
        return []
    
    # 提取反应物部分
    reactants_side = equation.split('->')[0].strip()
    
    # 分割反应物
    reactants = []
    parts = re.split(r'[+\s]+', reactants_side)
    
    for part in parts:
        part = part.strip()
        if part:
            # 移除化学计量数
            clean_part = re.sub(r'^\d+(?:\.\d+)?', '', part)
            clean_part = clean_part.strip()
            
            if clean_part:
                reactants.append(clean_part)
    
    return reactants


def fix_csv_file(input_file, output_file=None):
    """修复CSV文件，正确回填反应物"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"错误: 文件不存在: {input_file}")
        return False
    
    if output_file is None:
        output_file = input_file
    
    try:
        # 读取所有行
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) < 4:
            print("错误: CSV文件至少需要4行")
            return False
        
        # 分离头部和数据
        header_lines = lines[:3]  # 前三行
        data_lines = lines[3:]    # 数据行
        
        # 处理数据
        updated_lines = []
        
        # 使用csv处理数据
        import io
        data_content = ''.join(data_lines)
        
        # 找到实际的数据开始位置
        lines_to_process = data_content.strip().split('\n')
        if not lines_to_process:
            print("错误: 没有数据需要处理")
            return False
        
        # 处理CSV数据
        reader = csv.reader(lines_to_process)
        rows = list(reader)
        
        if not rows:
            print("错误: 无法读取数据")
            return False
        
        # 获取标题行并确定列索引
        headers = rows[0]
        try:
            equation_col = headers.index('reaction_equation')
            reactants_col = headers.index('reactants')
        except ValueError as e:
            print(f"错误: 找不到列 {e}")
            return False
        
        # 添加标题行
        updated_lines.append(','.join(headers))
        
        # 处理数据行
        processed_count = 0
        for row in rows[1:]:  # 跳过标题行
            if len(row) > max(equation_col, reactants_col):
                equation = row[equation_col] if equation_col < len(row) else ''
                reactants = parse_reactants_from_equation(equation)
                
                # 回填到reactants列
                if reactants_col < len(row):
                    row[reactants_col] = '|'.join(reactants)
                else:
                    # 扩展行长度
                    row.extend([''] * (reactants_col - len(row) + 1))
                    row[reactants_col] = '|'.join(reactants)
                
                processed_count += 1
            
            updated_lines.append(','.join(row))
        
        # 写回文件
        with open(output_file, 'w', encoding='utf-8') as f:
            # 写入原始头部
            for line in header_lines:
                f.write(line)
            
            # 写入处理后的数据
            for line in updated_lines:
                f.write(line + '\n')
        
        print(f"✅ 成功处理 {processed_count} 行数据")
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def preview_changes(input_file):
    """预览将要进行的更改"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"错误: 文件不存在: {input_file}")
        return
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) < 4:
            print("错误: CSV文件格式不正确")
            return
        
        # 读取数据
        data_lines = lines[3:]
        reader = csv.reader(data_lines)
        rows = list(reader)
        
        if len(rows) < 2:
            print("错误: 没有数据行")
            return
        
        headers = rows[0]
        try:
            equation_col = headers.index('reaction_equation')
            reactants_col = headers.index('reactants')
        except ValueError as e:
            print(f"错误: 找不到列 {e}")
            return
        
        print("📋 预览更改:")
        print("=" * 80)
        
        for i, row in enumerate(rows[1:], 1):
            if len(row) > max(equation_col, reactants_col):
                equation = row[equation_col] if equation_col < len(row) else ''
                current = row[reactants_col] if reactants_col < len(row) else ''
                new_reactants = '|'.join(parse_reactants_from_equation(equation))
                
                print(f"第{i}行:")
                print(f"  方程式: {equation}")
                print(f"  当前反应物: '{current}'")
                print(f"  解析结果: '{new_reactants}'")
                print()
        
    except Exception as e:
        print(f"预览错误: {e}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python csv_fix.py <csv文件路径> [输出文件路径]")
        print("       python csv_fix.py --preview <csv文件路径>")
        print()
        print("示例:")
        print("  python csv_fix.py example_reactions.csv")
        print("  python csv_fix.py input.csv output.csv")
        print("  python csv_fix.py --preview example_reactions.csv")
        return
    
    if len(sys.argv) == 3 and sys.argv[1] == '--preview':
        preview_changes(sys.argv[2])
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = fix_csv_file(input_file, output_file)
    if success:
        print(f"✅ 处理完成: {input_file}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()