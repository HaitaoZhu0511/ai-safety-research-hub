# 显著案例地图

| 案例 | 性质 | 重点 | 分析 |
| --- | --- | --- | --- |
| EchoLeak：企业Copilot的间接注入与信息泄露 | disclosed_vulnerability | 隔离外部文档指令，检索执行用户级ACL，检查输出链接和资源加载，并限制敏感信息到外部域的传输。 | [阅读](echoleak.md) |
| Constitutional Classifiers：越狱防护与可用性权衡 | controlled_research | 为风险领域定义政策、合成样本、正常近邻对照和留出攻击集；联合观察攻击成功、正常拒绝、延迟和成本。 | [阅读](constitutional-classifiers.md) |
| Agentic Misalignment：受控模拟中的目标冲突 | controlled_simulation | 让授权限制独立于任务目标；对外发、删除、财务和人事动作做确定性检查，监控实际执行而非只判断最终回答。 | [阅读](agentic-misalignment.md) |
| 2026行为研究：代码干预与评测标签偏移 | controlled_simulation | 评测结果要有人类盲审和多裁判一致性；分离被评对象与发布批准者，校验代码Diff和外发结果。 | [阅读](agentic-summer2026.md) |
| Project Vend：现实试验中的经营权限与社会诱导 | real_world_experiment | 建立价格下限、采购预算、独立账本、库存与价格校验；模型提案经业务规则批准后执行，并对长期任务做状态核对。 | [阅读](project-vend.md) |
| 快手：商品发布前AI辅助纠错与业务保护 | company_report | 把审核前移到提交阶段；输出问题位置和整改建议，持续追踪一次通过、重复驳回、事后风险与净业务收益。 | [阅读](kuaishou-commerce.md) |
| 阿里云：安全运营Agent辅助评测与策略调优 | product_application | 自动化样本整理、评测和候选参数生成；将训练/调优集与评测留出集隔离，候选策略先影子运行再批准上线。 | [阅读](alibaba-security-ops.md) |
| Google Model Armor：组织基线与只检测运行 | product_application | 新策略先收集影子检测事件，并使用正常流量估计误杀；分别管理输入输出模板和日志敏感字段。 | [阅读](model-armor-shadow.md) |

## 如何使用

选一个Case，先描述业务目标和受影响资产，再画出信任边界，明确系统实际上允许了什么。随后把问题转换成一个正常对照和一个风险回归用例。最后给出执行位置、负责人、指标和剩余风险。

Case性质必须保留：已披露漏洞、受控研究、受控模拟、现实试验、公司报告、公开产品应用并不等价。这里没有将模拟研究写成“某公司线上发生泄密”，也没有把产品介绍写成量化成功案例。

## v0.2补充

[火山AgentKit：围栏信号与授权分层](volc-agentkit.md)，性质为产品应用分析，不是真实攻击事故。材料读取边界已在案例和来源目录注明。
