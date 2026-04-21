---
name: Fajo-analyze
description: Analyze Fajo campaign event data from JSON files with user behavior tracking. Generate visualization charts (PNG) and markdown reports. Use when processing event-report.json files that contain: user ID, date, eventType fields. Focuses on metrics: total events, channel distribution, participant counts, completion rates, sharing statistics, and coupon usage.
---

# Fajo Event Data Analysis

## Quick Start

Run analysis on event data:

```bash
python scripts/analyze.py
```

This expects `event-report.json` in the current directory with event data.

## Workflow

1. **Check for existing script** - If `analyze.py` exists, use it directly
2. **Load data** - Parse `event-report.json` containing user events
3. **Calculate metrics** - Compute key indicators for the campaign
4. **Generate visualizations** - Create PNG charts with Chinese font support
5. **Output report** - Save markdown report and charts to date-named folder

## Key Metrics

The analysis generates these metrics:

- **Total events** - Sum of all event records
- **Channel distribution** - Breakdown by entry source (小程序banner, 电视广告机, 社群广告图, share, DEV)
- **Participants** - Unique users who answered at least one question
- **Completers** - Unique users who submitted all answers
- **Completion rate** - Percentage of participants who completed
- **Shares** - Times result page was shared
- **Shared opens** - Times shared links were opened
- **Coupons** - Coupon claims broken down by type (问答结果页, 抽奖结果页)

## Output Files

Generated in folder named: `Fajo2026步履新生-{start_date}至{end_date}/`

- `report.md` - Markdown report with all metrics
- `event_counts.png` - Horizontal bar chart of event types (descending)
- `channel_distribution.png` - Pie chart of channel sources (descending)
- `coupon_counts.png` - Bar chart of coupon claims (if coupons > 0)

## Data Format

`event-report.json` contains array of records:

```json
[
    {
        "date": "2026-03-02",
        "eventType": "活动首页小程序banner",
        "uid": " SH91870"
    }
]
```

## References

- **event-describe.md** - Complete event type definitions and workflow documentation
- **prompt.md** - Detailed analysis requirements and metric specifications

Load these references when:
- Need to understand event type meanings
- Need to verify metric calculation logic
- Need to understand user flow and reporting triggers

## Font Configuration

Charts use Chinese-friendly fonts to prevent encoding issues:
- Arial Unicode MS (macOS)
- SimHei (Windows)
- DejaVu Sans (Linux fallback)

## Troubleshooting

**Charts show garbled Chinese text**
→ Font not available on system. Add fallback fonts in matplotlib config.

**Empty output folder**
→ Check event-report.json exists and contains valid data.

**Missing visualizations**
→ Verify matplotlib and dependencies are installed: `pip install matplotlib`

**Incorrect event counts**
→ Ensure event types in analyze.py match event-describe.md definitions.
