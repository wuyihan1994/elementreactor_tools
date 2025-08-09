from elementreactor_tools import ChemicalEquationParser

# 测试化学方程式解析器
test_cases = [
    "2H2 + O2 → 2H2O",
    "CH4 + 2O2 → CO2 + 2H2O",
    "CaCO3 → CaO + CO2",
    "2Na + 2H2O → 2NaOH + H2",
    "Zn + 2HCl → ZnCl2 + H2"
]

for equation in test_cases:
    reactants = ChemicalEquationParser.parse_reactants(equation)
    print(f"方程式: {equation}")
    print(f"反应物: {reactants}")
    print("-" * 40)