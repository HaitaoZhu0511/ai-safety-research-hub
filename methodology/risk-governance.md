# 风险治理与威胁建模

## 统一语言

AI Safety关注有害结果、行为失配和高危能力；AI Security关注注入、越权、数据泄漏和供应链；Trust & Safety关注平台内容、主体、分发、交易、人审和申诉。三者共同落在“资产—威胁—边界—控制—证据—负责人”模型。

## 七步方法

1. **定义业务目标**：允许Agent完成什么，哪些动作必须经批准，哪些数据可进入模型。
2. **画资产与边界**：系统指令、用户消息、外部文档、检索库、工具、数据库、浏览器和外部接收者。
3. **枚举失败路径**：注入改变任务；正常任务泄密；有害用户请求；误判；评测偏移；预算失控。
4. **评估影响**：严重度、可逆性、波及人数、预计曝光、交易影响和数据敏感度。分数只是优先级，重大风险不可被平均收益抵消。
5. **分配控制**：输入检测、检索ACL、参数Schema、动作权限、人工批准、沙箱、出站控制、输出检测。
6. **设计验证**：一条危险路径至少有正常对照、风险回归、执行回执和负责人。
7. **运行与复盘**：抽检、申诉、漂移、事件响应、版本回滚和样本回流。

## 风险登记表

| 字段 | 含义 |
| --- | --- |
| risk_id / scenario | 风险与业务场景 |
| asset / trust_boundary | 受影响资产和边界 |
| owner | 业务/工程/策略责任人 |
| prevention / detection / response | 预防、检测、处置 |
| evidence | 验证证据和审计字段 |
| residual_risk | 仍不能阻止的风险 |
| approval / expiry | 例外批准与到期 |

## 与公开框架连接

- [NIST生成式AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)：参考全生命周期治理与测量。
- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/)：作为应用风险清单入口，不当作可直接套用的认证标准。
- [MITRE ATLAS](https://atlas.mitre.org/)：参考对抗AI技术的分类，连接测试与监控。
- [Anthropic RSP](https://www.anthropic.com/responsible-scaling-policy)：学习风险报告与版本管理；具体门槛须阅读相应版本全文。
- [DeepMind历史框架](https://deepmind.google/blog/introducing-the-frontier-safety-framework/)：学习能力评测、预警和部署保障的连接，来源为2024年初始版。

## 本项目风险目录

见[12类风险](../catalog/risks.json)。框架用于组织问题，实际门禁由业务、工程和策略负责人共同决定。
