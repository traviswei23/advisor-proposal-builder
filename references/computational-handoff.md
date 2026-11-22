# 从导师方案到可复用的计算证据

当一次解析检查或小型模拟能判断方案是否可行，执行与用户授权、资源范围相符的那一项，将结果带回导师简报。用户还要求完成计算研究时，按下面的次序做到有可核实的结果，同时保留失败项。对已经有结果的任务，可以从核对结果开始。整理方案和大规模运行各有清楚的结束条件。

### 单次运行

记录拟区分的主张、能观察的差异、评测命令与对照、外推边界和单轮预算。项目内的 Python 脚本若能将结果以 JSON 输出至标准输出，可用标准库工具运行。例如对本技能的光学案例：

```text
python "<skill>/scripts/capture_run.py" --case "<case>" --run-id centered-v1 --script pilot.py --timeout 60
```

成功时在 `<case>/runs/centered-v1/` 写入执行回执、输入指纹、命令参数、原始输出和 result.json。用可重复的 `--input 文件` 登记会改变结果的数据、参数或导入模块。额外命令参数放在 `--` 之后。只运行已审视、属于任务的项目代码。运行编号已存在时先看回执，重试另取编号。超时、非零退出、无可读 JSON、非有限数字或声明的输入在运行中变化都要留痕。保存方式适用于有界的小型任务；长任务或大输出采用项目已有调度器并保留等价证据。回执只能证明该程序产生了这份输出。派生数值仍须回到输入、模型和对照解读。

### 何时从一轮转入下一轮

- 先用能手算、查表或独立推导的例子验单位、方向和数量级。通过后复现强基线；把两条路线放在相同输入、预算和指标下。需求是纯模拟时，现场数据的未知条件写成参数区间或适用边界。
- 在看结果前写出预期、阈值依据和什么结果会推翻解释。调参和探索的数据与最终比较分开。随机模型分清独立样本和同轨迹的重复读数；确定性模型用步长、网格或截断范围测试收敛。比较交互作用时保留匹配的多因素条件。
- 主结果检查通过才追加必要的删减与失效边界。若失败，先重放最近一次成功输入，定位第一处差异。更改指标或条件后重新建立同口径基线。把预算用完也没区分开的假设写成下一次导师选择。
- 对每个可报告结论保存编号、代码与输入、关键参数、原始结果文件、图表与能支持的范围。将“推导证明”“在这些条件下数值验证”“尚待解释”分别落到原句。把结果包与经过收窄的主张交给写作技能，或者直接提供给作者。无需申请额外平台账号便可用本地流程复查。

### 工作簿中 21 个实施入口如何运用

下列 21 个入口来自工作簿“③ 实施并形成结果”在原 100 项之外的部分。与前一页的 6 个新来源有 3 个重复；Karpathy 是程序，NanoResearch 在这里作为骨架参考。单个案子按上面的决策顺序调用适用部分，实验室或远端计算使用实际可用的工具。原工作流中专用的模型训练、云环境、长期调度和实时通知由实际任务决定。

