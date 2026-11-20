# 徐大头手绘短视频制作 Skill

把一件生活小事做成中文手绘口播短视频。工作流覆盖选题、口播稿、旁白、逐句分镜、剪辑、双比例封面和交付检查。你可以带上自有角色和声音，在任一阶段接着做。

这份版本整理自「徐大头」系列的制作方法，提供文字指令和虚构示例。Claude、Codex 等支持 Agent Skills 的工具可按各自的技能安装方式加载 `skills/xudatou-handdrawn-video/`。出图、配音与导出由使用者选用的工具完成。

## 安装与第一次使用

1. 下载本仓库，把完整的 `skills/xudatou-handdrawn-video/` 复制到你的视频项目的 `.agents/skills/` 下。复制完成后应能找到 `.agents/skills/xudatou-handdrawn-video/SKILL.md`，脚本和参考文件也在同一个技能目录里。
2. 在 Codex 中打开你的视频项目，开始新对话。输入 `$xudatou-handdrawn-video`，附上自己的经历或已有文稿，例如：

```text
使用 $xudatou-handdrawn-video。把下面这件事写成第一人称聊天口吻的口播稿，
保留我提供的事实。这轮交完整逐字稿和建议的第一处画面。
```

第一次可以只做稿件。已有稿时，提供当前稿件并说明是否锁定。已有配音时，一并提供音频，可要求逐句分镜和按实际声音对齐的时间表。已有工程时，指明当前工程和本次要改的部分。

- [技能入口](skills/xudatou-handdrawn-video/SKILL.md)
- [示例《一页纸打成了二十份》](examples/printer-story.md)
- [单集制作卡](skills/xudatou-handdrawn-video/references/episode-template.md) · [可填写的分镜表 CSV](skills/xudatou-handdrawn-video/templates/shot-list.csv)

## 准备自己的人物项目

在视频项目中准备自己的 `人物项目/` 目录，放入角色基准图和可授权使用的音色。Skill 会检查人物参考与音色，给出缺项的制作提示。水印、片尾和封面参考按制作需要补充。在本仓库目录可用 Python 3 手动检查：

```sh
python3 skills/xudatou-handdrawn-video/scripts/check_assets.py "/你的项目/人物项目"
```

在 Windows 也可用 `py -3` 运行同一个脚本。需要出图、配音、剪辑时，准备对应工具。工具暂时缺失时，可以先交提示词、配音稿或剪辑交接表。 [人物项目目录和检查方式](skills/xudatou-handdrawn-video/references/project-assets.md)

## 维护与提交

在本仓库目录运行 `python3 -m unittest discover -s tests -v` 检查素材识别。发布时从这份目录建立仓库，用 `git diff --cached --name-only` 核对待提交的说明、虚构示例、模板、脚本和测试文件。制作用的人物图、音色和品牌素材存放在各自的视频项目目录。
