# 阿里巴巴 / 阿里云：安全运营Agent与空间隔离

核验日期：2026-09-30。本文关注官方公开能力和研究，不描述未公开内部系统。

## 公开实践

安全运营Agent公开支持在线测试、效果评测和政策调优；工作空间可隔离权限和用量。

## 可应用的业务场景

审核策略运营、多团队模型平台。本项目建议将厂商能力作为可替换组件接入统一网关，保留业务身份、政策版本、检测器版本、数据范围和动作证据。

## 方法论提炼（本项目归纳）

- 在风险发生的边界实施控制，而不是仅在最终回答后检测。
- 通过脱敏真实分布、边界样本和正常对照验证策略；发布前保存评测数据与批准人。
- 将检测信号、政策结论和执行动作分别记录；高影响动作采用独立授权或复核。
- 记录模型、防护配置、Prompt、检索片段、工具请求和结果的版本，支持事故回放。

## 指标建议

评测耗时、配置回滚、误杀、权限覆盖、工作空间成本。上述指标为本项目建议，不是该公司已公开的生产指标。

## 已知边界

产品文档公开预览状态；政策调优当前范围有限；一键应用仍应结合自身发布门禁。

## 来源

- [Security Operations Agent](https://www.alibabacloud.com/help/en/content-moderation/latest/how-to-use-the-security-operation-agent)：product_documentation。
- [Model Studio workspaces](https://www.alibabacloud.com/help/en/model-studio/use-workspace)：product_documentation。
