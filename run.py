#!/usr/bin/env python3

import csv
import re
from pathlib import Path


def parse_reactants(equation):
    """从化学方程式中提取反应物列表"""
    if not equation:
        return []
    
    # 替换箭头符号
    equation = equation.replace('→', '->')
    
    # 分割反应物和产物
    if '->' not in equation:
        return []
    
    reactants_side = equation.split('->')[0].strip()
    
    # 分割反应物
    reactants = []
    for reactant in re.split(r'[+\s]+', reactants_side):
        reactant = reactant.strip()
        if reactant:
            # 移除系数
            reactant = re.sub(r'^\d+', '', reactant)
            reactant = re.sub(r'^\d+\.\d+', '', reactant)
            reactant = reactant.strip()
            if reactant:
                reactants.append(reactant)
    
    return reactants


def process_csv(file_path):
    """处理CSV文件"""
    file_path = Path(file_path)
    
    # 读取文件
    lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 分离头部和数据
    header = lines[:4]  # 前三行 + 标题行
    data_lines = lines[4:]  # 数据行
    
    # 处理数据
    processed_data = []
    reader = csv.DictReader(data_lines)
    
    for row in reader:
        equation = row.get('reaction_equation', '')
        reactants = parse_reactants(equation)
        row['reactants'] = '|'.join(reactants)
        processed_data.append(row)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        for line in header:
            f.write(line)
        
        if processed_data:
            writer = csv.DictWriter(f, fieldnames=processed_data[0].keys())
            writer.writerows(processed_data)
    
    return len(processed_data)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("用法: python run.py <csv文件路径>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    try:
        count = process_csv(csv_file)
        print(f"✅ 成功处理 {count} 行数据")
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)