# 新建云端环境时可粘贴的配置要求

请为我的 `eian-collage-broll` Fork 创建一套**独立**的 Codex Cloud 环境，建议命名为 `eian-collage-broll-tts-2`。这套环境只关联这个 Fork，不关联、修改或复用 `sweety-handdraw-video`、`guofeng-video-pipeline`、旧手绘对话和旧云环境。

请按仓库内 `.agents/skills/eian-collage-broll/SKILL.md` 与 references 使用作者原版纸拼贴工作流。不要修改作者 Skill 文件。火山豆包语音合成 2.0 由仓库外层的 `tools/volc_tts.py` 独立负责：读取我最终确认的原文，使用 `seed-tts-2.0` 和可配置音色，生成 MP3 与服务返回的时间信息。默认音色仅作初始测试；若账户无权限请报告，不要自动换音色或反复计费请求。不要改写我的台词。

安装阶段只准备该仓库需要的 Python 与图片工作流工具。先离线运行脚本测试和 `--dry-run`，不要在配置阶段调用付费 TTS。网络仅允许必要域名 `openspeech.bytedance.com`（HTTPS 443）。`VOLC_TTS_API_KEY` 使用这个新环境请求的网络密钥，并由我的 Personal vault 为这个环境单独提供；不在聊天、GitHub、脚本或日志中记录真实密钥。环境隐私设为“仅限我自己”。

请如实报告：作者 Skill 最终只交付 `first-frame.png`、`last-frame.png`、`video-prompt.txt`；它不会自行合成有声成片。正式使用时先让我要确认文案和音色，做一次经我授权的短句 TTS 测试并核对 MP3，再推进视觉制作。发布环境前列出需要我检查的配置和未验证项。

