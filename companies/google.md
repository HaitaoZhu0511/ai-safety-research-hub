# Google / DeepMind：组织基线与模型能力风险

初始核验：2026-09-30；本轮增补：2026-10-01（旧来源日期不批量刷新）。本文关注官方公开能力和研究，不描述未公开内部系统。

## 公开实践

Model Armor以模板管理输入输出检测，提供组织基线与只检测模式；DeepMind公布能力风险框架。

## 可应用的业务场景

企业AI网关、RAG、多业务统一保护。本项目建议将厂商能力作为可替换组件接入统一网关，保留业务身份、政策版本、检测器版本、数据范围和动作证据。

## 方法论提炼（本项目归纳）

- 在风险发生的边界实施控制，而不是仅在最终回答后检测。
- 通过脱敏真实分布、边界样本和正常对照验证策略；发布前保存评测数据与批准人。
- 将检测信号、政策结论和执行动作分别记录；高影响动作采用独立授权或复核。
- 记录模型、防护配置、Prompt、检索片段、工具请求和结果的版本，支持事故回放。

## 指标建议

基线覆盖率、影子命中、人群误杀、敏感数据泄漏。上述指标为本项目建议，不是该公司已公开的生产指标。

## 已知边界

模型能力框架与云产品属于不同层；单轮检测不等于完整多轮任务安全。

## 来源

- [Model Armor overview](https://docs.cloud.google.com/model-armor/overview)：product_documentation。
- [Introducing Frontier Safety Framework (historical baseline)](https://deepmind.google/blog/introducing-the-frontier-safety-framework/)：governance_framework。2024年初始框架；不将其描述为当前版本全文。

## 2026-10-01补充：从风险问卷到责任与验收

[SAIF Risk Assessment公开介绍](https://blog.google/innovation-and-ai/technology/safety-security/google-ai-saif-risk-assessment/)发表于2024-10-24，以问卷生成风险和建议清单。本次重读用于治理方法补充，不称作2026新功能，也没有提交真实组织问卷。

本项目建议将自评结果落到负责人、证据、控制实施点和回归验收；问卷答“有权限控制”应对应可复现的跨租户测试。自报风险清单不是代码扫描、模型基准或安全认证。

用于审核中台接入评审、供应链/权限资产梳理；与Model Armor运行时检测分属不同层，不以一份问卷代替上线门禁。
