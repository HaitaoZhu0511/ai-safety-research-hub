# 工具学习与评测选型

## 开源工具与研究环境

| 工具 | 已核验用途 | 学习重点 | 不应承诺 |
| --- | --- | --- | --- |
| [Microsoft PyRIT](https://github.com/microsoft/PyRIT) | 生成式AI风险识别框架 | 实验对象、评分、记录与红队组织 | 运行工具等于完成红队 |
| [NVIDIA garak](https://github.com/NVIDIA/garak) | 模型漏洞探测与结果记录 | Probe、检测器、目标版本和预算 | 一套探测覆盖所有业务权限 |
| [AgentDojo](https://github.com/ethz-spylab/agentdojo) | Agent提示注入与防护评测环境 | 正常任务与危险目标分别判定 | 基准成功率等于生产事件概率 |
| [Meta Purple Llama](https://github.com/meta-llama/PurpleLlama) | 安全组件与评测工具集合 | 分类、Prompt防护及组件许可 | 组件共用一套许可证 |

已读取官方README和资源说明，没有安装或运行这些框架，没有上传业务样本。AgentDojo不是大厂产品，属于研究机构项目，单独说明来源性质。

## 本轮新增组件与云产品

以下是不同层的选型候选，不是一个可直接横比的开源榜单。

| 组件/服务 | 可学习能力 | 接入前必须核验 | 分析 |
| --- | --- | --- | --- |
| Meta LlamaFirewall | 提示、任务对齐、代码与自定义扫描器组合 | 每个扫描器版本、外部调用/凭据、许可、可观察轨迹字段；不索取隐藏思维链 | [Case](../cases/llama-firewall.md) |
| Meta Llama Guard 4 | 文本/图像联合风险分类 | 英语优化、中文验证、生成图像支持限制；不是所有短剧素材都适用 | [专题](../companies/meta.md) |
| Microsoft Prompt Shields | 用户提示与文档注入检测 | detected/filtered区别、Spotlighting预览范围与Token成本 | [专题](../companies/microsoft.md) |
| AWS Automated Reasoning | 已建模政策内的文本逻辑一致性 | 政策抽取保真、变量覆盖、US English、无流式；不验证凭据真实性或替代注入防护 | [Case](../cases/automated-reasoning.md) |
| OpenAI Moderation | 独立内容检测与工作流审核信号 | 支持输入、覆盖对象、完整输出后分数、错误处理；不提供业务授权 | [专题](../companies/openai.md) |

## 生命周期提醒

2026-10-01核验[OpenAI退役文档](https://developers.openai.com/api/docs/deprecations)：2026-06-03公告，Evals计划2026-10-31转只读，Evals dashboard/API及Agent Builder计划2026-11-30关闭。可以学习Trace、数据切片及回归方法，但新项目应避免绑定待退役平台，迁移前复查具体产品范围；这不表示所有评测方法或全部OpenAI API退役。也不把Anthropic内部激活探针研究视为第三方可直接调用的审核接口。

## 接入顺序

先运行本项目[离线权限控制](offline-demo.md)，确保危险提案即使由模型提出也无法执行；再在授权沙箱接入模型和工具基准，固定工具/模型/政策/数据集/裁判版本，最后加入业务正常样本与专家标签。

## 每次实测的报告字段

范围与授权、版本、数据许可和脱敏、攻击目标、有效尝试定义、预算/重试、正常任务结果、真实副作用、裁判一致性、人类复核、时延、成本、失败详情和未覆盖风险。模型最终说拒绝不代表前面的工具没有执行。

## 解释边界

不同工具、攻击预算和任务集之间的数字不能直接横比。本项目24个Golden用例测的是确定性控制逻辑；22个设计用例和外部模型基准尚未执行。没有厂商安全排行榜。
