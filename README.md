# cibo.hk — HK IPO Allotment API & MCP Server

面向 AI Agent 与开发者的**港股 IPO 中签分析**数据服务。提供两种接入方式：**REST API**（公开 JSON 端点）与 **MCP Server**（远程 Streamable HTTP，免安装）。

- 网站：https://cibo.hk
- 权威文档：https://cibo.hk/llms.txt （本 README 是其镜像，以 llms.txt 为准）
- API 清单：https://cibo.hk/api/
- MCP 端点：https://cibo.hk/mcp

> 由熊猫证券 CEO JW 用 AI 辅助编程构建。预测港股 IPO 中签率（可调申购倍数与 α 分配系数），
> 并从过户处 ID 数据推断中签者画像（地区 / 国籍 / 性别 / 年龄），含港股通纳入分析、配发结果、
> 国际配售、基石、全市场财务等。

---

## 两种接入方式

### 1. REST API（公开，无需鉴权）

- Base URL：`https://cibo.hk`
- 前缀：`/api`
- Content-Type：`application/json`
- 所有公开数据端点无需 API key / JWT。免费限流：每 IP 30 次/分钟，5,000 次/天。
- 个性化功能（自选股 / 偏好）需 pcell.si JWT，见 `/.well-known/agent-protocol`。

### 2. MCP Server（远程 Streamable HTTP，免安装）

**57 个工具**，覆盖全站数据：中签预测、招股书、配发结果（含国际配售）、中签画像、
公告中心、回购/增减持、港股通纳入、机构排名、A/B 对比、市场数据、快讯、披露易、
全市场财务与公司目录、价格、过户处研究、博客、海力士套利、A 股 ETF 资金流、
数据中心宏观 / 美股数据。

| 项 | 值 |
|----|----|
| Endpoint | `https://cibo.hk/mcp` |
| Transport | `streamable-http` |
| 安装 | 无需 pip install，直接连接 |

MCP 配置示例：

```json
{
  "mcpServers": {
    "cibo": { "url": "https://cibo.hk/mcp" }
  }
}
```

---

## 快速开始

```bash
# 列出所有 IPO 股票
curl -s 'https://cibo.hk/api/stocks' | python3 -m json.tool

# 单只股票完整分析（申购、档位、盈亏、CCASS 画像）
curl -s 'https://cibo.hk/api/stocks/06872/overview' | python3 -m json.tool

# 中签预测（默认参数）
curl -s 'https://cibo.hk/api/stocks/06872/predict' | python3 -m json.tool

# 任意参数的按需预测：1600 倍申购、α=0.5
curl -s 'https://cibo.hk/api/stocks/06802/predict/custom?oversub=1600&alpha=0.5' | python3 -m json.tool

# 配发结果（含国际配售、基石、甲乙组档位）
curl -s 'https://cibo.hk/api/stocks/06872/allotment-result' | python3 -m json.tool
```

---

