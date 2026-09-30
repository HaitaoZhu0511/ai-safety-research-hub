# AI Safety Research Hub · AI 安全研究与应用

面向安全策略、审核产品、数据分析和 Agent 工程的公开研究项目。整理主流大厂的 AI 安全资讯、治理方法、工程工具、业务场景和典型案例，将研究结论转成可实施的控制与评测设计。

**v0.2 · 资料核验日期：2026-09-30。** 现收录12家公司、39条来源、9个案例、12类应用场景和11条精选动态。新增24个已运行的离线控制用例与45个单元测试；原16个模型评测设计仍未执行。内容以中文原创分析为主，引用原始页面，不重新托管厂商文档、模型和攻击题包。

## 一分钟运行

Python3.10+，不需要模型API Key或真实数据库：

```bash
python scripts/run_demo.py
python scripts/run_evals.py
python scripts/cost_model.py
```

演示：未批准导出进入人工审查；批准后改参被拒绝；确切提案成功；同请求重试不重复执行；审计回放不执行工具。查看[完整运行说明与生产边界](docs/offline-demo.md)及[验证结果](reports/README.md)。

## 快速阅读

- 想看可执行控制：阅读[离线演示](docs/offline-demo.md)和[Agent/MCP安全](docs/agent-mcp-security.md)。
- 想整合机审人审：阅读[人机审核运营](docs/human-review-operations.md)。
- 想选评测工具：阅读[工具与评测选型](docs/tools-and-evaluation.md)。
- 想维护研究结论：阅读[来源版本维护](docs/source-maintenance.md)和[控制对应](methodology/control-crosswalk.md)。
- 想了解大厂在做什么：阅读[公司实践对照](docs/company-comparison.md)。
- 想分析典型Case：阅读[案例地图](cases/README.md)。
- 想搭建平台：阅读[安全架构与工作流](docs/architecture.md)。
- 想服务实际业务：阅读[应用场景](docs/scenarios.md)。
- 想做评测和降本：阅读[评测与指标](docs/evaluation.md)和[成本收益](docs/cost-and-value.md)。
- 想准备面试/项目计划：阅读[90天实施路线](docs/roadmap.md)。
- 想查看近期材料：阅读[精选资讯](news/README.md)和[来源索引](sources/README.md)。

## 研究范围

| 层面 | 核心问题 | 主要产出 |
| --- | --- | --- |
| 内容与输出安全 | 是否有害、误杀、幻觉、标识缺失 | 风险标签、证据、分级处置 |
| 模型与能力治理 | 风险能力、发布门禁、残余风险 | 风险评测、模型报告、发布批准 |
| 应用与Agent安全 | 注入、越权、泄密、工具副作用 | 权限、沙箱、审批、出站控制 |
| 数据与隐私 | 跨租户、敏感数据、训练/检索污染 | ACL、脱敏、数据血缘 |
| 运营与人机协同 | 人审、申诉、漂移、成本 | 队列、抽检、回流、效果归因 |

## 大厂覆盖

| 公司 | 主要学习方向 | 专题 |
| --- | --- | --- |
| OpenAI | 输入/输出/工具Guardrail与人工批准 | [阅读](companies/openai.md) |
| Anthropic | 风险治理、分类器与行为评测 | [阅读](companies/anthropic.md) |
| Microsoft | 企业内容安全与AI红队 | [阅读](companies/microsoft.md) |
| Google / DeepMind | 组织基线与模型能力风险 | [阅读](companies/google.md) |
| Meta | 开放安全模型与评测工具 | [阅读](companies/meta.md) |
| Amazon Web Services | 模型解耦的Guardrail服务 | [阅读](companies/aws.md) |
| NVIDIA | 五段式Rails与联合评测 | [阅读](companies/nvidia.md) |
| 阿里巴巴 / 阿里云 | 安全运营Agent与空间隔离 | [阅读](companies/alibaba.md) |
| 字节跳动 / 火山引擎 | AI网关、AgentKit安全围栏与可观测 | [阅读](companies/bytedance.md) |
| 腾讯 / 腾讯云 | LLM WAF与路由防护 | [阅读](companies/tencent.md) |
| 百度 / 百度智能云 | 大模型与Agent安全护栏 | [阅读](companies/baidu.md) |
| 快手 / 可灵AI | 内容生态、AIGC标识与商业治理 | [阅读](companies/kuaishou.md) |

