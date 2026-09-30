# OpenAI：输入/输出/工具Guardrail与人工批准

初始核验：2026-09-30；本轮增补：2026-10-01（旧来源日期不批量刷新）。本文关注官方公开能力和研究，不描述未公开内部系统。

## 公开实践

工具调用边界附近实施校验；需要人工决定时暂停运行；审查后恢复同一次运行。

## 可应用的业务场景

知识库、客服、取数、工具型Agent。本项目建议将厂商能力作为可替换组件接入统一网关，保留业务身份、政策版本、检测器版本、数据范围和动作证据。

## 方法论提炼（本项目归纳）

- 在风险发生的边界实施控制，而不是仅在最终回答后检测。
- 通过脱敏真实分布、边界样本和正常对照验证策略；发布前保存评测数据与批准人。
- 将检测信号、政策结论和执行动作分别记录；高影响动作采用独立授权或复核。
- 记录模型、防护配置、Prompt、检索片段、工具请求和结果的版本，支持事故回放。

## 指标建议

工具越权率、敏感数据外发率、正常任务完成率。上述指标为本项目建议，不是该公司已公开的生产指标。

## 已知边界

仅首个/最终Agent上的Guardrail覆盖范围有限；业务仍需独立实现授权与出站约束。

## 来源

- [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)：product_documentation。
- [Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)：product_documentation。

## v0.2：MCP执行边界

官方[MCP文档](https://developers.openai.com/api/docs/guides/tools-connectors-mcp)说明工具范围过滤、敏感操作批准及第三方服务器风险。应用仍需独立校验业务身份、租户、目标和动作参数。离线演示将批准绑定确切提案与政策快照；这是本项目控制实现，不是SDK默认能力，也没有接入真实MCP服务器。

## 2026-10-01补充：内容信号、轨迹与产品生命周期

[Moderation](https://developers.openai.com/api/docs/guides/moderation)区分审核信号和应用决策：错误需单独处理，流式完整输出后的分数不等于每个片段已被阻断，工具描述与Schema也不能依赖该内容审核保护。本项目建议给短剧生成和审核助手明确输出前门禁及失败路径，而不是只记flagged。

[Agent安全文档](https://developers.openai.com/api/docs/guides/agent-builder-safety)与[Trace评测](https://developers.openai.com/api/docs/guides/agent-evals)适合学习不可信数据边界和工作流检查。结构化数据减少自由文本传递面，但不自动实现业务授权；评分器评价可观察过程和结果，不要求隐藏思维链。

OpenAI Docs核验的[退役公告](https://developers.openai.com/api/docs/deprecations)显示Agent Builder/Evals处于过渡期：Evals计划2026-10-31只读，二者计划2026-11-30关闭。新项目学习方法但不绑定待退役界面，迁移与当前可用范围实施前重查。没有调用API或提交样本。