## REST API 端点（47 个）

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/stocks` | public | List all IPO stocks with basic info (code, name, listing date). |
| GET | `/api/stocks/oversub` | public | Batch oversubscription + frozen capital for all stocks. Query: `?year=2026`. |
| GET | `/api/stocks/index` | public | Stock cards grouped by index with filtering, pagination, search. |
| GET | `/api/stocks/homepage` | public | Homepage stock cards: upcoming (prelist) and recently listed. |
| GET | `/api/flash-events` | public | Derived flash-event feed (ipo_launch / allotment_result / listing / inclusion / prediction). |
| GET | `/api/stocks/{code}/overview` | public | Full per-stock IPO analysis: subscription rates, allotment tiers, PnL scenarios, CCASS demographics. |
| GET | `/api/stocks/{code}/prospectus` | public | Prospectus details (offer price, mechanism, greenshoe, secondary listing), cornerstone investors, IPO financial statements. |
| GET | `/api/stocks/{code}/allotment-result` | public | Allotment summary (incl. international placing, greenshoe), placing concentration, cornerstone + lock-up, Pool A/B tiers. |
| GET | `/api/stocks/{code}/allottee-profile` | public | 中签画像: winner demographics from registrar ID data — region/nationality, gender, age histogram + pyramid, HK ID letter/era/district. |
| GET | `/api/stocks/{code}/announcements` | public | 个股公告中心: all HKEXnews announcements for one stock, grouped by headline category. |
| GET | `/api/stocks/{code}/buyback` | public | 回购明细: share buyback records for one stock, newest first, with totals. |
| GET | `/api/stocks/{code}/disclosure` | public | 增减持明细: disclosure-of-interest records for one stock, newest first. |
| GET | `/api/stocks/{code}/summary` | public | Lightweight stock summary: key stats and tier classification. |
| GET | `/api/stocks/{code}/ccass` | public | CCASS custodian demographics: type, province, gender, age distributions. |
| GET | `/api/stocks/{code}/narrative` | public | AI-generated narrative (zh/en) summarizing the IPO's key characteristics. |
| GET | `/api/stocks/compare` | public | Side-by-side comparison of up to 10 stocks. Query: `?codes=00001,00002`. |
| GET | `/api/allotment-tiers/{code}` | public | Detailed allotment tier table: Pool A and Pool B subscription tiers. |
| GET | `/api/stocks/{code}/predict` | public | Full allotment prediction data (default predicted oversub/alpha). |
| GET | `/api/stocks/{code}/predict/custom` | public | On-demand single-point prediction. Query: `?oversub=300&alpha=0.5&agent=knn_calibrated`. |
| GET | `/api/predict-agent-grid/{code}` | public | Pre-computed prediction grid (18 oversub x 5 alpha). |
| GET | `/api/listing-day-close-price/{code}` | public | First-day closing price for a single stock. |
| GET\|POST | `/api/listing-day-close-prices-batch` | public | Batch first-day closing prices. |
| GET | `/api/dual-listing-price/{code}` | public | Dual-listing (A+H / secondary) cross-market price and premium/discount. |
| GET | `/api/market-insights` | public | Cross-IPO market insights, trends, and aggregate analysis. |
| GET | `/api/cmp/overview` | public | Cross-market comparison overview for peer stock context. |
| GET | `/api/charts/frozen-calendar` | public | Frozen capital calendar: date series, daily max, regulatory milestones. |
| GET | `/api/charts/scatter-oversub-pnl` | public | Oversubscription vs first-day P&L scatter plot data. |
| GET | `/api/cache/rankings/sponsors` | public | Sponsor institution rankings by IPO involvement. |
| GET | `/api/cache/rankings/underwriters` | public | Underwriter institution rankings by IPO involvement. |
| GET | `/api/cache/rankings/cornerstone` | public | Cornerstone investor rankings. |
| GET | `/api/cache/rankings/coinvestment` | public | Co-investment rankings. |
| GET | `/api/cache/ab` | public | A-tail vs B-head comparison matrix. |
| GET | `/api/cache/stocks/{code}/analysis` | public | Pre-computed per-stock analysis (tier data, demographic distributions). |
| GET | `/api/cache/frozen-calendar` | public | Pre-computed frozen capital calendar. |
| GET | `/api/cache/scatter` | public | Pre-computed scatter plot data. |
| GET | `/api/cache/status` | public | Freshness status for all cache tables. |
| GET | `/api/blog/posts` | public | List published blog posts with pagination. |
| GET | `/api/blog/posts/{slug}` | public | Get a single published blog post by slug. |
| GET | `/api/stocks/full-market` | public | Directory of all HK-listed companies (code, zh/en name, board, isin). |
| GET | `/api/hynix/snapshot` | public | SK Hynix cross-market arbitrage snapshot. |
| GET | `/api/a-share-etf/overview` | public | A-share ETF capital flow overview. |
| GET | `/api/user/me` | optional JWT | Current user info from JWT. |
| GET | `/api/user/watchlist` | pcell JWT | User's watchlist as array of stock codes. |
| POST | `/api/user/watchlist/{code}` | pcell JWT | Toggle a stock in/out of the watchlist. |
| GET\|PUT | `/api/user/preferences` | pcell JWT | Get or update saved user preferences JSON. |
| GET | `/api/` | public | API discovery root: lists all endpoints with methods, auth, return types. |
| GET | `/.well-known/agent-protocol` | public | Machine-readable agent protocol. |
| GET | `/health` | public | Health check: uptime, DB stats, agent status, cache warmth. |

---

## MCP 工具清单（57 个）

**预测 / 配发**

- `predict_allotment` — Predict IPO allotment success for arbitrary final oversubscription multiple.
- `get_prediction` — Full default-parameter prediction data for a stock.
- `get_agent_grid` — Pre-computed 18 oversub x 5 alpha prediction grid.
- `get_allotment_tiers` — Actual Pool A/B allotment tiers for a stock.
- `get_oversub` — Oversubscription + frozen capital + hit rate for all stocks.

**股票 / 画像**

- `list_stocks` — List all tracked IPO stocks.
- `search_stocks` — Fuzzy search by code / EN name / simplified-traditional Chinese name.
- `get_homepage_stocks` — Homepage stock cards (upcoming / recent).
- `get_stock_summary` — Lightweight stock summary + tier classification.
- `get_stock_overview` — Full per-stock IPO analysis.
- `get_stock_ccass` — CCASS custodian demographics.
- `get_allottee_profile` — 中签画像: winner demographics from registrar ID data.
- `get_stock_announcements` — 个股公告中心: HKEXnews announcements grouped by category.
- `get_stock_buyback` — 回购明细: per-stock share buyback records.
- `get_stock_disclosure` — 增减持明细: per-stock disclosure-of-interest records.
- `get_stock_narrative` — AI-generated narrative (zh/en).
- `compare_stocks` — Side-by-side comparison of up to 10 stocks.

**招股书 / 纳入 / 排名**

- `get_prospectus` — Full prospectus info page data.
- `get_allotment_result` — Full allotment results page data.
- `get_inclusion_batch` — Batch Stock Connect inclusion analysis.
- `get_stock_inclusion` — Single-stock Stock Connect inclusion detail.
- `get_sponsor_ranking` — Sponsor institution rankings.
- `get_underwriter_ranking` — Underwriter institution rankings.
- `get_cornerstone_ranking` — Cornerstone investor rankings.
- `get_coinvestment_network` — Cornerstone co-investment network rankings.
- `get_stabilizing_ranking` — Stabilizing manager rankings.

**市场 / 图表**

- `get_ab_comparison` — A-tail vs B-head comparison matrix.
- `get_group_ab` — Pool A vs Pool B aggregate comparison.
- `get_frozen_calendar` — Frozen capital calendar.
- `get_market_insights` — Cross-IPO market insights.
- `get_scatter` — Oversubscription vs first-day P&L scatter.
- `get_cmp_overview` — Cross-market comparison overview.

**快讯 / 披露易**

- `get_flash_events` — Machine-readable flash-event feed.
- `get_buyback_ranking` — Share buyback ranking across companies.
- `get_disclosure_interest` — Disclosure-of-interest (增减持) ranking.
- `get_suspension_resumption` — Trading suspension / resumption list.
- `get_earnings_calendar` — Earnings calendar.
- `get_director_changes` — Director appointment / resignation / role changes.
- `get_corporate_actions` — Corporate actions summary.

**全市场财务 / 公司**

- `get_financial_data` — Per-stock financial statements grouped by period.
- `get_director_roster` — Per-stock director and executive roster.
- `get_listing_hearings` — HKEX listing hearing records.
- `list_hk_companies` — Directory of all HK-listed companies.

**价格 / 过户处 / 其他**

- `get_listing_day_close` — First-day closing price.
- `get_dual_listing_price` — Dual-listing cross-market mapping + H-share premium.
- `get_stock_ohlc` — Daily OHLC candlestick data.
- `get_registrar_analysis` — Registrar (过户登记处) performance comparison.
- `get_registrar_research` — Registrar historical research.
- `get_blog_posts` — Published blog posts.
- `get_hynix_snapshot` — SK Hynix cross-market arbitrage snapshot.
- `get_hynix_history` — Premium history for one hynix instrument.
- `get_a_share_etf_flow` — A-share ETF capital flow overview.
- `get_macro_tags` — Data center macro indicator tags.
- `get_macro_indicators` — Data center macro indicators.
- `get_macro_indicator_data` — Time series for one macro indicator.
- `get_us_corp_actions` — US corporate actions (8-K).
- `get_us_listings` — US IPO / SPAC new listing calendar.

---

## Agent 工作流

1. **Discover** — 读本文件或 `GET /api/`
2. **List stocks** — `GET /api/stocks`
3. **Analyze** — `GET /api/stocks/{code}/overview`
4. **Predict** — `GET /api/stocks/{code}/predict`
5. **Compare** — `GET /api/stocks/compare?codes=A,B`
6. **MCP** — 连接 `https://cibo.hk/mcp`（57 tools）

---

## 免责声明

本服务输出为统计模型结果，仅供参考，不构成投资建议。
