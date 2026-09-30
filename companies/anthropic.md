# Anthropic：风险治理、分类器与行为评测

初始核验：2026-09-30；本轮增补：2026-10-01（旧来源日期不批量刷新）。本文关注官方公开能力和研究，不描述未公开内部系统。

## 公开实践

RSP持续版本化；分类器研究同时报告防护效果、正常拒答和开销；行为研究覆盖Agent失配。

## 可应用的业务场景

前沿模型发布、安全评测、长任务Agent。本项目建议将厂商能力作为可替换组件接入统一网关，保留业务身份、政策版本、检测器版本、数据范围和动作证据。

## 方法论提炼（本项目归纳）

- 在风险发生的边界实施控制，而不是仅在最终回答后检测。
- 通过脱敏真实分布、边界样本和正常对照验证策略；发布前保存评测数据与批准人。
- 将检测信号、政策结论和执行动作分别记录；高影响动作采用独立授权或复核。
- 记录模型、防护配置、Prompt、检索片段、工具请求和结果的版本，支持事故回放。

## 指标建议

攻击成功率、正常拒答率、行为失配频率、成本。上述指标为本项目建议，不是该公司已公开的生产指标。

## 已知边界

受控模拟结果不能外推为生产事故率；风险框架首页不能替代具体版本全文。

## 来源

- [Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy)：governance_framework。
- [Constitutional Classifiers](https://www.anthropic.com/news/constitutional-classifiers)：research。
- [Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment)：research。
- [Bloom automated behavioral evaluations](https://alignment.anthropic.com/2025/bloom-auto-evals/)：research。

## 2026-10-01补充：级联检测与平台滥用调查

[Constitutional Classifiers++介绍](https://www.anthropic.com/research/next-generation-constitutional-classifiers)提供轻量筛查、可疑升级及交互联合判断的学习点；内部探针不能作为普通API插件复制。如何将一级误报转成复核而非处罚，见[案例](../cases/classifiers-cascade.md)，研究数字不移作本项目业绩。

[2025网络活动披露](https://www.anthropic.com/news/disrupting-AI-espionage)与[2026-09报告概览](https://www.anthropic.com/threat-intelligence-report-september-2026)扩大到跨任务/工具行为调查。来源是厂商观察，不是独立归因或行业事故率；2026报告只核验HTML概览，未知精确发布日不补造。

迁移到SLG和短剧平台时，关注授权范围、工具副作用、累计预算与跨任务线索；自称防守或内容看似正常仍不能扩权。合法开发对照和独立处置批准同样重要。详见[调查Case](../cases/agentic-cyber-abuse.md)。
