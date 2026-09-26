# cibo.hk — HK IPO Allotment API & MCP Server

面向 AI Agent 与开发者的**港股 IPO 中签分析**数据服务。提供两种接入方式：
**REST API**（公开 JSON 端点）与 **MCP Server**（远程 Streamable HTTP，免安装）。

- 网站：https://cibo.hk
- 权威文档：https://cibo.hk/llms.txt （本 README 是其镜像，以 llms.txt 为准）
- API 清单：https://cibo.hk/api/
- MCP 端点：https://cibo.hk/mcp

> 由熊猫证券 CEO JW 用 AI 辅助编程构建。预测港股 IPO 中签率（可调申购倍数与 α 分配系数），
> 并从过户处 ID 数据推断中签者画像（地区 / 国籍 / 性别 / 年龄），含港股通纳入分析、配发结果、
> 国际配售、基石、全市场财务等。

---

## 完整文档（权威镜像）

以下内容逐字镜像自 https://cibo.hk/llms.txt：

# cibo.hk — HK IPO Allotment Forecasts & Allottee-Profile Analysis

> Built by JW, CEO of Panda Securities, using AI-assisted programming.
> Forecasts IPO allotment hit rates — with adjustable subscription
> multiples and allotment-method (α) parameters — and infers allottee
> profiles (region / nationality / gender / age) from registrar ID data,
> plus Stock Connect inclusion analysis, allotment results, and more.

## Quickstart for AI Agents

**Base URL:** https://cibo.hk
**API Prefix:** `/api`
**Content-Type:** application/json

### Authentication

All public IPO data endpoints are open — no API key or JWT required.
Free-tier rate limits: 30 requests/min per IP, 5,000 requests/day.

Optional: personalized features (watchlist, preferences) use a pcell.si JWT
— see /.well-known/agent-protocol for the optional auth flow.

### Python SDK (pcell.si community, optional)

`pcell-sdk` (pip install pcell-sdk) is for pcell.si community features only.
It is NOT required to access cibo IPO data — all data endpoints are public.
PyPI: https://pypi.org/project/pcell-sdk/
Repo: https://github.com/pcell-si/pcell-sdk

### MCP Server (remote Streamable HTTP, no install)

57 tools covering the whole site's data: allotment prediction, stocks, inclusion, rankings, A/B comparison, market data, flash events, disclosures (buyback / interest / suspension / earnings / directors / corporate actions), full-market financials and company directory, prices, registrar research, blog posts, hynix arbitrage, A-share ETF flow, and data-center macro / US-market data.

- **Endpoint:** https://cibo.hk/mcp
- **Transport:** streamable-http
- **Description:** Remote Streamable HTTP MCP server for cibo.hk — lets AI agents query HK IPO allotment, predictions, prospectus details, allotment results (incl. international placing), inclusion, rankings, disclosures, financials, registrar, blog, full-market directory, hynix arbitrage, A-share ETF flow, and data-center macro/US-market data directly.

```json
{
  "mcpServers": {
    "cibo": {
      "url": "https://cibo.hk/mcp"
    }
  }
}
```

---

