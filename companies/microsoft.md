# Microsoft：企业内容安全与AI红队

核验日期：2026-09-30。本文关注官方公开能力和研究，不描述未公开内部系统。

## 公开实践

公开内容安全分类和Prompt防护能力；提供AI红队方法及PyRIT相关指南。

## 可应用的业务场景

企业Copilot、办公RAG、审核工作台。本项目建议将厂商能力作为可替换组件接入统一网关，保留业务身份、政策版本、检测器版本、数据范围和动作证据。

## 方法论提炼（本项目归纳）

- 在风险发生的边界实施控制，而不是仅在最终回答后检测。
- 通过脱敏真实分布、边界样本和正常对照验证策略；发布前保存评测数据与批准人。
- 将检测信号、政策结论和执行动作分别记录；高影响动作采用独立授权或复核。
- 记录模型、防护配置、Prompt、检索片段、工具请求和结果的版本，支持事故回放。

## 指标建议

误杀、漏放、外发拦截、跨租户访问、红队修复率。上述指标为本项目建议，不是该公司已公开的生产指标。

## 已知边界

检测器无法独立解决权限、敏感数据访问和浏览器外发问题。

## 来源

- [Microsoft AI Red Team](https://learn.microsoft.com/en-us/security/ai-red-team/)：product_documentation。
- [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/cognitive-services/content-safety/overview)：product_documentation。
- [CVE-2025-32711 vendor advisory](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711)：vendor_advisory。页面需JavaScript，未直接读取公告正文；以Microsoft来源的NVD记录与论文辅助核验。
