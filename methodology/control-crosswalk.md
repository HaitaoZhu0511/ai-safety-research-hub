# 风险—控制—证据—测试对应

这是本项目控制设计对应表，不是OWASP/NIST官方认证或完整条目映射。2026版框架已核验资源页，阅读全文后的版本级交叉表仍是后续工作。

| 本项目风险 | 确定性控制 | 必需证据 | 已运行Golden用例 |
| --- | --- | --- | --- |
| privacy | 实际身份租户匹配、指标和目的地限制 | 身份引用、请求摘要、拒绝理由 | G04、G09、G13、G23 |
| tool-authority | 允许工具、角色、严格参数、独立批准 | 政策、批准引用、执行回执 | G06—G08、G14—G18、G24 |
| resource-abuse | 行数预算、类型检查 | 请求与预算、拒绝理由 | G10—G12 |
| model-governance | 完整政策快照与发布停用 | 政策版本、快照摘要 | G19—G20 |
| prompt-injection | 外部指令不能成为额外动作参数 | 外部来源与已拒绝提案 | G08，仅验证提案边界 |

没有模型参与，G08不代表识别或抵抗了语义注入。grounding、content-harm、provenance等内容与事实能力仍只有[设计用例](../evals/design-cases.json)，不能报告已经通过。

正常对照G01—G03、G16、G21确保控制未把全部合法请求一概拦掉。所有结果见[报告](../reports/README.md)。

参考入口：[OWASP LLM2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)、[OWASP Agent2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)、[NIST GenAI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)。