公司治理、公开研究、云产品与真实事故具有不同证据性质。每篇专题与Case均说明材料类型和适用边界。24项合成控制测试已经执行；16项模型测试仍只是设计。没有调用真实厂商接口或生成厂商排名。AgentKit新增资料仅取得官方搜索索引摘录，正文访问超时；OWASP2026资料已核验资源页，全文条目迁移尚未完成。

## 应用到既有项目

- [SLG游戏数据Agent](https://github.com/HaitaoZhu0511/game-agent-demo)：只读SQL、指标血缘、租户隔离、名单处置授权。
- [AI短剧数据Agent](https://github.com/HaitaoZhu0511/ai-short-drama-data-agent)：剧本/图文/音频安全、素材权利、生成标识、发布门禁。
- [商业化安全审核数据中台](https://github.com/HaitaoZhu0511/commercial-safety-review-data-hub)：政策与模型版本、人审、申诉、风险曝光和商业收益。

## 基础工作流

```mermaid
flowchart LR
    A[业务与风险定义] --> B[数据/身份/权限]
    B --> C[输入与检索控制]
    C --> D[模型与工具提案]
    D --> E[确定性授权/人工审批]
    E --> F[执行与输出校验]
    F --> G[审计/抽检/申诉]
    G --> H[评测/影子/灰度/回滚]
    H --> C
```

## 项目结构

```text
companies/     12家公司专题
cases/         9个案例分析与Case地图
catalog/       公司、来源、风险、场景、案例、精选动态JSON
news/          精选资讯与维护约定
sources/       来源索引与证据规则
methodology/   风险治理和威胁建模方法
playbooks/     事故响应、红队与策略发布
contracts/     风险事件JSON Schema
evals/         24个离线控制用例 + 16个未执行模型测试设计
runtime/       合成数据、权限、批准、幂等与审计回放
reports/       已运行控制用例的结果摘要
tests/         控制、契约、收益计算与资料校验测试
scripts/       资料一致性与链接路径校验
.github/       3.10/3.12/3.13多版本CI
```

## 验证与维护

资料校验、演示、Golden Set和收益计算仅用Python标准库；完整单元测试需要JSON Schema开发依赖：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/run_evals.py
```

校验JSON、跨目录引用、来源ID、日期、Case类型、必需文件和本地Markdown路径；不进行线上安全扫描、不把结构校验当模型评测。新增资料时按[维护规则](CONTRIBUTING.md)补充来源、性质和核验日期。

45个单元测试覆盖权限、批准角色与快照、过期、幂等、停用、审计变化、事件Schema、结果报告一致性、收益算例和资料校验。[变更记录](CHANGELOG.md)区分已完成与后续项。

后续路线：完整来源版本快照、授权环境下的真实模型评测、真实数据库RLS/事务幂等、人审队列服务和审核前置试点。当前没有定时更新任务，资讯目录按人工核验维护。

## 安全边界

这是研究项目和单进程合成演示，不是已部署的AI安全中台。演示身份不是认证、内存状态不持久、哈希链不等于签名审计；没有真实MCP、任意SQL、内容分类器或外发动作。[安全约定](SECURITY.md)说明数据与授权边界。收益计算是可调整的假设，不是实际业绩。

## 许可证

本仓库原创分析和示例代码采用 MIT；外部文档、模型、数据集与代码使用各自许可证。尤其 Meta 工具与模型组件的许可不同，部署前按具体版本核对。
