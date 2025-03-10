import asyncio
import random
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import (
    save_games_to_csv,
)
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()  # 加载环境变量


async def crawl_games():
    """
    主函数：从目标网站爬取游戏数据
    """
    # 初始化配置
    browser_config = get_browser_config()  # 获取浏览器配置
    llm_strategy = get_llm_strategy()  # 初始化大语言模型策略
    session_id = "games_crawl_session"  # 定义爬虫会话ID

    # 初始化状态变量
    i = 0
    page_number = 1  # 起始页码
    all_games = []  # 存储所有游戏数据
    seen_names = set()  # 记录已抓取的游戏名称

    # 启动异步爬虫上下文（参考文档：https://docs.crawl4ai.com/api/async-webcrawler/#asyncwebcrawler）
    async with AsyncWebCrawler(config=browser_config) as crawler:
        while True:
            # 根据页码动态生成请求URL
            URL = f"{BASE_URL}?page={page_number}&start={(page_number - 1) * 10}"

            # 抓取并处理当前页面
            games, no_results_found = await fetch_and_process_page(
                crawler,
                page_number,
                URL,
                CSS_SELECTOR,
                llm_strategy,
                session_id,
                REQUIRED_KEYS,
                seen_names,
            )

            # 终止条件判断
            if not games:
                print(f"第 {page_number} 页未提取到游戏数据")
                break

            # 数据聚合
            all_games.extend(games)  # 将当前页数据加入总列表
            page_number += 1  # 页码递增
            i += 1

            # 礼貌性暂停，避免触发速率限制
            await asyncio.sleep(2 + random.uniform(0, 3))  # 随机延时2-5秒

            # 安全终止条件（最多抓取10页）
            if page_number == 11:
                break

    # 数据持久化
    if all_games:
        save_games_to_csv(all_games, "complete_games.csv")
        print(f"已保存 {len(all_games)} 条游戏数据至 'complete_games.csv'")
    else:
        print("本次爬取未发现有效游戏数据")

    # 展示大语言模型使用统计
    llm_strategy.show_usage()


async def main():
    """
    脚本入口点
    """
    await crawl_games()


if __name__ == "__main__":
    asyncio.run(main())