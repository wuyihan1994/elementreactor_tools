# 化学方程式反应物回填工具

## 功能描述

自动读取CSV文件中的化学方程式，**解析反应物**并回填到`reactants`列中。

## 使用方法

### 命令行使用

```bash
# 处理单个文件
python csv_backfill.py example_reactions.csv

# 处理并输出到新文件
python csv_backfill.py input.csv output.csv
```

### CSV文件格式要求

文件必须包含以下列结构，**前三行固定**为格式说明：

|id|reaction_equation|reactants|catalyst|reaction_conditon|products|reaction_effect|reaction_type|desc|
| ---| --------------------| ------------| ----------| --------------------| ----------| ------------------| ----------------| --------|
|主键|反应方程式|反应物列表|催化剂|反应条件|产物列表|反应效果|反应类型|描述|
|int|String|String|String|String|String|String|String|String|

### 示例

**输入方程式**: `2H2 + O2 → 2H2O`  
**输出反应物**: `H2|O2`

## 支持的方程式格式

- **标准格式**: `A + B → C + D`
- **系数支持**: `2H2 + O2 → 2H2O` → `H2|O2`
- **复杂分子**: `CH4 + 2O2 → CO2 + 2H2O` → `CH4|O2`

## 安装

```bash
pip install .
```

## 开发

使用uv进行包管理：
```bash
uv run csv_backfill.py example_reactions.csv
```