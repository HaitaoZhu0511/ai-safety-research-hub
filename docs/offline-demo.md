# v0.3离线演示与验证

## 运行

Python3.10+，演示和24项控制套件只用标准库：

```bash
python scripts/run_demo.py
python scripts/run_evals.py
python scripts/validate.py
```

完整单元测试还包括JSON Schema检查，使用隔离环境：

```bash
python -m venv .venv
# Windows: .venv/Scripts/python；Linux/macOS: .venv/bin/python
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/python -m unittest discover -s tests -v
```

Linux把上述解释器路径替换为.venv/bin/python。命令只打印结果，不创建报告文件或联系业务服务。GitHub CI使用3.10、3.12、3.13重新执行。

## 一条可解释的闭环

未批准导出 → review；批准导出2条后提议3条 → block；执行确切批准提案 → allow；同一请求重复 → 返回原回执，不重复执行；随后回放事件链，不重放工具。

聚合工具只允许dau、retention_d7两个虚构指标；导出只生成合成记录引用，目标是internal://audit。任意SQL、文件路径、Shell和互联网目标不在工具接口内。

## 控制边界

| 控制 | 实现位置 | 覆盖 |
| --- | --- | --- |
| 角色与租户 | runtime/safety.py服务侧注册表 | 用户声明的参数不能修改角色 |
| 允许工具与参数 | _guard | 精确字段、指标、行数与目的地 |
| 敏感动作批准 | approve / execute | 用户、租户、ID、参数、工具、完整政策快照 |
| 批准有效期 | 注入时钟 | 到期时不能产生新执行 |
| 幂等 | 用户+请求ID缓存，同实例可重入锁 | 同ID改参拒绝；线程并发重试只执行一次 |
| 紧急停用 | disabled | 优先于已批准请求和缓存读取 |
| 审计 | _emit / replay | 请求者、操作人、审批人、理由、版本、回执、链连续性 |
| 风险分类 | RISK_BY_REASON / Golden标签断言 | 区分权限、隐私、资源预算与管理停用 |

同一请求成功后的原回执重取可以不再提交批准：这不产生新副作用，且仍检查当前权限、政策与紧急停用。它不等于旧批准永久有效。

## 用例与结果

[Golden Set](../evals/control-golden.json)包含5项正常对照和19项风险/边界断言；[结果](../reports/README.md)记录实际运行。原有16个[模型评测设计](../evals/design-cases.json)仍未执行，两套材料不可混算。

66个单元测试另覆盖线程并发、审批人追溯、事件分类、契约与报告一致性。顶层用例risk_ids是设计覆盖，expected.risk_ids才是实际事件标签断言，二者不能混为模型检出结果。详见[修复说明与契约迁移](control-hardening.md)。

## 不具备的生产保障

身份注册表不是认证系统；用户标识来自演示调用端，不是已验证的JWT。批准与幂等状态只在单实例内存，重启丢失；线程锁不保障多实例/多进程或真实工具的事务幂等。停用等待当前临界区结束，不抢占在执行的动作。哈希链不是签名，能重写全部事件的人能重算链；发现尾部删减还需可信外部锚点。

没有SQL解析、真实行级权限、模型判别、PII分类器、网络隔离或真实MCP协议实现。生产版本必须接入认证/IAM、数据库RLS、事务幂等、可靠执行状态机、独立审批服务、审计存储和密钥管理。不要把此代码作为完整安全网关上线。

[生产接入路线](production-integration.md)补充累计预算、故障恢复、SLG指标与权限、短剧血缘、人审申诉和质量/收益联合验收，均为待实施设计。
