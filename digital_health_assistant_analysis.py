"""
数字健康助手 - 数据分析脚本
Author: 江雨萱
Description: 社交媒体使用行为与心理压力关系分析
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==================== 配置 ====================
print("=" * 60)
print("数字健康助手 - 数据分析脚本")
print("=" * 60)

# 设置图表样式
sns.set_style("whitegrid")

# ==================== 1. 数据加载 ====================
print("\n[1/4] 加载数据")
try:
    df = pd.read_excel('mental_health_social_media_datasets.xlsx')
    print("数据加载成功")
    print(f"数据集形状: {df.shape[0]} 行 × {df.shape[1]} 列")
except FileNotFoundError:
    print("文件未找到: 'mental_health_social_media_datasets.xlsx'")
    print(f"当前目录: {os.getcwd()}")
    exit()

# ==================== 2. 数据清洗与特征工程 ====================
print("\n[2/4] 数据清洗与特征工程")

# 核心字段选择
core_columns = [
    'social_media_time_min',
    'sleep_hours',
    'negative_interactions_count',
    'positive_interactions_count',
    'stress_level',
    'anxiety_level',
    'mood_level'
]

# 创建清洗后的数据集
cleaned_df = df[core_columns].copy()

# 保存清洗数据
cleaned_df.to_csv('cleaned_behavior_data.csv', index=False)
print("已保存清洗数据: cleaned_behavior_data.csv")
print(f"保留字段数: {len(core_columns)}")

# 计算关键阈值
threshold_social = df['social_media_time_min'].quantile(0.75)  # 231分钟，75分位数
threshold_sleep = df['sleep_hours'].quantile(0.25)             # 6.7小时，25分位数
median_social = df['social_media_time_min'].median()          # 170分钟，中位数

print("\n关键阈值计算:")
print(f"重度使用阈值: {threshold_social:.0f} 分钟 (75分位数)")
print(f"睡眠不足阈值: {threshold_sleep:.1f} 小时 (25分位数)")
print(f"常规使用阈值: {median_social:.0f} 分钟 (中位数)")

# ==================== 3. 用户分群 ====================
print("\n[3/4] 用户分群分析")

# 高风险群体定义
high_risk_condition = (
    (df['social_media_time_min'] > threshold_social) &
    (df['sleep_hours'] < threshold_sleep) &
    (df['negative_interactions_count'] > 0)
)
high_risk_group = df[high_risk_condition]

# 低风险群体定义
low_risk_condition = (
    (df['social_media_time_min'] <= median_social) &
    (df['sleep_hours'] >= 7) &
    (df['negative_interactions_count'] == 0)
)
low_risk_group = df[low_risk_condition]

print(f"高风险群体人数: {len(high_risk_group)}")
print(f"低风险群体人数: {len(low_risk_group)}")

# 计算核心指标
high_risk_stress = high_risk_group['stress_level'].mean()
low_risk_stress = low_risk_group['stress_level'].mean()
stress_diff = high_risk_stress - low_risk_stress

high_risk_anxiety = high_risk_group['anxiety_level'].mean()
low_risk_anxiety = low_risk_group['anxiety_level'].mean()
anxiety_diff = high_risk_anxiety - low_risk_anxiety

# 效应量计算
pooled_std = np.sqrt((high_risk_group['stress_level'].std()**2 + low_risk_group['stress_level'].std()**2) / 2)
cohens_d = stress_diff / pooled_std

print("\n核心指标对比:")
print(f"压力水平 - 高风险组: {high_risk_stress:.2f} | 低风险组: {low_risk_stress:.2f} | 差异: {stress_diff:.2f}")
print(f"焦虑水平 - 高风险组: {high_risk_anxiety:.2f} | 低风险组: {low_risk_anxiety:.2f} | 差异: {anxiety_diff:.2f}")
print(f"效应量 (Cohen's d): {cohens_d:.2f}")

# ==================== 4. 可视化 ====================
print("\n[4/4] 生成可视化图表")

# 图表1：压力水平对比
plt.figure(figsize=(10, 6))
categories = [f'High-Risk Group\n(n={len(high_risk_group)})', f'Low-Risk Group\n(n={len(low_risk_group)})']
stress_values = [high_risk_stress, low_risk_stress]
bars = plt.bar(categories, stress_values, color=['#ff6b6b', '#48dbfb'], edgecolor='black', linewidth=1.5)

plt.title('Comparison of Average Stress Levels\nBetween High-Risk and Low-Risk User Groups',
          fontsize=14, fontweight='bold', pad=20)
plt.ylabel('Average Stress Level (Score, 5-9)', fontsize=12, labelpad=10)
plt.xlabel('User Group (Defined by Behavior Pattern)', fontsize=12, labelpad=10)

for bar, value in zip(bars, stress_values):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.05, f'{value:.2f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold', color='black')

plt.ylim(0, 10)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('FINAL_chart_stress_comparison.png', dpi=300, bbox_inches='tight')
print("图表1已保存: FINAL_chart_stress_comparison.png")

# 图表2：焦虑水平对比
plt.figure(figsize=(10, 6))
anxiety_values = [high_risk_anxiety, low_risk_anxiety]
bars = plt.bar(categories, anxiety_values, color=['#ff9f43', '#1dd1a1'], edgecolor='black', linewidth=1.5)

plt.title('Comparison of Average Anxiety Levels\nBetween High-Risk and Low-Risk User Groups',
          fontsize=14, fontweight='bold', pad=20)
plt.ylabel('Average Anxiety Level (Score)', fontsize=12, labelpad=10)
plt.xlabel('User Group (Defined by Behavior Pattern)', fontsize=12, labelpad=10)

for bar, value in zip(bars, anxiety_values):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.05, f'{value:.2f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold', color='black')

plt.ylim(0, max(anxiety_values)*1.3)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('FINAL_chart_anxiety_comparison.png', dpi=300, bbox_inches='tight')
print("图表2已保存: FINAL_chart_anxiety_comparison.png")

# 图表3：行为分布与阈值
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

axes[0].hist(df['social_media_time_min'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
axes[0].axvline(threshold_social, color='red', linestyle='--', linewidth=2.5,
                label=f'High-Risk Threshold: {threshold_social:.0f} min\n(75th Percentile)')
axes[0].axvline(median_social, color='orange', linestyle=':', linewidth=2,
                label=f'Low-Risk Threshold: {median_social:.0f} min\n(Median)')
axes[0].set_xlabel('Social Media Usage Time (minutes)', fontsize=11)
axes[0].set_ylabel('Frequency (User Count)', fontsize=11)
axes[0].set_title('Distribution of Social Media Usage Time\nwith Risk Thresholds', fontsize=12, fontweight='bold')
axes[0].legend(loc='upper right', fontsize=9)
axes[0].grid(alpha=0.3)

axes[1].hist(df['sleep_hours'], bins=30, color='lightgreen', edgecolor='black', alpha=0.7)
axes[1].axvline(threshold_sleep, color='red', linestyle='--', linewidth=2.5,
                label=f'High-Risk Threshold: {threshold_sleep:.1f} hours\n(25th Percentile)')
axes[1].axvline(7, color='orange', linestyle=':', linewidth=2,
                label='Low-Risk Threshold: 7.0 hours\n(Recommended Minimum)')
axes[1].set_xlabel('Sleep Duration (hours)', fontsize=11)
axes[1].set_ylabel('Frequency (User Count)', fontsize=11)
axes[1].set_title('Distribution of Sleep Duration\nwith Risk Thresholds', fontsize=12, fontweight='bold')
axes[1].legend(loc='upper left', fontsize=9)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('FINAL_chart_behavior_distribution.png', dpi=300, bbox_inches='tight')
print("图表3已保存: FINAL_chart_behavior_distribution.png")

# 图表4：相关性热力图
plt.figure(figsize=(10, 8))
corr_matrix = cleaned_df.corr(numeric_only=True)
heatmap = sns.heatmap(corr_matrix,
                      annot=True,
                      fmt=".2f",
                      cmap='coolwarm',
                      center=0,
                      square=True,
                      linewidths=1,
                      cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix: Behavior Indicators vs Psychological States',
          fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('FINAL_chart_correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("图表4已保存: FINAL_chart_correlation_heatmap.png")

# ==================== 5. 分析总结 ====================
print("\n" + "="*60)
print("分析完成")
print("="*60)
print(f"高风险群体: {len(high_risk_group)} 人，压力水平 {high_risk_stress:.2f}")
print(f"低风险群体: {len(low_risk_group)} 人，压力水平 {low_risk_stress:.2f}")
print(f"压力差异: {stress_diff:.2f} 分 (效应量 d={cohens_d:.2f})")
print("\n生成文件:")
print("- cleaned_behavior_data.csv")
print("- FINAL_chart_stress_comparison.png")
print("- FINAL_chart_anxiety_comparison.png")
print("- FINAL_chart_behavior_distribution.png")
print("- FINAL_chart_correlation_heatmap.png")
print("="*60)