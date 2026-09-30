# Meta：开放安全模型与评测工具

初始核验：2026-09-30；本轮增补：2026-10-01（旧来源日期不批量刷新）。本文关注官方公开能力和研究，不描述未公开内部系统。

## 公开实践

Purple Llama包含内容防护、Prompt防护和网络安全评测工具；组件许可证并不相同。

## 可应用的业务场景

自部署模型、开放模型应用、代码安全。本项目建议将厂商能力作为可替换组件接入统一网关，保留业务身份、政策版本、检测器版本、数据范围和动作证据。

## 方法论提炼（本项目归纳）

- 在风险发生的边界实施控制，而不是仅在最终回答后检测。
- 通过脱敏真实分布、边界样本和正常对照验证策略；发布前保存评测数据与批准人。
- 将检测信号、政策结论和执行动作分别记录；高影响动作采用独立授权或复核。
- 记录模型、防护配置、Prompt、检索片段、工具请求和结果的版本，支持事故回放。

## 指标建议

类别召回、注入识别、过度拒答、推理成本。上述指标为本项目建议，不是该公司已公开的生产指标。

## 已知边界

开放权重不等于无限制许可证；工具支持与版本需逐组件核对。

## 来源

- [Purple Llama official repository](https://github.com/meta-llama/PurpleLlama)：official_repository。

## 2026-10-01补充：Agent防护与图像审核边界

[LlamaFirewall官方README](https://raw.githubusercontent.com/meta-llama/PurpleLlama/main/LlamaFirewall/README.md)把Prompt、轨迹、代码与定制扫描分层；可读工具事件用于验证任务偏移，但扫描建议不替代执行授权，不能要求提供隐藏思维链。见[Case](../cases/llama-firewall.md)。

[Llama Guard 4文档](https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama-guard-4)说明文本图像联合输入、英语优化与生成图像的支持限制。中文生成漫剧不在未经验证的默认适用范围；应按具体权重/版本进行图像来源与语言切片评测，而非只看“多模态”。

本轮只读文档与可变main的README，没有下载权重、安装扫描器或复核完整基准；组件、模型和外部服务的许可/费用分别核对。
