# Amazon Web Services：模型解耦的Guardrail服务

核验日期：2026-09-30。本文关注官方公开能力和研究，不描述未公开内部系统。

## 公开实践

ApplyGuardrail可独立检查文本；可部署版本与工作草稿分开，并保存调用版本。

## 可应用的业务场景

多模型应用、RAG、安全网关。本项目建议将厂商能力作为可替换组件接入统一网关，保留业务身份、政策版本、检测器版本、数据范围和动作证据。

## 方法论提炼（本项目归纳）

- 在风险发生的边界实施控制，而不是仅在最终回答后检测。
- 通过脱敏真实分布、边界样本和正常对照验证策略；发布前保存评测数据与批准人。
- 将检测信号、政策结论和执行动作分别记录；高影响动作采用独立授权或复核。
- 记录模型、防护配置、Prompt、检索片段、工具请求和结果的版本，支持事故回放。

## 指标建议

版本干预率、P95延迟、单位调用成本、正常通过率。上述指标为本项目建议，不是该公司已公开的生产指标。

## 已知边界

内容过滤结果不能代替数据库ACL、IAM授权和工具副作用控制。

## 来源

- [ApplyGuardrail independent API](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-independent-api.html)：product_documentation。
- [Deploy your guardrail](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-deploy.html)：product_documentation。
