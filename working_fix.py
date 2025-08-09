#!/usr/bin/env python3
"""
化学方程式反应物回填工具 - 最终工作版本
修复了数据起始行识别和列索引问题
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
    
    # 提取反应物部分
    reactants_side = equation.split('->')[0].strip()
    
    # 分割反应物
    reactants = []
    parts = re.split(r'[+\s]+', reactants_side)
    
    for part in parts:
        part = part.strip()
        if part:
            # 移除化学计量数
            clean_part = re.sub(r'^\d+(?:\.\d+)?', '', part)
            clean_part = clean_part.strip()
            
            if clean_part:
                reactants.append(clean_part)
    
    return reactants


def process_csv_with_headers(input_file, output_file=None):
    """正确处理包含格式说明的CSV文件"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ 错误: 文件不存在: {input_file}")
        return False
    
    if output_file is None:
        output_file = input_file
    
    try:
        # 读取所有行
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) < 4:
            print("❌ 错误: CSV文件至少需要4行（3行格式说明 + 1行标题 + 数据行）")
            return False
        
        # 分离格式说明和数据
        format_lines = lines[:3]  # 前三行是格式说明
        data_lines = lines[3:]    # 从第4行开始是实际数据
        
        print(f"📋 文件结构:")
        print(f"  格式说明行: {len(format_lines)}")
        print(f"  数据行: {len(data_lines)}")
        
        # 处理数据部分
        data_content = ''.join(data_lines)
        reader = csv.reader(data_content.strip().split('\n'))
        
        rows = list(reader)
        
        if len(rows) < 2:
            print("❌ 错误: 数据部分至少需要标题行和一行数据")
            return False
        
        print(f"📊 数据部分:")
        print(f"  标题行: {rows[0]}")
        print(f"  数据行数: {len(rows) - 1}")
        
        # 获取标题行
        headers = rows[0]
        
        # 找到列索引
        try:
            equation_idx = headers.index('reaction_equation')
            reactants_idx = headers.index('reactants')
            print(f"✅ 找到列: reaction_equation={equation_idx}, reactants={reactants_idx}")
        except ValueError as e:
            print(f"❌ 错误: 找不到列 {e}")
            print(f"可用列: {headers}")
            return False
        
        # 处理数据行
        updated_rows = [headers]  # 保留标题行
        processed_count = 0
        
        for row_num, row in enumerate(rows[1:], 1):  # 跳过标题行
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
                row[reactants_idx] = reactants_str
                
                print(f"  行 {row_num}: '{current_reactants}' → '{reactants_str}'")
                if equation:
                    print(f"    方程式: {equation}")
                
                processed_count += 1
            else:
                print(f"  行 {row_num}: 跳过 - 列数不足")
            
            updated_rows.append(row)
        
        # 写回文件
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            # 写入原始格式说明
            for line in format_lines:
                f.write(line)
            
            # 写入处理后的数据
            writer = csv.writer(f)
            for row in updated_rows:
                # 确保所有列都被正确引用
                f.write(','.join(f'"{field}"' if ',' in str(field) or '\n' in str(field) else str(field) for field in row) + '\n')
        
        print(f"✅ 成功处理 {processed_count} 行数据")
        print(f"📁 结果已保存到: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 处理错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_file_structure(input_file):
    """显示文件结构，帮助调试"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ 文件不存在: {input_file}")
        return
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"📁 文件: {input_file}")
        print(f"总行数: {len(lines)}")
        print()
        
        for i, line in enumerate(lines, 1):
            print(f"第{i}行: {line.rstrip()}")
        
        print()
        print("=" * 50)
        print("分析结果:")
        
        if len(lines) >= 4:
            format_part = lines[:3]
            data_part = lines[3:]
            
            print(f"格式说明行: 第1-3行")
            print(f"数据开始行: 第4行")
            
            if len(data_part) >= 1:
                # 分析数据部分
                data_content = ''.join(data_part)
                reader = csv.reader(data_content.strip().split('\n'))
                rows = list(reader)
                
                if rows:
                    print(f"数据部分标题: {rows[0]}")
                    print(f"数据行数: {len(rows) - 1}")
                    
                    headers = rows[0]
                    if 'reaction_equation' in headers and 'reactants' in headers:
                        print("✅ 列结构正确")
                    else:
                        print("❌ 列结构有问题")
                        print(f"可用列: {headers}")
        
    except Exception as e:
        print(f"❌ 读取错误: {e}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("🔧 化学方程式反应物回填工具 - 最终修复版")
        print()
        print("用法:")
        print("  python working_fix.py <csv文件路径>")
        print("  python working_fix.py <csv文件路径> [输出文件路径]")
        print("  python working_fix.py --show <csv文件路径>")
        print()
        print("示例:")
        print("  python working_fix.py correct_reactions.csv")
        print("  python working_fix.py input.csv output.csv")
        print("  python working_fix.py --show correct_reactions.csv")
        return
    
    # 处理显示文件结构模式
    if len(sys.argv) == 3 and sys.argv[1] == '--show':
        show_file_structure(sys.argv[2])
        return
    
    # 处理正常模式
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🚀 开始处理: {input_file}")
    success = process_csv_with_headers(input_file, output_file)
    
    if success:
        print("✅ 处理完成！")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()