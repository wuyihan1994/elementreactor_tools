import csv
import re

# 测试解析器
def parse_reactants(equation):
    if not equation:
        return []
    
    # 处理箭头
    equation = equation.replace('→', '->')
    
    if '->' not in equation:
        return []
    
    reactants_side = equation.split('->')[0].strip()
    
    # 分割反应物
    reactants = []
    parts = re.split(r'[+\s]+', reactants_side)
    
    for part in parts:
        part = part.strip()
        if part:
            # 移除系数
            part = re.sub(r'^\d+\.?\d*', '', part)
            part = part.strip()
            if part:
                reactants.append(part)
    
    return reactants

# 测试用例
tests = [
    "2H2 + O2 -> 2H2O",
    "CH4 + 2O2 -> CO2 + 2H2O", 
    "CaCO3 -> CaO + CO2",
    "2Na + 2H2O -> 2NaOH + H2",
    "Zn + 2HCl -> ZnCl2 + H2"
]

print("测试化学方程式解析:")
for test in tests:
    result = parse_reactants(test)
    print(f"{test} -> {result}")

# 处理CSV
print("\n处理CSV文件...")
try:
    with open('example_reactions.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到数据开始行
    data_start = 0
    for i, line in enumerate(lines):
        if re.match(r'^\d+,', line):
            data_start = i
            break
    
    header = lines[:data_start]
    data_lines = lines[data_start:]
    
    # 处理数据
    processed = []
    reader = csv.reader(data_lines)
    
    for row in reader:
        if len(row) >= 9:
            equation = row[1]  # reaction_equation
            reactants = parse_reactants(equation)
            row[2] = '|'.join(reactants)  # reactants列
            processed.append(row)
    
    # 写回
    with open('processed_reactions.csv', 'w', encoding='utf-8', newline='') as f:
        for line in header:
            f.write(line)
        
        writer = csv.writer(f)
        writer.writerows(processed)
    
    print(f"✅ 成功处理 {len(processed)} 行数据")
    
except Exception as e:
    print(f"❌ 错误: {e}")