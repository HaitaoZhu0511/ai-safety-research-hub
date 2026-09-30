# OpenAI：输入/输出/工具Guardrail与人工批准

核验日期：2026-09-30。本文关注官方公开能力和研究，不描述未公开内部系统。

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
