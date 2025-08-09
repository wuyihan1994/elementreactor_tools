#!/usr/bin/env python3
"""
化学方程式反应物回填工具 - 100%工作版本

实际文件格式：
- 第0行：标题行（包含所有列名）
- 第1行：中文描述
- 第2行：数据类型
- 第3行开始：实际数据内容
"""

import csv
import re
import sys
from pathlib import Path


def parse_reactants_from_equation(equation):
    """从化学方程式中提取反应物列表"""
    if not equation or not equation.strip():
        return []
    
    equation = equation.strip()
    
    # 统一箭头格式
    equation = equation.replace('→', '->').replace('=', '->')
    
    if '->' not in equation:
        return []
    
    # 提取反应物部分（箭头左边）
    reactants_side = equation.split('->')[0].strip()
    
    # 分割反应物
    reactants = []
    parts = re.split(r'[+\s]+', reactants_side)
    
    for part in parts:
        part = part.strip()
        if part:
            # 移除化学计量数（如2H2中的2）
            clean_part = re.sub(r'^\d+(?:\.\d+)?', '', part)
            clean_part = clean_part.strip()
            if clean_part:
                reactants.append(clean_part)
    
    return reactants


def process_csv_actual_format(input_file, output_file=None):
    """处理实际格式的CSV文件"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ 错误: 文件不存在: {input_file}")
        return False
    
    if output_file is None:
        output_file = input_file
    
    try:
        # 读取所有行
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        if len(rows) < 4:
            print("❌ 错误: 文件至少需要4行（标题+中文+类型+数据）")
            return False
        
        # 分离格式描述和数据
        format_rows = rows[:3]  # 前3行：标题、中文、类型
        data_rows = rows[3:]    # 从第4行开始是数据
        
        print(f"📊 文件结构:")
        print(f"  标题行: {rows[0]}")
        print(f"  数据行数: {len(data_rows)}")
        
        # 获取标题行
        headers = rows[0]
        
        # 找到列索引
        try:
            equation_idx = headers.index('reaction_equation')
            reactants_idx = headers.index('reactants')
            print(f"  ✅ 找到列: reaction_equation={equation_idx}, reactants={reactants_idx}")
        except ValueError as e:
            print(f"❌ 错误: 找不到列 {e}")
            print(f"  可用列: {headers}")
            return False
        
        # 处理数据行
        updated_rows = rows[:3]  # 保留前3行（格式描述）
        processed_count = 0
        
        for row_num, row in enumerate(data_rows, 4):  # 从第4行开始编号
            if len(row) > max(equation_idx, reactants_idx):
                equation = row[equation_idx] if equation_idx < len(row) else ''
                current_reactants = row[reactants_idx] if reactants_idx < len(row) else ''
                
                # 解析反应物
                reactants = parse_reactants_from_equation(equation)
                reactants_str = '|'.join(reactants)
                
                # 确保行长度足够
                if len(row) <= reactants_idx:
                    row.extend([''] * (reactants_idx - len(row) + 1))
                
                # 回填到reactants列
                old_value = row[reactants_idx]
                row[reactants_idx] = reactants_str
                
                print(f"  行 {row_num}: '{old_value}' → '{reactants_str}'")
                if equation and equation != current_reactants:
                    print(f"    方程式: {equation}")
                
                processed_count += 1
            
            updated_rows.append(row)
        
        # 写回文件
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(updated_rows)
        
        print(f"✅ 成功处理 {processed_count} 行数据")
        print(f"📁 结果已保存到: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 处理错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("🔧 化学方程式反应物回填工具")
        print()
        print("用法:")
        print("  python reaction_backfill.py <csv文件路径>")
        print("  python reaction_backfill.py <csv文件路径> [输出文件路径]")
        print()
        print("示例:")
        print("  python reaction_backfill.py correct_reactions.csv")
        print("  python reaction_backfill.py input.csv output.csv")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(input_file).exists():
        print(f"❌ 错误: 文件不存在: {input_file}")
        return
    
    print(f"🚀 开始处理: {input_file}")
    success = process_csv_actual_format(input_file, output_file)
    
    if success:
        print("✅ 处理完成！")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()