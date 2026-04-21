import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter
from typing import Dict, List, Tuple
import os

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_data(filepath: str) -> List[Dict]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_date_range(data: List[Dict]) -> Tuple[str, str]:
    dates = sorted(set(item['date'] for item in data))
    if not dates:
        return ('', '')
    return (dates[0], dates[-1])

def create_output_folder(date_start: str, date_end: str) -> str:
    folder_name = f"Fajo2026步履新生-{date_start}至{date_end}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def count_events(data: List[Dict]) -> Dict[str, int]:
    events = [item['eventType'] for item in data]
    return Counter(events)

def count_channel_distribution(data: List[Dict]) -> Dict[str, int]:
    channel_events = ['活动首页小程序banner', '活动首页电视广告机', '活动首页社群广告图', '活动首页share', '活动首页DEV']
    channels = [item['eventType'] for item in data if item['eventType'] in channel_events]
    channel_names = [c.replace('活动首页', '') for c in channels]
    channel_names = ['DEV' if c == '' else c for c in channel_names]
    return Counter(channel_names)

def count_participants(data: List[Dict]) -> int:
    answer_events = ['问答1', '问答2', '问答3', '问答4']
    uids = set()
    for item in data:
        if item['eventType'] in answer_events:
            uids.add(item['uid'].strip())
    return len(uids)

def count_completers(data: List[Dict]) -> int:
    complete_events = ['问答提交', '问答完毕']
    uids = set()
    for item in data:
        if item['eventType'] in complete_events:
            uids.add(item['uid'].strip())
    return len(uids)

def count_shares(data: List[Dict]) -> int:
    return sum(1 for item in data if item['eventType'] == '问答结果页分享')

def count_shared_opens(data: List[Dict]) -> int:
    return sum(1 for item in data if item['eventType'] == '问答分享被打开')

def count_coupons(data: List[Dict]) -> Dict[str, int]:
    qa_coupons = sum(1 for item in data if item['eventType'] == '问答结果页领券')
    lottery_coupons = sum(1 for item in data if item['eventType'] == '抽奖结果页领券')
    return {'问答结果页领券': qa_coupons, '抽奖结果页领券': lottery_coupons, '总计': qa_coupons + lottery_coupons}

def plot_event_counts(event_counts: Dict[str, int], output_folder: str):
    sorted_events = sorted(event_counts.items(), key=lambda x: x[1], reverse=True)
    events = [item[0] for item in sorted_events]
    counts = [item[1] for item in sorted_events]
    
    plt.figure(figsize=(14, 6))
    bars = plt.barh(events, counts, color='steelblue')
    plt.xlabel('次数', fontsize=12)
    plt.ylabel('事件类型', fontsize=12)
    plt.title('各事件类型统计（按数量降序）', fontsize=14, fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    
    for bar, count in zip(bars, counts):
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{count}',
                ha='left', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(output_folder, 'event_counts.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_channel_distribution(channel_dist: Dict[str, int], output_folder: str):
    sorted_channels = sorted(channel_dist.items(), key=lambda x: x[1], reverse=True)
    channels = [item[0] for item in sorted_channels]
    counts = [item[1] for item in sorted_channels]
    
    plt.figure(figsize=(10, 6))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    result = plt.pie(counts, labels=channels, autopct='%1.1f%%', 
                     colors=colors[:len(channels)], startangle=90)
    if len(result) > 2:
        wedges, texts, autotexts = result
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    plt.title('渠道来源占比（按数量降序）', fontsize=14, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    output_path = os.path.join(output_folder, 'channel_distribution.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_coupons(coupon_counts: Dict[str, int], output_folder: str):
    items = ['问答结果页领券', '抽奖结果页领券']
    counts = [coupon_counts['问答结果页领券'], coupon_counts['抽奖结果页领券']]
    
    plt.figure(figsize=(10, 6))
    colors = ['#FF6B6B', '#4ECDC4']
    bars = plt.bar(items, counts, color=colors)
    plt.xlabel('领券类型', fontsize=12)
    plt.ylabel('次数', fontsize=12)
    plt.title('领券次数统计', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(output_folder, 'coupon_counts.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def generate_report(data: List[Dict]):
    date_start, date_end = get_date_range(data)
    output_folder = create_output_folder(date_start, date_end)
    
    event_counts = count_events(data)
    total_events = len(data)
    
    channel_dist = count_channel_distribution(data)
    
    participants = count_participants(data)
    
    completers = count_completers(data)
    
    shares = count_shares(data)
    
    shared_opens = count_shared_opens(data)
    
    coupons = count_coupons(data)
    
    report = f"""
# Fajo-2026步履新生活动数据分析报告

## 概览
- 总事件数: {total_events}
- 数据日期范围: {date_start} 至 {date_end}

## 事件类型统计（按数量降序）
"""
    for event, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
        report += f"- {event}: {count} 次\n"
    
    report += f"""
## 渠道来源占比（按数量降序）
"""
    for channel, count in sorted(channel_dist.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / sum(channel_dist.values())) * 100 if channel_dist else 0
        report += f"- {channel}: {count} 次 ({percentage:.1f}%)\n"
    
    report += f"""
## 用户参与情况
- 参与答题人数: {participants} 人
- 完成答题人数: {completers} 人
- 完成率: {(completers/participants*100) if participants > 0 else 0:.1f}%

## 分享情况
- 问答结果页分享次数: {shares} 次
- 问答分享被打开次数: {shared_opens} 次

## 领券情况
- 问答结果页领券: {coupons['问答结果页领券']} 次
- 抽奖结果页领券: {coupons['抽奖结果页领券']} 次
- 总计领券次数: {coupons['总计']} 次
"""
    
    plot_event_counts(event_counts, output_folder)
    plot_channel_distribution(channel_dist, output_folder)
    
    if coupons['总计'] > 0:
        plot_coupons(coupons, output_folder)
    
    report_path = os.path.join(output_folder, 'report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("=" * 60)
    print("分析完成！")
    print("=" * 60)
    print(f"输出文件夹: {output_folder}/")
    print(f"已生成以下文件:")
    print(f"  - report.md: 数据分析报告")
    print(f"  - event_counts.png: 事件类型统计图")
    print(f"  - channel_distribution.png: 渠道来源占比图")
    if coupons['总计'] > 0:
        print(f"  - coupon_counts.png: 领券次数统计图")
    print("=" * 60)
    print(f"\n关键指标:")
    print(f"总事件数: {total_events}")
    print(f"参与答题人数: {participants}")
    print(f"完成答题人数: {completers}")
    print(f"问答结果页分享次数: {shares}")
    print(f"问答分享被打开次数: {shared_opens}")
    print(f"总计领券次数: {coupons['总计']}")

if __name__ == '__main__':
    data = load_data('event-report.json')
    generate_report(data)
