# 来源索引与证据规则

本轮增补：2026-10-01。共54条来源；每条真实核验日、访问限制与备注见[结构化目录](../catalog/sources.json)。旧材料不批量改为今天，最新更新不代表所有历史资料重新验证。

## 证据性质

- 官方治理/产品文档说明公开方法和支持范围，不证明独立生产效果；预览、地域和版本另查。
- 官方研究只证明给定条件下的观察；厂商调查披露不等于独立归因或全行业事故率。
- 漏洞公告、受控模拟、现实试验与产品应用分开标记。
- search_excerpt只取得官方搜索索引，不能等同直接正文；HTTP200也不能证明正文可读。
- 本项目控制、场景、指标和回归方案为原创建议；模型与产品基准没有实际运行。

## 来源列表

| ID | 发布方 | 材料 | 类型 | 访问等级 |
| --- | --- | --- | --- | --- |
| openai-guardrails | OpenAI | [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) | product_documentation | content_retrieved |
| openai-safety | OpenAI | [Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices) | product_documentation | content_retrieved |
| anthropic-rsp | Anthropic | [Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy) | governance_framework | content_retrieved |
| anthropic-classifiers | Anthropic | [Constitutional Classifiers](https://www.anthropic.com/news/constitutional-classifiers) | research | content_retrieved |
| anthropic-misalignment | Anthropic | [Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment) | research | content_retrieved |
| anthropic-summer2026 | Anthropic | [Agentic Misalignment in Summer 2026](https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/) | research | content_retrieved |
| anthropic-vend1 | Anthropic | [Project Vend phase one](https://www.anthropic.com/research/project-vend-1) | real_world_experiment | content_retrieved |
| anthropic-vend2 | Anthropic | [Project Vend phase two](https://www.anthropic.com/research/project-vend-2) | real_world_experiment | content_retrieved |
| anthropic-bloom | Anthropic | [Bloom automated behavioral evaluations](https://alignment.anthropic.com/2025/bloom-auto-evals/) | research | content_retrieved |
| ms-redteam | Microsoft | [Microsoft AI Red Team](https://learn.microsoft.com/en-us/security/ai-red-team/) | product_documentation | content_retrieved |
| ms-content | Microsoft | [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/cognitive-services/content-safety/overview) | product_documentation | content_retrieved |
| ms-cve | Microsoft | [CVE-2025-32711 vendor advisory](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711) | vendor_advisory | javascript_required |
| nvd-echoleak | NIST NVD | [CVE-2025-32711 record](https://nvd.nist.gov/vuln/detail/cve-2025-32711) | vulnerability_record | content_retrieved |
| echoleak-paper | Reddy and Gujral | [EchoLeak independent case-study paper](https://arxiv.org/abs/2509.10540) | independent_research | content_retrieved |
| google-armor | Google Cloud | [Model Armor overview](https://docs.cloud.google.com/model-armor/overview) | product_documentation | content_retrieved |
| google-frontier | Google DeepMind | [Introducing Frontier Safety Framework (historical baseline)](https://deepmind.google/blog/introducing-the-frontier-safety-framework/) | governance_framework | content_retrieved |
| meta-purple | Meta | [Purple Llama official repository](https://github.com/meta-llama/PurpleLlama) | official_repository | content_retrieved |
| aws-guardrail | AWS | [ApplyGuardrail independent API](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-independent-api.html) | product_documentation | content_retrieved |
| aws-version | AWS | [Deploy your guardrail](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-deploy.html) | product_documentation | content_retrieved |
| nvidia-rails | NVIDIA | [Guardrail Types](https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/rail-types) | product_documentation | content_retrieved |
| nvidia-eval | NVIDIA | [Evaluate Configuration](https://docs.nvidia.com/nemo/guardrails/evaluation/evaluate-configuration) | product_documentation | content_retrieved |
| alibaba-ops | Alibaba Cloud | [Security Operations Agent](https://www.alibabacloud.com/help/en/content-moderation/latest/how-to-use-the-security-operation-agent) | product_documentation | content_retrieved |
| alibaba-workspace | Alibaba Cloud | [Model Studio workspaces](https://www.alibabacloud.com/help/en/model-studio/use-workspace) | product_documentation | content_retrieved |
| volc-gateway | Volcengine | [AI Gateway overview](https://docs.volcengine.com/docs/apig/What_is_the_AI_Gateway?lang=zh) | product_documentation | content_retrieved |
| tencent-waf | Tencent Cloud | [LLM Web Application Firewall](https://cloud.tencent.com/product/llmwaf) | product_documentation | content_retrieved |
| tencent-routing | Tencent Cloud | [Model routing safety configuration](https://cloud.tencent.com/document/product/1829/135297) | product_documentation | content_retrieved |
| baidu-guard | Baidu Cloud | [AI Safety Guardrail](https://cloud.baidu.com/product/AIGCSEC/platform.html) | product_documentation | content_retrieved |
| kuaishou-esg | Kuaishou | [2025 ESG release](https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-releases-2025-esg-report-deepening-green-operations-and) | company_report | content_retrieved |
| nist-genai | NIST | [AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | standard_framework | content_retrieved |
| owasp-llm | OWASP | [Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) | community_framework | content_retrieved |
| mitre-atlas | MITRE | [ATLAS](https://atlas.mitre.org/) | community_framework | javascript_required |
| cac-label | 国家网信办 | [人工智能生成合成内容标识办法](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm) | regulation | content_retrieved |
| openai-mcp | OpenAI | [MCP servers: risks and approvals](https://developers.openai.com/api/docs/guides/tools-connectors-mcp) | product_documentation | content_retrieved |
| owasp-llm-2026 | OWASP | [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) | community_framework | content_retrieved |
| owasp-agentic-2026 | OWASP | [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | community_framework | content_retrieved |
| ms-pyrit | Microsoft | [PyRIT official repository](https://github.com/microsoft/PyRIT) | official_repository | content_retrieved |
| nvidia-garak | NVIDIA | [garak official repository](https://github.com/NVIDIA/garak) | official_repository | content_retrieved |
| agentdojo | ETH Zurich / Invariant Labs | [AgentDojo official repository](https://github.com/ethz-spylab/agentdojo) | official_repository | content_retrieved |
| volc-agentkit | Volcengine | [AgentKit Guardrails overview](https://docs.volcengine.com/docs/agentkit/Guardrailsoverview?lang=zh) | product_documentation | search_excerpt |
| openai-moderation | OpenAI | [Moderation: signals, tool coverage and streaming](https://developers.openai.com/api/docs/guides/moderation) | product_documentation | content_retrieved |
| openai-agent-safety | OpenAI | [Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety) | product_documentation | content_retrieved |
| openai-agent-evals | OpenAI | [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) | product_documentation | content_retrieved |
| openai-deprecations | OpenAI | [Deprecations: Agent Builder and Evals transition](https://developers.openai.com/api/docs/deprecations) | product_documentation | content_retrieved |
| anthropic-classifiers-next | Anthropic | [Next-generation Constitutional Classifiers](https://www.anthropic.com/research/next-generation-constitutional-classifiers) | research | content_retrieved |
| anthropic-cyber-campaign | Anthropic | [Disrupting an AI-orchestrated cyber espionage campaign](https://www.anthropic.com/news/disrupting-AI-espionage) | company_report | content_retrieved |
| anthropic-misuse-sep2026 | Anthropic | [Detecting and countering misuse of AI: September 2026](https://www.anthropic.com/threat-intelligence-report-september-2026) | company_report | content_retrieved |
| meta-firewall | Meta | [LlamaFirewall official README](https://raw.githubusercontent.com/meta-llama/PurpleLlama/main/LlamaFirewall/README.md) | official_repository | content_retrieved |
| meta-guard4 | Meta | [Llama Guard 4: image support and limitations](https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama-guard-4) | product_documentation | content_retrieved |
| ms-prompt-shields | Microsoft | [Prompt Shields and Spotlighting](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection) | product_documentation | content_retrieved |
| aws-reasoning | AWS | [Automated Reasoning checks in Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html) | product_documentation | content_retrieved |
| google-saif-assessment | Google | [SAIF Risk Assessment tool introduction](https://blog.google/innovation-and-ai/technology/safety-security/google-ai-saif-risk-assessment/) | product_announcement | content_retrieved |
| alibaba-vod-review | Alibaba Cloud | [ApsaraVideo VOD: Automated review](https://www.alibabacloud.com/help/en/vod/user-guide/automated-review-1) | product_documentation | content_retrieved |
| tencent-video-review | Tencent Cloud | [COS video moderation and public-read freeze](https://cloud.tencent.com/document/product/436/134929) | product_documentation | content_retrieved |
| volc-runtime-security | Volcengine | [AgentKit Runtime security best practices](https://docs.volcengine.com/docs/agentkit/Runtime_security_best_practices?lang=zh) | product_documentation | search_excerpt |

本轮15条新增资料详见[资讯分析](../news/2026-10-01-research-roundup.md)。[复核台账](../catalog/source-review.json)保留证据范围与下一步；未保存完整网页快照，不提供未生成的哈希或历史版本差异。
