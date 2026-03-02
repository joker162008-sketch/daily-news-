#!/usr/bin/env python3
"""
科技/AI 资讯抓取脚本
抓取过去24小时最重要的科技和AI资讯
通过 Discord Webhook 推送
"""

import requests
import json
import os
from datetime import datetime
from typing import List, Dict

# ======== 配置 ========
# Discord Webhook 配置
# 在 Discord 服务器设置 -> 整合 -> Webhook 创建一个 Webhook
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL', '')


def get_hackernews_top_news(limit: int = 10) -> List[Dict]:
    """从 Hacker News 获取科技新闻"""
    try:
        ids_response = requests.get(
            "https://hacker-news.firebase.io/v0/topstories.json",
            timeout=15
        )
        story_ids = ids_response.json()[:limit]
        
        news_list = []
        for story_id in story_ids:
            story_response = requests.get(
                f"https://hacker-news.firebase.io/v0/item/{story_id}.json",
                timeout=10
            )
            story = story_response.json()
            if story and story.get('url'):
                news_list.append({
                    'title': story.get('title', ''),
                    'url': story.get('url', ''),
                    'source': 'Hacker News',
                    'score': story.get('score', 0)
                })
        return news_list
    except Exception as e:
        print(f"Hacker News API 错误: {e}")
        return []


def get_reddit_tech_news(limit: int = 8) -> List[Dict]:
    """从 Reddit 获取科技/AI 新闻"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (News Bot)'}
        subreddits = ['technology', 'artificial', 'MachineLearning']
        news_list = []
        
        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}"
            response = requests.get(url, headers=headers, timeout=15)
            data = response.json()
            
            if 'data' in data:
                for post in data['data']['children']:
                    post_data = post['data']
                    if post_data.get('url'):
                        news_list.append({
                            'title': post_data.get('title', ''),
                            'url': post_data.get('url', ''),
                            'source': f'Reddit r/{sub}',
                            'score': post_data.get('score', 0)
                        })
        
        news_list.sort(key=lambda x: x.get('score', 0), reverse=True)
        return news_list[:limit]
    except Exception as e:
        print(f"Reddit API 错误: {e}")
        return []


def get_devto_news(limit: int = 5) -> List[Dict]:
    """从 Dev.to 获取开发者科技新闻"""
    try:
        response = requests.get(
            f"https://dev.to/api/articles?per_page={limit}&top=1",
            timeout=15
        )
        articles = response.json()
        
        news_list = []
        for article in articles:
            news_list.append({
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'source': 'Dev.to',
                'reactions': article.get('public_reactions_count', 0)
            })
        return news_list
    except Exception as e:
        print(f"Dev.to API 错误: {e}")
        return []


def send_via_discord(message: str, webhook_url: str) -> bool:
    """通过 Discord Webhook 发送消息"""
    if not webhook_url:
        print("⚠️ 未配置 Discord Webhook URL")
        return False
    
    try:
        # 构建 Discord embed 消息
        data = {
            "content": message,
            "username": "科技资讯推送",
            "avatar_url": "https://i.imgur.com/AfFp7pu.png"
        }
        
        response = requests.post(webhook_url, json=data, timeout=30)
        
        print(f"Discord 响应: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print("✅ Discord 发送成功!")
            return True
        else:
            print(f"❌ Discord 发送失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Discord 错误: {e}")
        return False


def main():
    """主函数"""
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL', DISCORD_WEBHOOK_URL)
    
    print(f"⏰ 开始抓取资讯... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_news = []
    
    # 1. 获取 Hacker News
    print("📡 正在获取 Hacker News...")
    hn_news = get_hackernews_top_news(10)
    all_news.extend(hn_news)
    print(f"   获取到 {len(hn_news)} 条")
    
    # 2. 获取 Reddit
    print("📡 正在获取 Reddit...")
    reddit_news = get_reddit_tech_news(8)
    all_news.extend(reddit_news)
    print(f"   获取到 {len(reddit_news)} 条")
    
    # 3. 获取 Dev.to
    print("📡 正在获取 Dev.to...")
    devto_news = get_devto_news(5)
    all_news.extend(devto_news)
    print(f"   获取到 {len(devto_news)} 条")
    
    # 按评分排序
    all_news.sort(key=lambda x: x.get('score', 0) or x.get('reactions', 0), reverse=True)
    
    # 格式化消息
    message = "🚀 **每日科技/AI资讯**\n"
    message += f"📅 {datetime.now().strftime('%Y年%m月%d日')}\n\n"
    message += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if hn_news:
        message += "🔥 **Hacker News Top 10**\n"
        for i, news in enumerate(hn_news[:10], 1):
            title = news.get('title', '')[:50]
            if len(news.get('title', '')) > 50:
                title += "..."
            message += f"{i}. {title}\n"
        message += "\n"
    
    if reddit_news:
        message += "🔵 **Reddit 热门**\n"
        for i, news in enumerate(reddit_news[:5], 1):
            title = news.get('title', '')[:50]
            if len(news.get('title', '')) > 50:
                title += "..."
            message += f"{i}. {title}\n"
        message += "\n"
    
    if devto_news:
        message += "💻 **Dev.to 热门**\n"
        for i, news in enumerate(devto_news[:3], 1):
            title = news.get('title', '')[:50]
            if len(news.get('title', '')) > 50:
                title += "..."
            message += f"{i}. {title}\n"
    
    message += "\n━━━━━━━━━━━━━━━━━━━━\n"
    message += "🤖 由 GitHub Actions 自动推送"
    
    print("\n📝 消息内容:")
    print(message)
    
    # 发送消息
    if webhook_url:
        print("\n📤 通过 Discord 发送消息...")
        send_via_discord(message, webhook_url)
    else:
        print("\n⚠️ 未配置 Discord Webhook URL")
    
    # 输出 JSON
    with open('news_output.json', 'w', encoding='utf-8') as f:
        json.dump({
            'message': message,
            'news_count': len(all_news),
            'timestamp': datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 完成! 共获取 {len(all_news)} 条资讯")


if __name__ == "__main__":
    main()
