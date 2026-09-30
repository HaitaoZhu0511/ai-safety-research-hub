# AI安全精选资讯

截至2026-10-01，18条人工核验的精选动态，并非完整新闻流。[本轮15条来源、6篇Case的分析](2026-10-01-research-roundup.md)包含无确切发布日期的材料，不虚构新闻日日期。

| 日期 | 类型 | 材料 | 关注点 |
| --- | --- | --- | --- |
| 2026-09-18 | documentation_update | [阿里云安全运营Agent文档](https://www.alibabacloud.com/help/en/content-moderation/latest/how-to-use-the-security-operation-agent) | 公开预览的在线测试、评测和调优能力。 |
| 2026-09-18 | documentation_update | [Microsoft Prompt Shields与Spotlighting文档](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection) | 预览能力、Token开销及检测/过滤差异；文档更新不等于首次产品发布。 |
| 2026-09-17 | documentation_update | [阿里云VOD机审与人审联动文档](https://www.alibabacloud.com/help/en/vod/user-guide/automated-review-1) | 人工覆盖机审与播放状态分开；旧播放链接可能继续有效，不把改判等同全渠道撤销。 |
| 2026-09-15 | documentation_update | [腾讯模型路由安全配置](https://cloud.tencent.com/document/product/1829/135297) | 文档更新，不等于产品首次上线。 |
| 2026-08-03 | framework_publication | [OWASP LLM风险指南2026版资源页](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) | 资源页日期；保留旧版入口，后续阅读全文后再做条目级差异。 |
| 2026-07-29 | documentation_update | [AgentKit Runtime安全责任摘录](https://docs.volcengine.com/docs/agentkit/Runtime_security_best_practices?lang=zh) | 官方索引的文档更新时间；直接正文需JavaScript，责任划分仍需实施前核验。 |
| 2026-07-23 | documentation_update | [腾讯COS视频审核与自动冻结文档](https://cloud.tencent.com/document/product/436/134929) | 截帧检测及公有读冻结；不是全模态覆盖或CDN清除效果证明。 |
| 2026-06-03 | documentation_update | [OpenAI Agent Builder/Evals退役公告](https://developers.openai.com/api/docs/deprecations) | 日期是退役通知日；Evals计划10-31只读、11-30关闭，Agent Builder计划11-30关闭；部署前复核。 |
| 2026-04-24 | report_release | [快手2025 ESG披露](https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-releases-2025-esg-report-deepening-green-operations-and) | 发布在2026年，主要报告期为2025年。 |
| 2026-02-12 | documentation_update | [火山AgentKit安全围栏资料](https://docs.volcengine.com/docs/agentkit/Guardrailsoverview?lang=zh) | 索引摘录记录的文档更新日；初次正文超时，本轮复核返回JavaScript提示，仍仅有摘录，不是首次发布或效果证明。 |
| 2026-01-09 | research_publication | [Constitutional Classifiers++研究介绍](https://www.anthropic.com/research/next-generation-constitutional-classifiers) | 两级筛查与整段交互判断；厂商研究条件不可外推为中文审核召回或现金节约。 |
| 2025-12-19 | research_publication | [Bloom自动行为评测](https://alignment.anthropic.com/2025/bloom-auto-evals/) | 针对指定行为生成场景并衡量频率/严重度。 |
| 2025-12-18 | experiment_publication | [Project Vend第二阶段](https://www.anthropic.com/research/project-vend-2) | 多因素变更后经营改善；不能单因果归因。 |
| 2025-12-09 | framework_publication | [OWASP Agent风险框架2026版资源页](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | 版本年份2026，资源页发布日期2025，不混为同一日期。 |
| 2025-11-13 | report_release | [Anthropic披露Agent编排型网络滥用调查](https://www.anthropic.com/news/disrupting-AI-espionage) | 活动发现于2025-09，公开于11-13并于11-14勘误；厂商视角，不是独立事故频率统计。 |
| 2025-09-06 | paper_submission | [EchoLeak案例论文](https://arxiv.org/abs/2509.10540) | 这是论文提交日期；漏洞披露在此前，不能混为一谈。 |
| 2025-06-27 | experiment_publication | [Project Vend第一阶段](https://www.anthropic.com/research/project-vend-1) | 现实经营Agent暴露长期状态、价格和授权问题。 |
| 2025-02-03 | research_publication | [Constitutional Classifiers研究](https://www.anthropic.com/news/constitutional-classifiers) | 同时研究防护、正常拒答和算力开销。 |

## 日期与维护

日期类型见[结构化目录](../catalog/news.json)。文档更新时间、首次公告、活动发生、报告期与计划关闭日不能混用。Anthropic2026-09报告仅确认标题月份与报告期，因此不编造精确日期进入本表；README可变版本也不伪造发布日期。

新增动态应给发布方、原始URL、可确认的日期、事件类型、访问等级与启示。仅取得搜索摘录就写清楚；产品自述不作为独立效果证明。旧日期与限制保留，不为了“新鲜”批量刷新。

当前没有自动抓取、定时通知或自动发布。[来源台账](../catalog/source-review.json)不是已归档网页快照。
