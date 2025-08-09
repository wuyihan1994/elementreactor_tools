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

# 读取文件
with open('correct_reactions.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("原始文件:")
for i, line in enumerate(lines, 1):
    print(f"{i:2d}: {line.rstrip()}")

# 分离格式说明和数据
format_lines = lines[:3]
data_lines = lines[3:]

print(f"\n格式说明行: {len(format_lines)}")
print(f"数据行: {len(data_lines)}")

# 处理数据
print("\n处理数据部分:")
data_content = ''.join(data_lines)
reader = csv.reader(data_content.strip().split('\n'))

rows = list(reader)
print(f"数据行数: {len(rows)}")

if rows:
    headers = rows[0]
    print(f"列名: {headers}")
    
    equation_idx = headers.index('reaction_equation')
    reactants_idx = headers.index('reactants')
    
    print(f"列索引: equation={equation_idx}, reactants={reactants_idx}")
    
    # 处理数据
    updated_rows = [headers]
    
    for row in rows[1:]:
        if len(row) > max(equation_idx, reactants_idx):
            equation = row[equation_idx]
            current_reactants = row[reactants_idx]
            
            new_reactants = parse_reactants(equation)
            new_reactants_str = '|'.join(new_reactants)
            
            print(f"\n处理: {equation}")
            print(f"  当前: '{current_reactants}' → 新: '{new_reactants_str}'")
            
            row[reactants_idx] = new_reactants_str
        
        updated_rows.append(row)
    
    # 写回文件
    with open('correct_reactions_processed.csv', 'w', encoding='utf-8', newline='') as f:
        # 写入格式说明
        for line in format_lines:
            f.write(line)
        
        # 写入处理后的数据
        writer = csv.writer(f)
        writer.writerows(updated_rows)
    
    print(f"\n✅ 完成！生成了 correct_reactions_processed.csv")
    
    print(f"\n处理结果:")
    with open('correct_reactions_processed.csv', 'r', encoding='utf-8') as f:
        for line in f:
            print(line.rstrip())