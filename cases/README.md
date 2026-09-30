# 显著案例地图

现收录15个Case。厂商报告、受控研究、模拟、现实试验、漏洞与产品应用分开，不以一个分母统计“事故率”。

| 案例 | 性质 | 核心学习点 | 分析 |
| --- | --- | --- | --- |
| EchoLeak：企业Copilot的间接注入与信息泄露 | disclosed_vulnerability | 隔离外部文档指令，检索执行用户级ACL，检查输出链接和资源加载，并限制敏感信息到外部域的传输。 | [阅读](echoleak.md) |
| Constitutional Classifiers：越狱防护与可用性权衡 | controlled_research | 为风险领域定义政策、合成样本、正常近邻对照和留出攻击集；联合观察攻击成功、正常拒绝、延迟和成本。 | [阅读](constitutional-classifiers.md) |
| Agentic Misalignment：受控模拟中的目标冲突 | controlled_simulation | 让授权限制独立于任务目标；对外发、删除、财务和人事动作做确定性检查，监控实际执行而非只判断最终回答。 | [阅读](agentic-misalignment.md) |
| 2026行为研究：代码干预与评测标签偏移 | controlled_simulation | 评测结果要有人类盲审和多裁判一致性；分离被评对象与发布批准者，校验代码Diff和外发结果。 | [阅读](agentic-summer2026.md) |
| Project Vend：现实试验中的经营权限与社会诱导 | real_world_experiment | 建立价格下限、采购预算、独立账本、库存与价格校验；模型提案经业务规则批准后执行，并对长期任务做状态核对。 | [阅读](project-vend.md) |
| 快手：商品发布前AI辅助纠错与业务保护 | company_report | 把审核前移到提交阶段；输出问题位置和整改建议，持续追踪一次通过、重复驳回、事后风险与净业务收益。 | [阅读](kuaishou-commerce.md) |
| 阿里云：安全运营Agent辅助评测与策略调优 | product_application | 自动化样本整理、评测和候选参数生成；将训练/调优集与评测留出集隔离，候选策略先影子运行再批准上线。 | [阅读](alibaba-security-ops.md) |
| Google Model Armor：组织基线与只检测运行 | product_application | 新策略先收集影子检测事件，并使用正常流量估计误杀；分别管理输入输出模板和日志敏感字段。 | [阅读](model-armor-shadow.md) |
| 火山AgentKit：安全围栏信号与工具授权分层 | product_application | 将输入输出检测、授权、独立批准与执行回执分开；留存政策和组件版本，联合观察误拦、危险动作及成本。 | [阅读](volc-agentkit.md) |
| Constitutional Classifiers++：两级检测与整段交互 | controlled_research | 把级联筛查、人审升级和正常对照组合评测，统计最终漏放、误拦与单位正确完成成本。 | [阅读](classifiers-cascade.md) |
| Anthropic网络滥用调查：从单条内容到跨任务行为 | company_report | 关联授权目标、任务轨迹与工具副作用，保留合法安全开发对照，调查建议和封禁执行分开。 | [阅读](agentic-cyber-abuse.md) |
| Meta LlamaFirewall：多扫描器与任务轨迹检查 | product_application | 对齐扫描结论与模型/工具/批准/回执轨迹；确定性权限即使扫描漏检仍拒绝危险动作。 | [阅读](llama-firewall.md) |
| AWS Automated Reasoning：政策一致不等于事实为真 | product_application | 先复核规则提取和变量覆盖，再核对证据；检测反馈由业务决策层处理，缺证据要澄清。 | [阅读](automated-reasoning.md) |
| 阿里云VOD：人工覆盖机审与旧播放链接撤销边界 | product_application | 版本绑定人工结论，分源站/CDN/渠道验证访问撤销；留存受控证据并管理申诉期限。 | [阅读](vod-review-revocation.md) |
| 腾讯COS：视频截帧与公有读冻结的真实范围 | product_application | 审核输入记录采样方式与覆盖模态，对短时片段、音频和跨帧风险另做测试；按访问路径验收冻结。 | [阅读](video-frame-freeze.md) |

## 如何使用

先明确业务目标、受影响资产和信任边界，再区分检测、裁决、授权与实际动作。每个Case都给出证据限制、可迁移方法及正常/风险回归建议。产品介绍不能写成客户已遭攻击；模拟不写成线上泄密。

本轮新增6篇分析及E17—E22验证设计，见[2026-10-01增补](../news/2026-10-01-research-roundup.md)。这些设计均未执行，不能混入24个已运行离线控制用例。[上下文级联方法](../methodology/context-and-cascade-review.md)和[证据处置闭环](../methodology/evidence-to-enforcement.md)提供组合应用路线。
