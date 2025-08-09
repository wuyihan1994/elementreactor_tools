import csv
import re
from pathlib import Path
from typing import List, Dict, Any


class ChemicalEquationParser:
    """化学方程式解析器"""
    
    @staticmethod
    def parse_reactants(equation: str) -> List[str]:
        """从化学方程式中提取反应物列表
        
        方程格式: "A + B -> C + D" 或 "A+B→C+D"
        返回: ["A", "B"] 形式的反应物列表
        """
        if not equation:
            return []
            
        # 替换箭头符号
        equation = equation.replace('→', '->').replace('=', '->')
        
        # 分割反应物和产物
        if '->' not in equation:
            return []
            
        reactants_side = equation.split('->')[0].strip()
        
        # 分割反应物
        reactants = []
        for reactant in re.split(r'[\+\s]+', reactants_side):
            reactant = reactant.strip()
            if reactant:
                # 移除系数
                reactant = re.sub(r'^\d+', '', reactant)
                reactant = re.sub(r'^\d+\.\d+', '', reactant)
                reactant = reactant.strip()
                if reactant:
                    reactants.append(reactant)
        
        return reactants


class CSVProcessor:
    """CSV文件处理器"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        
    def read_csv(self) -> List[Dict[str, Any]]:
        """读取CSV文件，跳过前三行（列名、中文名称、数据类型）"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"文件不存在: {self.file_path}")
            
        data = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            # 跳过前三行
            for _ in range(3):
                next(f, None)
            
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))
                
        return data
    
    def write_csv(self, data: List[Dict[str, Any]], output_path: str = None):
        """将处理后的数据写回CSV文件"""
        if output_path is None:
            output_path = self.file_path
            
        # 读取原始文件的前三行
        original_header = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < 3:
                    original_header.append(line.strip())
                else:
                    break
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            # 写入原始前三行
            for line in original_header:
                f.write(line + '\n')
            
            # 写入数据
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)


class ReactionBackfiller:
    """反应物回填器"""
    
    def __init__(self, csv_file: str):
        self.csv_processor = CSVProcessor(csv_file)
        self.parser = ChemicalEquationParser()
    
    def process_file(self) -> Dict[str, Any]:
        """处理整个CSV文件"""
        try:
            data = self.csv_processor.read_csv()
            processed_rows = 0
            
            for row in data:
                equation = row.get('reaction_equation', '')
                if equation:
                    reactants = self.parser.parse_reactants(equation)
                    row['reactants'] = '|'.join(reactants)
                    processed_rows += 1
            
            self.csv_processor.write_csv(data)
            
            return {
                'success': True,
                'processed_rows': processed_rows,
                'total_rows': len(data),
                'message': f'成功处理 {processed_rows}/{len(data)} 行数据'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'处理失败: {str(e)}'
            }


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) != 2:
        print("用法: python elementreactor_tools.py <csv文件路径>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    try:
        backfiller = ReactionBackfiller(csv_file)
        result = backfiller.process_file()
        
        if result['success']:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['message']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()