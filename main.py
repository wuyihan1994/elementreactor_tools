import sys
from pathlib import Path

# 使用最终工作版本
from reaction_backfill import process_csv_actual_format


def main():
    if len(sys.argv) != 2:
        print("🔧 化学方程式反应物回填工具")
        print()
        print("用法: python main.py <csv文件路径>")
        print("示例: python main.py correct_reactions.csv")
        return
    
    csv_file = sys.argv[1]
    
    if not Path(csv_file).exists():
        print(f"❌ 错误: 文件 '{csv_file}' 不存在")
        return
    
    success = process_csv_actual_format(csv_file)
    
    if success:
        print("✅ 处理完成！")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
