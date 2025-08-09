import sys
from pathlib import Path

from elementreactor_tools import ReactionBackfiller


def main():
    if len(sys.argv) != 2:
        print("用法: python main.py <csv文件路径>")
        print("示例: python main.py example_reactions.csv")
        return
    
    csv_file = sys.argv[1]
    
    if not Path(csv_file).exists():
        print(f"错误: 文件 '{csv_file}' 不存在")
        return
    
    backfiller = ReactionBackfiller(csv_file)
    result = backfiller.process_file()
    
    if result['success']:
        print(f"✅ 处理成功: {result['message']}")
    else:
        print(f"❌ 处理失败: {result['message']}")


if __name__ == "__main__":
    main()