| 固定版入口 | 在当前任务中执行的动作、产物或触发条件 |
| --- | --- |
| [physics-research-numerics](https://github.com/qjgoisz/physics-research-agent-kit/blob/ee2a4dffb76dd8916830cca72cee9800ca0c1274/skills/physics-research-numerics/SKILL.md) | 先统一量、单位和归一化，再用解析极限、守恒或对称性及离散收敛验算。把获准外推的区间写入结果索引。 |
| [experiment-bridge](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/experiment-bridge/SKILL.md) | 把计划逐块对应到已有代码或待实现函数。先跑可手算的小例，按基线、主效果、删减的顺序收结果，每块回填计划号。 |
| [experiment-pipeline](https://github.com/EvoScientist/EvoSkills/blob/85ad685d1df5ed1d7fe641564d04bb8a3dec8f28/skills/experiment-pipeline/SKILL.md) | 先复现基线，探索参数用开发条件，固定后再测目标路线与消融。各阶段按预设容差和预算判断能否继续。 |
| [autoresearch-skill](https://github.com/wjgoarxiv/autoresearch-skill/blob/c4c5948994dd9000eb19d69afcb8d62c05bf0112/SKILL.md) | 在可度量任务中冻结评测命令、主指标与保护条件。每轮提出一种可辨认更改，实跑、判读、留日志；无可靠评分器时保留人工原文判读。 |
| [result-to-claim](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/result-to-claim/SKILL.md) | 将原始文件、参数、图号与结果声明绑定；从结果逐句写出支持、仅部分支持及需要新证据的说法后交写作。 |
| [experiment-craft](https://github.com/EvoScientist/EvoSkills/blob/85ad685d1df5ed1d7fe641564d04bb8a3dec8f28/skills/experiment-craft/SKILL.md) | 隔离失败样本，找到最近成功版本，缩小两者之间的差异；提出一个能解释故障的机制并独立重跑。 |
| [research-implement-feature](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/research-implement-feature/SKILL.md) | 按功能从输入到结果先打通最小实现。逐项记录默认假设、暂缺模块和实际触发路径。占位输出不能进入证据表。 |
| [run-experiment](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/run-experiment/SKILL.md) | 登记运行环境、命令、资源与输出路径，确认任务真实启动。启动日志和结束产物分别记录。 |
| [monitor-experiment](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/monitor-experiment/SKILL.md) | 按任务标识检查进程、输出增长和结果文件。失联先定位原任务；确认失败后再重试，避免重复消耗。 |
| [analyze-results](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/analyze-results/SKILL.md) | 从原文件汇总同条件结果，分清随机重复、参数扫点和数值精度，报告差异大小及误差来源。 |
| [experiment-audit](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/experiment-audit/SKILL.md) | 核结果文件存在、标签或参照量来源、归一化、实际执行的代码路径及结论范围。代理量只支持与该代理有关的说法。 |
| [hiera-experiment](https://github.com/PKU-DAIR/AutoSci/blob/aa852fd929128545ee3dce2e5629a4aeeab6ccf9/.claude/skills/hiera-experiment/SKILL.md) | 冻结候选源码、输入和评测条件，保存指纹。算法变更给新编号。已有远程尝试先找回原回执，恢复时避免重复提交。 |
| [exp-run](https://github.com/PKU-DAIR/AutoSci/blob/aa852fd929128545ee3dce2e5629a4aeeab6ccf9/.claude/skills/exp-run/SKILL.md) | 区分派发与收集。先记录目标、分配标识和启动结果，再取回退出状态、日志与可解析产物。只看到排队不能标为完成。 |
| [formula-derivation](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/formula-derivation/SKILL.md) | 推导先写不变量、假设、符号和要证的式子，逐步核查量纲与退化极限；与数值不合时优先找首个产生差异的步骤。 |
| [experiment-queue](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/experiment-queue/SKILL.md) | 参数网格分批运行，登记依赖关系与状态。恢复时跳过有证据的已完成项；显存不足或重复超时时先收缩任务再扩批。 |
| [research-refine-pipeline](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/research-refine-pipeline/SKILL.md) | 保持研究问题和主贡献稳定，注明删去的复杂度，把最需证明的主张交给实验计划。 |
| [experiment-plan](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/experiment-plan/SKILL.md) | 每一主张配一个有判别力的试验块、最强基线、成本和预期图；排出先后与终止条件。 |
| [experiment-iterative-coder](https://github.com/EvoScientist/EvoSkills/blob/85ad685d1df5ed1d7fe641564d04bb8a3dec8f28/skills/experiment-iterative-coder/SKILL.md) | 把实现拆成能检查的几段。每轮只验一个行为，保存有效版本、失败原因，正确性尚未通过时先修复再优化。 |
| [ablation-planner](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/ablation-planner/SKILL.md) | 删除、替换或扰乱一个关键部件，检查它的必要性；疑有交互时保留组合条件。 |
| [autoresearch（原版程序）](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md) | 可借用固定评价口径、单轮预算及保留所有尝试的记录。仅在可比较的优化任务中用指标选优；科学解释还要保留反例和阴性结果。 |
| [nanoresearch-experiment](https://github.com/OpenRaiser/NanoResearch/blob/584fd06f295bda51712311794e63ee7b7a68f930/skills/nanoresearch-experiment/SKILL.md) | 只在缺少程序结构时借用数据、模型、评价、配置与入口分层。生成的骨架必须经实际运行才能产生科研结果。 |

完整计算研究还参考 [ARIS research-pipeline](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/research-pipeline/SKILL.md) 的阶段交接。恢复工作时核对上次实际产物和本次条件，从首个失效环节继续；反复得到同一无信息结果时改验证方式或收尾。