## API Endpoints (47 total)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/stocks` | public | List all IPO stocks with basic info (code, name, listing date). |
| GET | `/api/stocks/oversub` | public | Batch oversubscription + frozen capital for all stocks with allotment data. Query: ?year=2026. |
| GET | `/api/flash-events` | public | Derived flash-event feed (ipo_launch / allotment_result / listing / inclusion / prediction) as structured JSON for AI crawlers. Query: ?locale=zh-CN&limit=50&stock_code=07688. |
| GET | `/api/stocks/index` | public | Stock cards grouped by index with filtering, pagination, search. |
| GET | `/api/stocks/{code}/overview` | public | Full per-stock IPO analysis: subscription rates, allotment tiers, PnL scenarios, CCASS demographics. |
| GET | `/api/stocks/{code}/prospectus` | public | Full prospectus info page data: prospectus details (offer price, mechanism, greenshoe, secondary listing), cornerstone investors, and IPO financial statements. |
| GET | `/api/stocks/{code}/allotment-result` | public | Full allotment results page data: allotment summary (incl. international placing, greenshoe), placing concentration, cornerstone allocation + lock-up, Pool A/B tiers. |
| GET | `/api/stocks/{code}/allottee-profile` | public | 中签画像 (allottee profile): winner demographics from the registrar allotment dataset — total lots, person/company split, region/nationality, province, gender, age histogram + pyramid, HK ID letter/era/district. |
| GET | `/api/stocks/{code}/announcements` | public | 个股公告中心 (announcement center): all HKEXnews announcements for one stock, grouped by headline category with publish date and file URL. |
| GET | `/api/stocks/{code}/buyback` | public | 回购明细 (per-stock buyback): share buyback records for one stock, newest first, with per-day shares/amount and aggregate totals. |
| GET | `/api/stocks/{code}/disclosure` | public | 增减持明细 (per-stock disclosure-of-interest): DI records for one stock, newest first, with holder, capacity, event type, shares and pct. |
| GET | `/api/stocks/{code}/summary` | public | Lightweight stock summary: key stats and tier classification. |
| GET | `/api/stocks/{code}/ccass` | public | CCASS custodian demographics: type, province, gender, age distributions. |
| GET | `/api/stocks/{code}/narrative` | public | AI-generated narrative (zh/en) summarizing the IPO's key characteristics. |
| GET | `/api/stocks/compare` | public | Side-by-side comparison of up to 10 stocks. Query: ?codes=00001,00002 |
| GET | `/api/allotment-tiers/{code}` | public | Detailed allotment tier table: Pool A and Pool B subscription tiers with expected lots. |
| GET | `/api/stocks/{code}/predict` | public | Full allotment prediction data (default predicted oversub/alpha) backing the prediction page. |
| GET | `/api/stocks/{code}/predict/custom` | public | On-demand single-point allotment prediction for arbitrary parameters. Query: ?oversub=300&alpha=0.5&agent=knn_calibrated. |
| GET | `/api/predict-agent-grid/{code}` | public | Pre-computed prediction grid (18 oversub x 5 alpha) for interpolation. |
| GET | `/api/listing-day-close-price/{code}` | public | First-day closing price for a single stock. |
| GET|POST | `/api/listing-day-close-prices-batch` | public | Batch first-day closing prices. GET: ?codes=07688,01511 POST: {"codes":[...]} |
| GET | `/api/market-insights` | public | Cross-IPO market insights, trends, and aggregate analysis. |
| GET | `/api/cmp/overview` | public | Cross-market comparison overview for peer stock context. |
| GET | `/api/charts/frozen-calendar` | public | Frozen capital calendar: date series, daily max, regulatory milestones (for index page stacked bar chart). |
| GET | `/api/charts/scatter-oversub-pnl` | public | Oversubscription vs first-day P&L scatter plot data. |
| GET | `/api/cache/rankings/sponsors` | public | Sponsor institution rankings by IPO involvement. |
| GET | `/api/cache/rankings/underwriters` | public | Underwriter institution rankings by IPO involvement. |
| GET | `/api/cache/rankings/cornerstone` | public | Cornerstone investor rankings. |
| GET | `/api/cache/rankings/coinvestment` | public | Co-investment rankings. |
| GET | `/api/cache/stocks/{code}/analysis` | public | Pre-computed per-stock analysis (tier data, demographic distributions, HK letter/era breakdowns). |
| GET | `/api/cache/ab` | public | A-tail vs B-head comparison matrix. |
| GET | `/api/cache/frozen-calendar` | public | Pre-computed frozen capital calendar (dates, series, max_daily). |
| GET | `/api/cache/scatter` | public | Pre-computed scatter plot data (oversubscription vs P&L). |
| GET | `/api/cache/status` | public | Freshness status for all cache tables (row count, last_built timestamp). |
| GET | `/api/blog/posts` | public | List published blog posts with pagination. Query: ?locale=zh-CN&limit=20&offset=0 |
| GET | `/api/blog/posts/{slug}` | public | Get a single published blog post by slug. |
| GET | `/api/stocks/full-market` | public | Directory of all HK-listed companies (code, zh/en name, board, isin). Query: ?search=&limit=200. |
| GET | `/api/hynix/snapshot` | public | SK Hynix cross-market arbitrage snapshot (instruments with premium_pct, FX rates, base price). |
| GET | `/api/a-share-etf/overview` | public | A-share ETF capital flow overview (merged proxy, ETF inflow, margin). Query: ?limit=60. |
| GET | `/api/user/me` | optional JWT | Current user info from JWT. Returns {user: null} when unauthenticated. |
| GET | `/api/user/watchlist` | pcell JWT | User's watchlist as array of stock codes. |
| POST | `/api/user/watchlist/{code}` | pcell JWT | Toggle a stock in/out of the watchlist. Returns {in_watchlist: bool}. |
| GET|PUT | `/api/user/preferences` | pcell JWT | Get or update saved user preferences JSON. |
| GET | `/api/` | public | API discovery root: lists all endpoints with methods, auth, and return types. |
| GET | `/.well-known/agent-protocol` | public | Machine-readable agent protocol: service description, auth methods, data categories, recommended agent onboarding flow. |
| GET | `/health` | public | Health check: uptime, DB stats, agent status, cache warmth, pipeline health. |
| GET | `/api/agents` | internal | Internal agent heartbeat status and duration (ops telemetry). |

