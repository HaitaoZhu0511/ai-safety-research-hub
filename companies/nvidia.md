# NVIDIA：五段式Rails与联合评测

核验日期：2026-09-30。本文关注官方公开能力和研究，不描述未公开内部系统。

## 公开实践

在输入、检索、对话、执行、输出阶段实施检查；评测同时统计遵从、资源和延迟。

## 可应用的业务场景

RAG、工具Agent、领域对话系统。本项目建议将厂商能力作为可替换组件接入统一网关，保留业务身份、政策版本、检测器版本、数据范围和动作证据。

## 方法论提炼（本项目归纳）

- 在风险发生的边界实施控制，而不是仅在最终回答后检测。
- 通过脱敏真实分布、边界样本和正常对照验证策略；发布前保存评测数据与批准人。
- 将检测信号、政策结论和执行动作分别记录；高影响动作采用独立授权或复核。
- 记录模型、防护配置、Prompt、检索片段、工具请求和结果的版本，支持事故回放。

## 指标建议

政策遵从率、工具异常、额外模型调用、延迟。上述指标为本项目建议，不是该公司已公开的生产指标。

## 已知边界

Rails是编排能力，不自动保证检查逻辑正确；完整配置仍需评测。

## 来源

- [Guardrail Types](https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/rail-types)：product_documentation。
- [Evaluate Configuration](https://docs.nvidia.com/nemo/guardrails/evaluation/evaluate-configuration)：product_documentation。
