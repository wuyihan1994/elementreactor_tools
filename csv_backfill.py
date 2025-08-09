#!/usr/bin/env python3
"""
化学方程式反应物回填工具

功能：读取CSV文件中的化学方程式，解析反应物并回填到reactants列
格式：csv文件前三行为列名、中文名称、数据类型，第四行开始为数据
"""

import csv
import re
import sys
from pathlib import Path


def parse_reactants_from_equation(equation):
    """
    从化学方程式中提取反应物列表
    
    支持格式：
    - "2H2 + O2 → 2H2O"
    - "CH4 + 2O2 → CO2 + 2H2O" 
    - "CaCO3 → CaO + CO2"
    
    返回：反应物列表，如 ["H2", "O2"]
    """
    if not equation or not equation.strip():
        return []
    
    equation = equation.strip()
    
    # 统一箭头格式
    equation = equation.replace('→', '->').replace('=', '->')
    
    # 检查是否有箭头
    if '->' not in equation:
        return []
    
    # 提取反应物部分（箭头左边）
    reactants_side = equation.split('->')[0].strip()
    
    # 分割反应物
    reactants = []
    
    # 使用正则分割+号和空格
    parts = re.split(r'[+\s]+', reactants_side)
    
    for part in parts:
        part = part.strip()
        if part:
            # 移除化学计量数（如2H2中的2）
            # 匹配开头的数字，包括整数和小数
            clean_part = re.sub(r'^\d+(?:\.\d+)?', '', part)
            clean_part = clean_part.strip()
            
            if clean_part:
                reactants.append(clean_part)
    
    return reactants


def process_reaction_csv(input_file, output_file=None):
    """
    处理反应CSV文件，回填反应物信息
    
    参数：
    - input_file: 输入CSV文件路径
    - output_file: 输出CSV文件路径，默认为覆盖原文件
    
    返回：处理结果字典
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        return {
            'success': False,
            'error': f'文件不存在: {input_file}',
            'processed_rows': 0
        }
    
    if output_file is None:
        output_file = input_file
    
    try:
        # 读取文件内容
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) < 4:
            return {
                'success': False,
                'error': 'CSV文件格式错误：至少需要4行',
                'processed_rows': 0
            }
        
        # 分离头部和数据
        header_lines = lines[:3]  # 前三行（列名、中文、类型）
        
        # 找到数据开始位置
        data_start = 3
        for i in range(3, len(lines)):
            line = lines[i].strip()
            if line and not line.startswith(','):
                data_start = i
                break
        
        # 读取数据部分
        data_lines = lines[data_start:]
        
        # 处理数据
        processed_rows = 0
        updated_data = []
        
        # 创建CSV读取器
        reader = csv.DictReader(data_lines)
        
        # 获取字段名
        if reader.fieldnames is None:
            return {
                'success': False,
                'error': '无法读取CSV字段名',
                'processed_rows': 0
            }
        
        fieldnames = list(reader.fieldnames)
        
        # 确保reactants列存在
        if 'reactants' not in fieldnames:
            fieldnames.append('reactants')
        
        # 处理每一行
        for row in reader:
            equation = row.get('reaction_equation', '')
            
            # 解析反应物
            reactants = parse_reactants_from_equation(equation)
            
            # 回填反应物列
            row['reactants'] = '|'.join(reactants)
            
            updated_data.append(row)
            processed_rows += 1
        
        # 写回文件
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            # 写入原始头部
            for line in header_lines:
                f.write(line)
            
            # 写入数据
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if data_lines:
                # 写入标题行（如果需要）
                if data_start == 3:  # 只有标题行+数据
                    writer.writeheader()
                writer.writerows(updated_data)
        
        return {
            'success': True,
            'processed_rows': processed_rows,
            'message': f'成功处理 {processed_rows} 行数据'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'processed_rows': 0
        }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python csv_backfill.py <csv文件路径> [输出文件路径]")
        print("示例: python csv_backfill.py reactions.csv")
        print("示例: python csv_backfill.py reactions.csv output.csv")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = process_reaction_csv(input_file, output_file)
    
    if result['success']:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ 错误: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()