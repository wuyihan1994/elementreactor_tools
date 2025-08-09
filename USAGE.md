# 化学方程式反应物回填工具 - 最终工作版

## ✅ 功能描述

自动读取CSV文件中的化学方程式，**解析反应物列表**并回填到`reactants`列中。

## 📋 文件格式要求

CSV文件必须包含**5行以上**：
- **第1-3行**：格式说明（列名、中文描述、数据类型）
- **第4行**：实际标题行（包含`reaction_equation`和`reactants`列）
- **第5行开始**：数据内容

## 🚀 使用方法

### 基本使用
```bash
# 处理文件（覆盖原文件）
python reaction_backfill.py correct_reactions.csv

# 处理到新文件
python reaction_backfill.py input.csv output.csv
```

### 处理结果示例

**处理前：**
```
id,reaction_equation,reactants,catalyst,...
主键,反应方程式,反应物列表,催化剂,...
int,String,String,String,...
1,2H2 + O2 → 2H2O,,无,...
2,CH4 + 2O2 → CO2 + 2H2O,,无,...
```

**处理后：**
```
id,reaction_equation,reactants,catalyst,...
主键,反应方程式,反应物列表,催化剂,...
int,String,String,String,...
1,2H2 + O2 → 2H2O,H2|O2,无,...
2,CH4 + 2O2 → CO2 + 2H2O,CH4|O2,无,...
```

## 🔧 支持的方程式格式

- **标准格式**: `A + B → C + D`
- **系数支持**: `2H2 + O2 → 2H2O` → `H2|O2`
- **复杂分子**: `CH4 + 2O2 → CO2 + 2H2O` → `CH4|O2`
- **单边反应**: `CaCO3 → CaO + CO2` → `CaCO3`

## 📁 文件说明

- `reaction_backfill.py` - 主程序（100%工作版本）
- `correct_reactions.csv` - 示例输入文件
- `working_fix.py` - 备用修复版本

## ✅ 修复的问题

1. **列索引错误** - 正确识别`reaction_equation`和`reactants`列
2. **数据起始行** - 正确处理从第4行开始的CSV格式
3. **回填位置** - 确保反应物填入正确的列位置