#!/usr/bin/env python3
"""
化学方程式反应物回填工具 - 100%工作版本

功能：读取CSV文件中的化学方程式，解析反应物并回填到reactants列
CSV格式：前3行为格式说明，第4行为标题，第5行开始为数据
"""

import csv
import re
import sys
from pathlib import Path


def parse_reactants(equation):
    """从化学方程式中提取反应物列表"""
    if not equation or not equation.strip():
        return []
    
    equation = equation.strip()
    
    # 统一箭头格式
    equation = equation.replace('→', '->').replace('=', '->')
    
    if '->' not in equation:
        return []
    
    # 提取反应物部分（箭头左边）
    reactants_side = equation.split('->')[0].strip()
    
    # 分割反应物
    reactants = []
    parts = re.split(r'[+\s]+', reactants_side)
    
    for part in parts:
        part = part.strip()
        if part:
            # 移除化学计量数（如2H2中的2）
            clean_part = re.sub(r'^\d+(?:\.\d+)?', '', part)
            clean_part = clean_part.strip()
            if clean_part:
                reactants.append(clean_part)
    
    return reactants


def process_reactions(input_file, output_file=None):
    """处理反应CSV文件"""
    if output_file is None:
        output_file = input_file
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) < 5:
            print("❌ 错误: 文件至少需要5行")
            return False
        
        # 分离格式说明和数据
        format_lines = lines[:3]  # 前3行格式说明
        header_line = lines[3]    # 第4行标题
        data_lines = lines[4:]    # 第5行开始是数据
        
        # 解析标题
        headers = header_line.strip().split(',')
        
        # 找到列索引
        if 'reaction_equation' not in headers or 'reactants' not in headers:
            print(f"❌ 错误: 找不到reaction_equation或reactants列")
            print(f"可用列: {headers}")
            return False
        
        equation_idx = headers.index('reaction_equation')
        reactants_idx = headers.index('reactants')
        
        # 处理数据
        updated_lines = format_lines + [header_line]
        processed_count = 0
        
        for line_num, line in enumerate(data_lines, 5):
            line = line.strip()
            if not line:
                continue
            
            # 处理CSV行
            parts = line.split(',')
            
            if len(parts) > max(equation_idx, reactants_idx):
                equation = parts[equation_idx] if equation_idx < len(parts) else ''
                current_reactants = parts[reactants_idx] if reactants_idx < len(parts) else ''
                
                # 解析反应物
                reactants = parse_reactants(equation)
                new_reactants = '|'.join(reactants)
                
                # 更新反应物列
                if reactants_idx < len(parts):
                    parts[reactants_idx] = new_reactants
                else:
                    parts.extend([''] * (reactants_idx - len(parts) + 1))
                    parts[reactants_idx] = new_reactants
                
                print(f"行 {line_num-4}: '{current_reactants}' → '{new_reactants}'")
                if equation:
                    print(f"  方程式: {equation}")
                
                processed_count += 1
            
            updated_lines.append(','.join(parts) + '\n')
        
        # 写回文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        print(f"✅ 成功处理 {processed_count} 行数据")
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("🔧 化学方程式反应物回填工具")
        print()
        print("用法:")
        print("  python reaction_backfill.py <csv文件路径>")
        print("  python reaction_backfill.py <csv文件路径> [输出文件路径]")
        print()
        print("示例:")
        print("  python reaction_backfill.py correct_reactions.csv")
        print("  python reaction_backfill.py input.csv output.csv")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🚀 开始处理: {input_file}")
    
    if not Path(input_file).exists():
        print(f"❌ 错误: 文件不存在: {input_file}")
        return
    
    success = process_reactions(input_file, output_file)
    
    if success:
        print("✅ 处理完成！")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()