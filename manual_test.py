#!/usr/bin/env python3

import csv
import re

def parse_reactants(equation):
    """解析反应物"""
    if not equation:
        return []
    
    equation = equation.replace('→', '->')
    
    if '->' not in equation:
        return []
    
    reactants_side = equation.split('->')[0].strip()
    
    reactants = []
    parts = re.split(r'[+\s]+', reactants_side)
    
    for part in parts:
        part = part.strip()
        if part:
            clean_part = re.sub(r'^\d+(?:\.\d+)?', '', part)
            clean_part = clean_part.strip()
            if clean_part:
                reactants.append(clean_part)
    
    return reactants

# 测试解析
print("测试解析功能:")
test_cases = [
    "2H2 + O2 → 2H2O",
    "CH4 + 2O2 → CO2 + 2H2O",
    "CaCO3 → CaO + CO2",
    "2Na + 2H2O → 2NaOH + H2",
    "Zn + 2HCl → ZnCl2 + H2"
]

for eq in test_cases:
    reactants = parse_reactants(eq)
    print(f"{eq} -> {reactants}")

print("\n处理CSV文件:")

# 读取并处理CSV
with open('test_reactions.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"文件行数: {len(lines)}")

# 分离头部和数据
header_lines = lines[:3]
data_lines = lines[3:]

print("头部:")
for line in header_lines:
    print(line.strip())

print("\n数据:")
for line in data_lines:
    print(line.strip())

# 处理数据
print("\n处理数据...")
import io

# 创建CSV读取器
csv_content = ''.join(data_lines)
reader = csv.reader(io.StringIO(csv_content))

rows = list(reader)
print(f"数据行数: {len(rows)}")

if rows:
    headers = rows[0]
    print(f"列名: {headers}")
    
    # 找到列索引
    try:
        equation_idx = headers.index('reaction_equation')
        reactants_idx = headers.index('reactants')
        print(f"reaction_equation列索引: {equation_idx}")
        print(f"reactants列索引: {reactants_idx}")
    except ValueError as e:
        print(f"错误: {e}")
        exit(1)
    
    # 处理数据行
    updated_rows = [headers]
    
    for row in rows[1:]:
        if len(row) > max(equation_idx, reactants_idx):
            equation = row[equation_idx] if equation_idx < len(row) else ''
            current_reactants = row[reactants_idx] if reactants_idx < len(row) else ''
            
            new_reactants = parse_reactants(equation)
            new_reactants_str = '|'.join(new_reactants)
            
            print(f"行: {row}")
            print(f"方程式: {equation}")
            print(f"当前反应物: '{current_reactants}'")
            print(f"新反应物: '{new_reactants_str}'")
            
            # 更新反应物列
            if reactants_idx < len(row):
                row[reactants_idx] = new_reactants_str
            else:
                row.extend([''] * (reactants_idx - len(row) + 1))
                row[reactants_idx] = new_reactants_str
            
            print(f"更新后: {row}")
            print("-" * 50)
        
        updated_rows.append(row)
    
    # 写回文件
    with open('test_reactions_processed.csv', 'w', encoding='utf-8', newline='') as f:
        # 写入原始头部
        for line in header_lines:
            f.write(line)
        
        # 写入处理后的数据
        writer = csv.writer(f)
        writer.writerows(updated_rows)
    
    print("✅ 处理完成！文件已保存为 test_reactions_processed.csv")

else:
    print("❌ 没有数据行")