#!/usr/bin/env python3
"""
化学方程式反应物回填工具 - 最终修复版
修复了反应物回填到正确列的问题
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


def process_csv_correctly(input_file, output_file=None):
    """正确处理CSV文件，确保反应物回填到正确列"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ 错误: 文件不存在: {input_file}")
        return False
    
    if output_file is None:
        output_file = input_file
    
    try:
        # 读取所有行
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) < 4:
            print("❌ 错误: CSV文件至少需要4行")
            return False
        
        # 分离头部和数据
        header_lines = lines[:3]  # 前三行（格式说明）
        data_content = ''.join(lines[3:])  # 数据部分
        
        # 处理CSV数据
        reader = csv.reader(data_content.strip().split('\n'))
        rows = list(reader)
        
        if len(rows) < 2:
            print("❌ 错误: 没有数据行")
            return False
        
        # 获取标题行
        headers = rows[0]
        
        # 找到列索引
        try:
            equation_idx = headers.index('reaction_equation')
            reactants_idx = headers.index('reactants')
        except ValueError as e:
            print(f"❌ 错误: 找不到列 {e}")
            return False
        
        print(f"📋 列索引: reaction_equation={equation_idx}, reactants={reactants_idx}")
        
        # 处理数据行
        updated_rows = [headers]  # 保留标题行
        processed_count = 0
        
        for row in rows[1:]:  # 跳过标题行
            if len(row) > max(equation_idx, reactants_idx):
                equation = row[equation_idx] if equation_idx < len(row) else ''
                
                # 解析反应物
                reactants = parse_reactants_from_equation(equation)
                reactants_str = '|'.join(reactants)
                
                # 确保行长度足够
                if len(row) <= reactants_idx:
                    row.extend([''] * (reactants_idx - len(row) + 1))
                
                # 回填到reactants列
                old_value = row[reactants_idx]
                row[reactants_idx] = reactants_str
                
                print(f"行 {processed_count + 1}: '{old_value}' → '{reactants_str}'")
                
                processed_count += 1
            
            updated_rows.append(row)
        
        # 写回文件
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            # 写入原始头部
            for line in header_lines:
                f.write(line)
            
            # 写入处理后的数据
            for row in updated_rows:
                f.write(','.join(row) + '\n')
        
        print(f"✅ 成功处理 {processed_count} 行数据")
        print(f"📁 结果已保存到: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 处理错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def preview_changes(input_file):
    """预览将要进行的更改"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ 错误: 文件不存在: {input_file}")
        return
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) < 4:
            print("❌ 错误: CSV文件格式不正确")
            return
        
        # 读取数据
        data_content = ''.join(lines[3:])
        reader = csv.reader(data_content.strip().split('\n'))
        rows = list(reader)
        
        if len(rows) < 2:
            print("❌ 错误: 没有数据行")
            return
        
        headers = rows[0]
        try:
            equation_idx = headers.index('reaction_equation')
            reactants_idx = headers.index('reactants')
        except ValueError as e:
            print(f"❌ 错误: 找不到列 {e}")
            return
        
        print("🔍 预览更改:")
        print("=" * 100)
        print(f"{'行号':<5} {'方程式':<25} {'当前反应物':<15} {'新反应物':<20}")
        print("-" * 100)
        
        for i, row in enumerate(rows[1:], 1):
            if len(row) > max(equation_idx, reactants_idx):
                equation = row[equation_idx] if equation_idx < len(row) else ''
                current = row[reactants_idx] if reactants_idx < len(row) else ''
                new_reactants = '|'.join(parse_reactants_from_equation(equation))
                
                print(f"{i:<5} {equation:<25} {current:<15} {new_reactants:<20}")
        
    except Exception as e:
        print(f"预览错误: {e}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("🔧 化学方程式反应物回填工具")
        print()
        print("用法:")
        print("  python final_fix.py <csv文件路径>")
        print("  python final_fix.py <csv文件路径> [输出文件路径]")
        print("  python final_fix.py --preview <csv文件路径>")
        print()
        print("示例:")
        print("  python final_fix.py correct_reactions.csv")
        print("  python final_fix.py input.csv output.csv")
        print("  python final_fix.py --preview correct_reactions.csv")
        return
    
    # 处理预览模式
    if len(sys.argv) == 3 and sys.argv[1] == '--preview':
        preview_changes(sys.argv[2])
        return
    
    # 处理正常模式
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🚀 开始处理: {input_file}")
    success = process_csv_correctly(input_file, output_file)
    
    if success:
        print("✅ 处理完成！")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()