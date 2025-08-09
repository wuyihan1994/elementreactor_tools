#!/usr/bin/env python3

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
    import re
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

# 测试
test_cases = [
    "2H2 + O2 -> 2H2O",
    "CH4 + 2O2 -> CO2 + 2H2O", 
    "CaCO3 -> CaO + CO2",
    "2Na + 2H2O -> 2NaOH + H2",
    "Zn + 2HCl -> ZnCl2 + H2"
]

for eq in test_cases:
    result = parse_reactants(eq)
    print(f"{eq} -> {result}")