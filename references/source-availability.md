# 导师方案的来源可用性

本阶段的 20 份技能入口均已取得。每份入口按原清单指定的 GitHub 提交核对。连同直接讲解方法的文档、提示词、模板、脚本及重定位的关联材料，归集 286 个不同的仓库文件。同一文件只在本阶段计一次。文件数量仅用于复查来源。

以下记录影响复查的缺件、路径调整和容易误当原始资料的示例。每个入口的完整方法对应关系见本技能的来源对照。

| 上游入口 | 待核项目 | 核查结果与影响 |
|---|---|---|
| [idea-spark](https://github.com/microsoft/ResearchStudio/blob/063f10088af49909e1a4a7ea8d29efe19633f34e/ResearchStudio-Idea/skills/idea_spark/SKILL.md) | 旧的质量规范 quality-v2.md | 两个 schema 说明都引用该旧文件名，固定提交中没有同名文件。已核对同目录 quality-flow.md、质量检查脚本及各阶段提示词；保留可见标准，不回填旧版条款。 |
| [research-pipeline-planner](https://github.com/yananlong/codex-skills/blob/a9bad384ae7e04eea38ab5efb13529ae4b664575/research/research-pipeline-planner/SKILL.md) | 共享审查模式与示例程序 | 通过固定仓库的审查模块找回 review_schema.py。scripts/run_b1.py 出现在项目执行任务示例中，由使用者提供，不能当成一个已运行实验。 |
| [research-questions](https://github.com/EricssonResearch/academic-writing-review/blob/1082254ce3a5c4e0309c617cc26d2376999bd2cf/skills/research-questions/SKILL.md) | 示例论文路径 | ../path/file.tex 和 conclusions.tex 是帮助理解问题追踪表的示例。用当前方案的真实主张和证据位置填表。 |

原文中同名的项目输入、生成文件、个人机器路径与学术书目的作用各异。凡无法从公开材料确认的指令，不以推测补写为上游原话。
