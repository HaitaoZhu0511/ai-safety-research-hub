# 2026-10-01大厂AI安全资料增补

本轮新增15条来源、6篇案例分析、3类应用场景、7条有可核验日期的动态及6项待执行回归设计。共覆盖12家公司、54条来源、15个Case、15类场景、18条精选动态和22项未执行设计。旧资料不批量刷新核验日；这不是当天新闻全集。

## 值得优先阅读

| 主题 | 材料性质 | 本轮结论/借鉴 | 阅读 |
| --- | --- | --- | --- |
| 两级检测 | Anthropic官方研究介绍 | 一级可疑升级，联合观察最终质量与开销 | [Case](../cases/classifiers-cascade.md) |
| 跨任务滥用 | Anthropic调查披露与2026-09概览 | 单条安全不能证明整段任务获授权 | [Case](../cases/agentic-cyber-abuse.md) |
| Agent扫描器 | Meta官方README | 检测建议、任务轨迹和执行授权分层 | [Case](../cases/llama-firewall.md) |
| 政策逻辑验证 | AWS产品文档 | 政策相容不证明资质或合同真实 | [Case](../cases/automated-reasoning.md) |
| 人审与播放状态 | 阿里云VOD文档 | 人工改判还要验证已有访问能力 | [Case](../cases/vod-review-revocation.md) |
| 截帧与冻结 | 腾讯COS文档 | 所截画面与公有读冻结都有范围 | [Case](../cases/video-frame-freeze.md) |

上述案例中有厂商报告、受控研究与产品应用，不能放在一个“事故发生率”分母中。未安装开源检测工具，未调用厂商模型或上传业务样本；保留66个单元测试和24个控制用例的独立口径。

## 其他补充及选型提醒

- OpenAI：[Moderation](https://developers.openai.com/api/docs/guides/moderation)的分数用于业务策略，不是自动裁决；完整生成后的审核不能视为逐流式片段已放行。[Agent安全](https://developers.openai.com/api/docs/guides/agent-builder-safety)强调来源与数据流边界；结构化结果仍需验证授权。
- OpenAI Docs核验发现[退役时间表](https://developers.openai.com/api/docs/deprecations)：2026-06-03通知；Evals计划2026-10-31转只读，Evals/Agent Builder计划2026-11-30关闭。学习[Trace评测方法](https://developers.openai.com/api/docs/guides/agent-evals)仍有价值，但不能据页面旧链接推荐新项目依赖待退役界面；部署前复查。
- Microsoft：[Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection)区分检测和过滤；Spotlighting为预览，编码可能增加Token，不能代替权限。
- Meta：[Llama Guard 4](https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama-guard-4)的输入/语言/生成图像边界影响中文短剧选型；需专项验证，不能仅看“多模态”标签。
- Google：[2024-10-24 SAIF工具介绍](https://blog.google/innovation-and-ai/technology/safety-security/google-ai-saif-risk-assessment/)帮助把问卷结论变成风险清单，是历史方法重读，不是2026新发布；自评清单不是扫描结果或认证。
- 字节/火山：[Runtime安全最佳实践](https://docs.volcengine.com/docs/agentkit/Runtime_security_best_practices?lang=zh)只取得官方搜索索引，直接正文返回JavaScript提示；可讨论责任分工，但未完成正文部署核验。原AgentKit围栏也仍是摘录等级。

## 日期、证据与版本

有些材料只有标题月份或可变README，未确认日日期就不编造新闻日期。Anthropic2026-09报告目前只分析HTML概览，报告期2025-12至2026-08，不是每个活动都发生在9月。OpenAI公告日期不是关闭日期；阿里、腾讯、Microsoft文档更新也不是首次产品上线。

原始来源与访问说明见[索引](../sources/README.md)，复核范围见[台账](../catalog/source-review.json)。没有保存网页快照或内容哈希，不伪造历史版本证据。

## 怎么转成自己的项目

先读[上下文与级联审核](../methodology/context-and-cascade-review.md)，选一个风险底线已定义的正常/疑难内容试点；再读[证据到处置闭环](../methodology/evidence-to-enforcement.md)，核验机审、人审、批准与实际回执。SLG、短剧和中台具体组合见[场景](../docs/scenarios.md)。

新E17—E22全部design_only。厂商数字不能当本项目效果；资料结构校验通过也不能当模型检出率。当前没有定时采集、自动发新闻或真实业务部署。