## Query Parameters
### /api/stocks/oversub
- `year` — optional listing year filter (e.g. 2026)
### /api/flash-events
- `locale` — zh-CN / zh-HK / en
- `limit` — max events (1-200, default 50)
- `stock_code` — optional 5-digit code to filter to one stock
### /api/stocks/compare
- `codes` — comma-separated stock codes
### /api/stocks/{code}/predict/custom
- `oversub` — final oversubscription multiple (optional, >0; omitted -> cibo predicted oversub)
- `alpha` — allocation-method coefficient in [0,1] (optional; omitted -> agent's recommended alpha)
- `agent` — agent key (optional, default knn_calibrated)
### /api/stocks/full-market
- `search` — optional substring on code/name
- `limit` — max companies (default 200)

---

## Agent Workflow

1. **Discover** — Read this file or GET /api/
2. **List stocks** — GET /api/stocks to see available IPO stocks
3. **Analyze** — GET /api/stocks/{code}/overview for full per-stock analysis
4. **Predict** — GET /api/stocks/{code}/predict for allotment forecast
5. **Compare** — GET /api/stocks/compare?codes=A,B to compare multiple stocks
6. **MCP** — Connect to https://cibo.hk/mcp for 57 tools (no install)

Full API reference: https://cibo.hk/api/
Agent protocol: https://cibo.hk/.well-known/agent-protocol

---

## Field Semantics (口径)

Field names are ambiguous across endpoints. Before reporting a number,
check which caliber it uses:

- **hit_rate** = overall allotment rate = 获配申请数 ÷ 有效申请数
  (successful applications ÷ valid applications). NOT the one-hand rate.
- **one_hand_hit_rate** = hit rate for the smallest (one-hand) tier only.
- **allotment_pct** (per tier) = 获配股份 ÷ 申请股份, i.e. the share-allotment
  ratio for that tier, not a probability. To judge "did this applicant win",
  use winner_count / applicant_count, not allotment_pct.
- **guaranteed_lots** = guaranteed minimum allotted shares, NOT "surely win one
  lot" (稳中一手). Do not translate it as such.
- **reallocation** is overloaded: in allotment results it is the raw clawback/
  重新分配 flag from the PDF; in per-stock analysis it means *discretionary*
  reallocation beyond the standard clawback. The two can disagree.
- **Dates** are YYYYMMDD integers (e.g. 20260930); 0 / empty = unknown.
- **predict vs actual**: predict_allotment / get_prediction are model forecasts;
  get_allotment_result / get_allotment_tiers are actual published results.
  Never mix the two.
- **ok:false contract**: every tool returns ok:false + error when the stock is
  unknown or the data does not exist. ok:true never means "complete" — always
  check the payload for missing / zero fields.

---

## Site Pages (GEO)

Static SSR pages for crawlers. Locales: zh-CN / zh-HK / en. `{code}` = 5-digit stock code.

Disclosure (HKEXnews Phase 1):
- 股份回购榜: https://cibo.hk/zh-CN/all-buybacks.html
- 大股东增减持: https://cibo.hk/zh-CN/disclosure-interest.html
- 停牌复牌: https://cibo.hk/zh-CN/suspension-resumption.html
- 财报日历: https://cibo.hk/zh-CN/earnings-calendar.html
- 董事变动: https://cibo.hk/zh-CN/director-change.html
- 供股配售/股本变动: https://cibo.hk/zh-CN/corporate-actions.html

Per-stock disclosure pages:
- 公告中心: https://cibo.hk/zh-CN/announcement-{code}.html
- 回购明细: https://cibo.hk/zh-CN/buyback-{code}.html
- 增减持明细: https://cibo.hk/zh-CN/disclosure-{code}.html

IPO allotment:
- 首页: https://cibo.hk/zh-CN/index.html
- 单股分析: https://cibo.hk/zh-CN/ipo-analysis-{code}.html
- 配发结果: https://cibo.hk/zh-CN/ipo-allotment-results-{code}.html

Derived flash events (Cibo快讯):
- Cibo快讯流: https://cibo.hk/zh-CN/flash-news.html
- 个股Cibo快讯: https://cibo.hk/zh-CN/flash-news-{code}.html
- 快讯 JSON feed: https://cibo.hk/api/flash-events?locale=zh-CN&limit=50
  (structured derived events: ipo_launch / allotment_result / listing /
   inclusion / prediction / buyback / earnings / dividend / disclosure_interest;
   each with stock_code, summary, metrics, url)

Full-market financials:
- 港股公司目录: https://cibo.hk/zh-CN/all-hk-stocks.html
- 单股财务: https://cibo.hk/zh-CN/stock-financial-{code}.html

---

## MCP 工具清单（57 个）

工具清单由 MCP `tools/list` 实时生成。

| 工具 | 说明 |
|------|------|
| `compare_stocks` | Side-by-side comparison of up to 10 stocks (comma-separated codes): prospectus, allotment, first-day close and change. |
| `get_a_share_etf_flow` | A-share ETF capital flow overview: merged proxy, ETF inflow, margin balance history, sectors and ETF breakdown. |
| `get_ab_comparison` | A-tail vs B-head comparison matrix (oversub, expected lots, capital efficiency). |
| `get_agent_grid` | Pre-computed 18 oversub x 5 alpha prediction grid for a stock and agent. |
| `get_allotment_result` | Full allotment results page data for a stock: allotment summary (offer price, oversubscription, international placing, greenshoe), international placing concentration, cornerstone allocation + lock-up, and Pool A/B tiers. Returns ok:false when the stock is unknown or has no published allotment result yet (pre-listing stocks return placeholder tiers, not real data). `summary.reallocation` is the raw clawback/重新分配 flag from the allotment PDF — it does NOT mean discretionary reallocation. |
| `get_allotment_tiers` | Actual Pool A/B allotment tiers for a stock: applied shares, allotted shares, hit pct, and expected lots per tier. Returns ok:false when the stock has no published allotment result. |
| `get_allottee_profile` | 中签画像 (allottee profile): winner demographics parsed from the registrar allotment dataset — total lots, person/company split, region/nationality, province, gender, age histogram + pyramid, and HK ID letter/era/district. |
| `get_blog_posts` | Published blog posts (赛博畅想) with title, excerpt, author, tags, date. |
| `get_buyback_ranking` | Share buyback ranking across listed companies. Paginated (page/page_size). |
| `get_cmp_overview` | Cross-market comparison overview for peer stock context. |
| `get_coinvestment_network` | Cornerstone investor co-investment network rankings. |
| `get_cornerstone_ranking` | Cornerstone investor rankings by IPO involvement. |
| `get_corporate_actions` | Corporate actions summary (buybacks, dividends, placements, etc.). Paginated. |
| `get_director_changes` | Director appointment / resignation / role changes list. Paginated. |
| `get_director_roster` | Per-stock director and executive roster (names, bio, roles). |
| `get_disclosure_interest` | Disclosure-of-interest (增减持) records, newest first. Paginated. event: 'buy', 'sell', or '' for both. |
| `get_dual_listing_price` | Dual-listing cross-market mapping for a stock: A+H via ah_stock_mapping, other markets via prospectus_details.secondary_markets, plus the IPO-time H-share premium/discount (ah_premium_at_ipo). |
| `get_earnings_calendar` | Earnings calendar (final/interim/quarterly results, dividends, profit warnings, board dates). Paginated. |
| `get_financial_data` | Per-stock financial statements grouped by period (revenue, profit, eps, etc.) from post-listing financial data. |
| `get_flash_events` | Machine-readable flash-event feed (ipo_launch / allotment_result / listing / inclusion / prediction). Filter by stock_code. |
| `get_frozen_calendar` | Frozen capital calendar: daily date series, max frozen, milestones. |
| `get_group_ab` | Pool A vs Pool B aggregate comparison data. |
| `get_homepage_stocks` | Homepage stock cards: upcoming IPOs (prelist, with listing status such as delayed/cancelled) and recently listed IPOs (recent). Same data as the index page's upcoming/recent sections. |
| `get_hynix_history` | Premium history for one hynix instrument (e.g. SKHY, 7709.HK). |
| `get_hynix_snapshot` | SK Hynix cross-market arbitrage snapshot: instruments with premium_pct, FX rates, base price (from the hynix tracker service). |
| `get_inclusion_batch` | Batch Stock Connect inclusion analysis for all candidate stocks. |
| `get_listing_day_close` | First-day closing price for a single stock. |
| `get_listing_hearings` | HKEX listing hearing records (company, date, result, market). |
| `get_macro_indicator_data` | Time series for one data center macro indicator by id. |
| `get_macro_indicators` | Data center macro indicators, optionally filtered by tag/source/search. |
| `get_macro_tags` | Data center macro indicator tags (growth, inflation, AI chain, etc.). |
| `get_market_insights` | Cross-IPO market insights, trends, and aggregate analysis. |
| `get_oversub` | Oversubscription + frozen capital + hit rate for all stocks with allotment data, ordered by listing date desc. Optional ?year filter. |
| `get_prediction` | Full default-parameter prediction data for a stock (actual tiers, AI alpha map, prediction grid, agent ratings) backing the prediction page. |
| `get_prospectus` | Full prospectus info page data for a stock: prospectus details (offer price, mechanism, greenshoe, secondary listing, subscription tiers), cornerstone investors + ratio, IPO financial statements (income/balance/ cashflow), IPO timeline, directors, syndicate, stabilizing manager. |
| `get_registrar_analysis` | Registrar (过户登记处) performance comparison across IPOs. |
| `get_registrar_research` | Registrar historical research and insights. |
| `get_scatter` | Oversubscription vs first-day P&L scatter plot data. |
| `get_sponsor_ranking` | Sponsor institution rankings by IPO involvement. |
| `get_stabilizing_ranking` | Stabilizing manager rankings by IPO involvement. |
| `get_stock_announcements` | 个股公告中心 (announcement center): all HKEXnews announcements for one stock, grouped by headline category with publish date and file URL. |
| `get_stock_buyback` | 回购明细 (per-stock buyback): share buyback records for one stock, newest first, with per-day shares/amount and aggregate totals. |
| `get_stock_ccass` | CCASS custodian demographics for a stock: type, province, gender, age distributions and HK letter/era breakdowns. |
| `get_stock_disclosure` | 增减持明细 (per-stock disclosure-of-interest): DI records for one stock, newest first, with holder, capacity, event type, shares and pct. |
| `get_stock_inclusion` | Single-stock Stock Connect inclusion detail across review periods. |
| `get_stock_narrative` | AI-generated narrative (zh/en) summarizing a stock's IPO characteristics. |
| `get_stock_ohlc` | Daily OHLC candlestick data (~400 days) from Tencent Finance. |
| `get_stock_overview` | Full per-stock IPO analysis: subscription rates, allotment tiers, PnL scenarios, CCASS demographics, narrative, plus cross-market context. Returns ok:false when the stock code is unknown. Note: the analysis `data.s.reallocation` flag means *discretionary* reallocation (not the raw clawback flag), and may disagree with get_allotment_result's summary.reallocation. |
| `get_stock_summary` | Lightweight stock summary: key stats and tier classification (fast). Returns ok:false when the stock code is unknown or has no data. Field note: `summary.reallocation` is '是' only when there was a *discretionary* reallocation (shares moved beyond the standard clawback). For the raw clawback/重新分配 flag from the allotment PDF, use get_allotment_result -> summary.reallocation instead — the two are different and may disagree. |
| `get_suspension_resumption` | Trading suspension / resumption announcements list. Paginated. type_key: 'suspension', 'resumption', or '' for both. |
| `get_underwriter_ranking` | Underwriter institution rankings by IPO involvement. |
| `get_us_corp_actions` | US corporate actions (8-K): M&A, earnings, dividends, splits, buybacks, etc. |
| `get_us_listings` | US IPO / SPAC new listing calendar. |
| `list_hk_companies` | Directory of all HK-listed companies (code, zh/en name, board, isin, listing_date) from the full-market securities master. Optional substring search. |
| `list_stocks` | List all tracked IPO stocks with basic info (code, name, listing date). |
| `predict_allotment` | Predict IPO allotment success for arbitrary final oversubscription multiple and allocation-method alpha. alpha=None uses the agent's own recommended alpha; oversub=None uses cibo's predicted final multiple. Returns Pool A/B tier expected lots and hit pct. |
| `search_stocks` | Fuzzy search stocks by code, English name, or simplified/traditional Chinese name (cross-script via OpenCC when available). |

---

## 免责声明

本服务输出为统计模型结果，仅供参考，不构成投资建议。
