# 从想法到导师能决定的方案

## 先建立能交接的底稿

读取用户材料和本阶段已有选题卡、缺口证据表或查新结论，保留其原编号、原文位置、日期、范围和已否决项目。手头只有一句想法就从这句话建立同样的记录。优先去查会改变路线的事实。若只有摘要，把它用在摘要能支持的位置。从零开始可以照着[可运行的示例](../examples/aperture/proposal.json)填写。语句由执行者按本题写，不照搬示例里的光学模型或数值门槛。

请先用三句话回答：如果导师只批一个动作，希望批哪个？哪个公开结果或用户观察使它值得做？如果最简单解释也能得到同一现象，哪个观测能区分？由此写出一项主贡献、一条可能令它失效的解释、明确删去的一项复杂设计。没有必要引入 AI 时，无需专设 AI 路线。时间和资源缺数字时，给出确定数字所需的短试验或导师决定，区分估算与实测。

## 先比较有区分力的备选

| 本轮动作 | 必须留下的判断 |
| --- | --- |
| 还原最近似工作 | 它研究了什么、图或公式支持哪句话、在本课题哪个边界仍可作为强基准。若它已经完成整个主张，收窄问题再重做对照。 |
| 同条件比较 | 写下不加新部件时的自然方案和推荐方案。把两条路线放在相同的信息、算量、测量时刻和输出定义下。解释为何增加的复杂度值得，更便宜的路线能验证哪一半。 |
| 预写结果判据 | 对主解释和竞争解释各写一个在同一干预下的可观测预言。定义单位、分母、有效重复和足以改变行动的分辨率。理论任务可用反例、极限和可区分的预测。 |
| 设计最低成本的判别 | 从复现、必要性或删减、失效边界中选最能改变决定的一项。明确计算或测量步骤、输入和控制变量、预计资源、主图横纵轴，以及支持、转向、无法区分各走哪一步。若要识别交互效应，比较需要的因素组合，并用匹配资源的基线检验。 |
| 核对可执行性 | 先核单位、量级、边界与信息是否可得。任务约束允许时，直接运行不需新外部资源的解析校验或小模拟，保存输入、程序、输出和解读。规划真实现场实验、大算力任务或采购时，交付排期、资源、触发条件。 |

试算失败也会改变方案。先查单位、可观测量、共享归一化和实现，再判断假设是否受反证。基础对照未通过便先修模型。对结果看来相同的方案，说明是科学上给出同一预测，还是工具的分辨率不足。将事后才发现的指标标成探索性，重写预测后再以独立条件验证。

## 根据证据修订到可以开会

质疑者先问：“即使预期的曲线出现，哪种更简单解释仍然成立？假设它是真的，原方案会得到什么？”执行者用原文或新的对照回应。把每条意见落到具体主张、测试或资源决定。替代解释可用当前预算区分就立即改设计，再审一次。证据需要下一阶段才能产生时，写明谁在什么条件下作何决定。只重复同一轮评分没有新信息时停止；若发现不可满足的硬约束，交付一份建议收窄或放弃的方案及理由，同样可以开会。论证已足够时交付正文、可执行的验证次序、已删路线与交接底稿。用户只审现有稿或只做口头演练时沿用原文与要求。

## 从正常入口运行工具

1. 在研究项目中运行 `python "<skill>/scripts/proposal.py" init "<case>/proposal.json"`。已有档案则直接读取。填入根字段与 sources、hypotheses、routes、tests，具体字段参见[完整实例](../examples/aperture/proposal.json)。其中 sources 的 ref 指可访问的出版物链接或项目内真实材料。level 选择 original、abstract、metadata 或 user_record。用同一标识符从假设追踪到比较、决策与下一步。
2. allowed_modes 取用户允许的 simulation、analytic、existing_data、field、laboratory、qualitative 中的适用项。其他方法可用 other 并在范围中写明，tests.mode 必须在其中。默认 test 的 purpose 为 discriminate，至少有一项主验证直接比较互异预测。辅助诊断可标 sanity 或 calibration，并只引用它实际检验的路线。每个 test 对应所比较的解释、路线、观察量、分辨率、对照、预算，以及三种结果的行动。理论研究的“基线”可以是既有定理或特殊情形。“已执行”要有案内非空产物与具体阅读结果；计划用 planned。数值型结果可登记 measurements，每项用 path 选择 JSON 单元格、digits 指定显示小数位、display 指定稿内数值，phrase 用包含 {value} 的短句绑定量名与数值；程序会和结果句一起核对。使用运行工具生成的产物，可在 run_receipt 指向回执，让程序比对文件指纹和成功状态。
3. 运行 `python "<skill>/scripts/proposal.py" check "<case>/proposal.json"`。退出码 0 表示结构可追踪，1 给出需补齐的内容，2 表示输入或路径无效。再运行 `python "<skill>/scripts/proposal.py" brief "<case>/proposal.json"` 生成可读初稿。初稿相对链接以案例目录为准。核对原文和实际数字，按导师要作的决定整理成完整简报。工具不能判读科学真伪或替导师立项。
4. 没有 Python 的环境可以人工运行同一表。若证据有限，用材料确能支撑的条件式计划交付，把未决部分指向一次具体行动。整个过程可以独立完成，进已有技能链时将同一主张、路线编号及负结果交给后续阶段。

## 工作流的固定来源

下列为原 20 个技能之外直接采用的 6 个入口。每条均指向实际采用的版本。每一行的操作都出现在上述流程或输出字段中。

| 入口 | 实际纳入的操作 | 在本阶段怎样使用 |
| --- | --- | --- |
| [ARIS 方案细化与规划](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/research-refine-pipeline/SKILL.md) | 先固定研究问题与主贡献，再判断旧方案能否复用，记录删掉的复杂度，然后沿同一主张编号排验证。 | 输入检查、同条件比较与主线修订。 |
| [ARIS 实验计划](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/experiment-plan/SKILL.md) | 将主张、竞争解释、强基线、可读结果、资源和运行顺序绑定到同一验证块。 | tests、优先级与下一里程碑。 |
| [ARIS 消融规划](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/ablation-planner/SKILL.md) | 为每一删减指明所排除解释，评估对照、重复及资源，删去不能改变判断的对比。 | 必要性、敏感性与停止条件。 |
| [AutoResearchClaw 假设构造](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/researchclaw/skills/builtin/experiment/hypothesis-formulation/SKILL.md) | 从同一观察构造竞争机制，预写可区分预言和混杂因素。 | hypotheses、observable、controls。 |
| [AutoResearchClaw 对照设计](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/researchclaw/skills/builtin/experiment/experimental-design/SKILL.md) | 在匹配预算下采用有意义的基线，随机系统检查重复，报告计算代价。 | 根据对象选择重复或确定性收敛检查。 |
| [Kalaris 自主科研工作流](https://github.com/KalarisLabs/research-agent-skills/blob/a74b0dbe5fa865d73b9f250ba5b0c9f107bd1baa/skills/autoresearch/SKILL.md) | 小循环检验一项预测，大循环根据反常或阴性结果回到文献、改换解释、继续或停止。 | 记录预测、实际试算和导致改案的证据。 |

上游默认的机器学习数据集、自动调度、固定种子数和会议投稿流程不属于本阶段必需条件。使用者要求的研究对象、可用资源和交付决定优先。原 20 个入口各自的操作与模板见[原来源逐项对照](source-map.md)。
