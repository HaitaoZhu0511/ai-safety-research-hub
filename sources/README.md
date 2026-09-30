# 来源索引与证据规则

核验日期：2026-09-30。结构化索引见[来源目录](../catalog/sources.json)。

## 证据性质

- 官方治理框架：证明公开承诺和方法；不自动证明执行成效。
- 官方产品文档：证明公开支持方向；预览、地域、限额和版本需单独确认。
- 官方研究：证明给定实验设计下的观察；受控模拟不等于生产事故。
- 厂商公告/漏洞记录：证明已披露漏洞；不自动证明已发生入侵或仍未修复。
- 独立研究：标注研究者身份，与厂商来源交叉核验；不写成厂商自述。
- 本项目归纳：控制、指标、业务路线和回归设计属于原创建议。

## 来源列表

| ID | 发布方 | 材料 | 类型 |
| --- | --- | --- | --- |
| openai-guardrails | OpenAI | [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) | product_documentation |
| openai-safety | OpenAI | [Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices) | product_documentation |
| anthropic-rsp | Anthropic | [Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy) | governance_framework |
| anthropic-classifiers | Anthropic | [Constitutional Classifiers](https://www.anthropic.com/news/constitutional-classifiers) | research |
| anthropic-misalignment | Anthropic | [Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment) | research |
| anthropic-summer2026 | Anthropic | [Agentic Misalignment in Summer 2026](https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/) | research |
| anthropic-vend1 | Anthropic | [Project Vend phase one](https://www.anthropic.com/research/project-vend-1) | real_world_experiment |
| anthropic-vend2 | Anthropic | [Project Vend phase two](https://www.anthropic.com/research/project-vend-2) | real_world_experiment |
| anthropic-bloom | Anthropic | [Bloom automated behavioral evaluations](https://alignment.anthropic.com/2025/bloom-auto-evals/) | research |
| ms-redteam | Microsoft | [Microsoft AI Red Team](https://learn.microsoft.com/en-us/security/ai-red-team/) | product_documentation |
| ms-content | Microsoft | [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/cognitive-services/content-safety/overview) | product_documentation |
| ms-cve | Microsoft | [CVE-2025-32711 vendor advisory](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711) | vendor_advisory |
| nvd-echoleak | NIST NVD | [CVE-2025-32711 record](https://nvd.nist.gov/vuln/detail/cve-2025-32711) | vulnerability_record |
| echoleak-paper | Reddy and Gujral | [EchoLeak independent case-study paper](https://arxiv.org/abs/2509.10540) | independent_research |
| google-armor | Google Cloud | [Model Armor overview](https://docs.cloud.google.com/model-armor/overview) | product_documentation |
| google-frontier | Google DeepMind | [Introducing Frontier Safety Framework (historical baseline)](https://deepmind.google/blog/introducing-the-frontier-safety-framework/) | governance_framework |
| meta-purple | Meta | [Purple Llama official repository](https://github.com/meta-llama/PurpleLlama) | official_repository |
| aws-guardrail | AWS | [ApplyGuardrail independent API](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-independent-api.html) | product_documentation |
| aws-version | AWS | [Deploy your guardrail](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-deploy.html) | product_documentation |
| nvidia-rails | NVIDIA | [Guardrail Types](https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/rail-types) | product_documentation |
| nvidia-eval | NVIDIA | [Evaluate Configuration](https://docs.nvidia.com/nemo/guardrails/evaluation/evaluate-configuration) | product_documentation |
| alibaba-ops | Alibaba Cloud | [Security Operations Agent](https://www.alibabacloud.com/help/en/content-moderation/latest/how-to-use-the-security-operation-agent) | product_documentation |
| alibaba-workspace | Alibaba Cloud | [Model Studio workspaces](https://www.alibabacloud.com/help/en/model-studio/use-workspace) | product_documentation |
| volc-gateway | Volcengine | [AI Gateway overview](https://docs.volcengine.com/docs/apig/What_is_the_AI_Gateway?lang=zh) | product_documentation |
| tencent-waf | Tencent Cloud | [LLM Web Application Firewall](https://cloud.tencent.com/product/llmwaf) | product_documentation |
| tencent-routing | Tencent Cloud | [Model routing safety configuration](https://cloud.tencent.com/document/product/1829/135297) | product_documentation |
| baidu-guard | Baidu Cloud | [AI Safety Guardrail](https://cloud.baidu.com/product/AIGCSEC/platform.html) | product_documentation |
| kuaishou-esg | Kuaishou | [2025 ESG release](https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-releases-2025-esg-report-deepening-green-operations-and) | company_report |
| nist-genai | NIST | [AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | standard_framework |
| owasp-llm | OWASP | [Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) | community_framework |
| mitre-atlas | MITRE | [ATLAS](https://atlas.mitre.org/) | community_framework |
| cac-label | 国家网信办 | [人工智能生成合成内容标识办法](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm) | regulation |

## 读取限制

Microsoft CVE页面需要JavaScript，本项目没有直接取得其公告正文，相关Case以Microsoft来源的NVD条目与独立案例论文辅助核验。Google Frontier Safety Framework来源为2024年初始材料，不能据其内容宣称当前最新版的具体要求。

MITRE ATLAS交互首页未返回可读正文，本项目仅提供框架入口，不声称完成其全部技术目录核验。各来源的读取状态和限制记录在JSON索引中。

外链会变化；`verified_at`是本次读取日期，不是首次发布时间。结构校验不保证所有外链长期可用。涉及版本敏感能力，实施时重新阅读对应文档。
