import os
import itertools
import heapq  # 用于维护 Top N 个最频繁的组合
from collections import Counter
import openpyxl

def find_cooccurring_species_optimized(folder_path, max_combo_size=5, top_n=1000):
    """
    查找指定文件夹中共同出现的物种组合，组合大小不超过 max_combo_size，优化内存使用。

    Args:
        folder_path: 包含物种 XML 文件的文件夹路径。
        max_combo_size: 物种组合的最大大小。
        top_n: 返回最频繁的共现物种组合的数量。

    Returns:
        一个包含最频繁共现物种组合的列表，每个组合是一个 frozenset。
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"指定的文件夹路径不存在: {folder_path}")

    # 获取文件夹中所有的 XML 文件名（即物种名）
    all_species = sorted([f.replace(".xml", "") for f in os.listdir(folder_path) if f.endswith(".xml")])
    num_species = len(all_species)
    print(f"文件夹中共有 {num_species} 个物种。")

    co_occurrence_counts = Counter()

    # 迭代生成不同大小的物种组合，最大不超过 max_combo_size
    for r in range(2, max_combo_size + 1):
        print(f"正在生成大小为 {r} 的组合...")
        for combo_tuple in itertools.combinations(all_species, r):
            combo = frozenset(combo_tuple)
            co_occurrence_counts[combo] += 1

    print(f"共找到 {len(co_occurrence_counts)} 种不同的物种组合。")

    # 获取最频繁的 top_n 个组合
    most_common_combinations = co_occurrence_counts.most_common(top_n)

    return [combo for combo, count in most_common_combinations]

def generate_excel_output_optimized(co_occurrences, output_filename="cooccurrence_communities.xlsx"):
    """
    将共现物种组合写入 Excel 文件，优化内存使用。

    Args:
        co_occurrences: 一个包含共现物种组合的列表 (frozenset)。
        output_filename: 输出 Excel 文件的名称。
    """
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Co-occurring Communities"

    # 写入表头
    sheet.append(["Community", "Species"])

    for i, combo in enumerate(co_occurrences):
        community_name = f"community{i+1}"
        for species in sorted(list(combo)):
            sheet.append([community_name, species])

    try:
        workbook.save(output_filename)
        print(f"\n结果已保存到 Excel 文件: {output_filename}")
    except Exception as e:
        print(f"保存 Excel 文件时出错: {e}")

if __name__ == "__main__":
    folder_path = "DL_all"  # 替换成你的文件夹路径
    max_combo_size = 5
    top_n = 1000

    try:
        top_cooccurrences = find_cooccurring_species_optimized(folder_path, max_combo_size, top_n)

        print(f"\n找到最常见的 {len(top_cooccurrences)} 个物种组合（大小不超过 {max_combo_size}）。")

        # 打印一些结果来验证是否包含大小大于 2 的组合
        for combo in top_cooccurrences[:10]:
            print(f"组合大小: {len(combo)}, 物种: {combo}")

        generate_excel_output_optimized(top_cooccurrences)

    except ValueError as e:
        print(f"错误: {e}")