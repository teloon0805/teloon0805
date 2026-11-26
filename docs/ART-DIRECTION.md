# 水墨版视觉说明

## 构图与字体

头图以墨黑留白为基础，左侧呈现 Bodoni MT 斜体字标、行书中文名和两行学历，右侧呈现缓慢流动的双弧墨色、银灰环纹与黑白云水。远山、芦苇和笔触纹理在雾气中逐渐隐去。

研究主线采用三组居中的书法标题，搭配居中的英文与楷体说明。桌面横排、手机纵排，避免将桌面图片直接缩成难读的小字。

动画分为不同节奏：主体 40 秒回旋、外侧笔触 82 秒反向流转、云气 17/23 秒漂移、水纹 26 秒循环。文字只在加载时有轻微的入墨变化；减少动态效果时使用静态构图。

多波束案例插图、邮箱与落款同步调整为暗色水墨配色。多波束图形仍为原创方法示意，不是实际海域或实验图；数字对应论文中的特定案例。

## 素材

- 背景：`assets/ink-landscape.jpg`，内置图像生成工具（built-in image_gen）生成并按暗色要求编辑的绘画，经等比例缩放及 JPEG 压缩用于网页。
- 最终图：`assets/hero.svg`、`hero-mobile.svg`、`research.svg` 等。底景内嵌于 SVG，文字、墨色构图与动画由源代码生成。
- 实现：`scripts/build_ink_assets.py`。没有使用第三方游戏图片或字体文件分发。

## 底景生成提示词

```text
Edit this background painting into the user's requested DARK BLACK-AND-WHITE ink landscape for a personal profile banner. Preserve the panoramic composition, sophisticated painterly detail, broad EMPTY LEFT HALF for separate typography, mountain forms toward the far right, low water and mist, and wide open area near the right-middle for separate animated circular artwork. Replace the warm paper with matte near-black charcoal and layered deep graphite atmosphere. Strictly MONOCHROME: black, charcoal, cool neutral gray, silver-white fog. Mountains and reeds should be expressed in pale dry-brush silver ink and charcoal silhouettes, disappearing into multiple layers of flowing white-gray mist. Finely nuanced brush texture, exquisite soft fog transitions, restrained highlights, very deep dark negative space. Left half should remain near black and quiet with only the faintest ink texture for highly readable light typography. Keep the far-right painting rich but subtle, no harsh whites, no glossy or plastic rendering, no neon. Think a refined ink painting seen at midnight, elegant black-and-white film grain, not fantasy game art. The large circular animated symbol will be added separately: DO NOT draw any yin-yang or bagua symbols in this background. No text, no calligraphy, no letters, no logo, no stamps, no warm beige, no gold, no brown, no saturated color, no UI or cards, no watermark.
```
