# 化学方程式反应物回填工具

## ✅ 功能描述

自动读取CSV文件中的化学方程式，**解析反应物列表**并回填到`reactants`列中。

## 🚀 使用方法

### 基本使用
```bash
# 处理文件（覆盖原文件）
python reaction_backfill.py correct_reactions.csv

# 处理到新文件
python reaction_backfill.py input.csv output.csv

# 使用main.py
python main.py correct_reactions.csv
```

### 文件格式
CSV文件格式：
- **第0行**：标题行（包含`reaction_equation`和`reactants`列）
- **第1行**：中文描述
- **第2行**：数据类型说明
- **第3行开始**：实际数据内容

### 示例格式
```
id,reaction_equation,reactants,catalyst,reaction_conditon,products,reaction_effect,reaction_type,desc
主键,反应方程式,反应物列表,催化剂,反应条件,产物列表,反应效果,反应类型,描述
int,String,String,String,String,String,String,String,String
1,2H2 + O2 → 2H2O,,无,加热,2H2O,生成水,化合反应,氢气和氧气反应生成水
2,CH4 + 2O2 → CO2 + 2H2O,,无,点燃,CO2+2H2O,完全燃烧,氧化反应,甲烷燃烧
```

### 处理结果
**输入方程式**: `2H2 + O2 → 2H2O`  
**输出反应物**: `H2|O2`

## 📁 核心文件
- `reaction_backfill.py` - 主处理程序
- `main.py` - 命令行入口
- `correct_reactions.csv` - 示例数据文件