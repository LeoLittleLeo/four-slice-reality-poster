# Four-Slice Reality Poster

> 将一张照片重构为一个由 **Reality + 30% / 65% / 90% 抽象状态**组成的四状态编辑海报，同时尽量保留人物身份、建筑识别度与原始场景语义。

`four-slice-reality-poster` 是一个面向 Codex / Agent 图像工作流的 Skill。

它不是把照片简单切成四条，再分别套上不同强度的滤镜，而是先建立四个等分的 **隐藏逻辑区（Logical Zones）**，再依据人物、建筑、树木、道路、阴影、色块和笔触等语义结构，将它们转化为四个面积大致均衡、边界可不规则的 **可见视觉模块（Visible Modules）**。

最终目标：

> **一个摄影级 Reality 状态 + 三个清晰不同、且非线性递进的抽象状态，组成一张完整而统一的海报。**

---

## ✦ Visual Objective

这个 Skill 首先保证四种视觉状态都可以被清晰感知，其次才追求整体融合。

默认使用 **Hybrid Transition**：

* 背景和大型色块可以在模块之间发生明显变化；
* 人物、建筑等重要主体保持语义连续；
* 模块边缘不需要是矩形；
* 不要求所有边界完全无缝；
* 四个模块在面积和视觉重量上保持大致均衡；
* 最终结果必须像 **一张完整海报**，而不是四张独立图片的拼接。

---

## ✦ Four-State System

Skill 首先根据原图的构图方向建立四个等分的隐藏逻辑区。

```text
Vertical division

┌────┬────┬────┬────┐
│ Z1 │ Z2 │ Z3 │ Z4 │
└────┴────┴────┴────┘
```

或：

```text
Horizontal division

┌──────────────┐
│      Z1      │
├──────────────┤
│      Z2      │
├──────────────┤
│      Z3      │
├──────────────┤
│      Z4      │
└──────────────┘
```

这四个区域只决定 **视觉状态的逻辑归属**。

它们并不意味着最终必须出现四个矩形切片。

最终可见边界可以沿着：

* 人体轮廓；
* 人群边缘；
* 建筑结构；
* 天际线；
* 树冠；
* 道路；
* 阴影；
* 大型色块；
* 表现性笔触；

形成更加自然、更加接近编辑设计与艺术拼贴的模块。

---

## ✦ Reality Anchor

四个逻辑区中只会选择一个 **Reality Anchor**，作为主要摄影现实状态。

默认锚点选择优先级：

1. **主体人物脸部所在逻辑区**
2. **主要人群语义所在逻辑区**
3. **重要建筑所在逻辑区**
4. 如果以上均不存在，则默认选择 **Logical Zone 2**

剩余三个逻辑区分别获得：

* `30%` abstraction
* `65%` abstraction
* `90%` abstraction

三个抽象等级各出现一次。

它们**不要求按照空间位置机械递增或递减**。

例如：

```text
Reality → 65% → 30% → 90%
```

完全可以比：

```text
Reality → 30% → 65% → 90%
```

更适合某张照片。

状态分配由以下因素共同决定：

* 画面平衡；
* 主体语义；
* 节奏；
* 色彩；
* 建筑和人物位置；
* 整体视觉反差。

---

## ✦ Abstraction Is Structural

本 Skill 不把抽象理解成：

```text
30% blur
65% blur
90% blur
```

抽象必须真正改变：

* 结构；
* 形态；
* 空间；
* 信息密度；
* 组件组织方式；
* 摄影表面的保留程度。

30%、65%、90% 的差异主要体现在：

* 细节保留量；
* 组件密度；
* 空间位置忠实度；
* 形状忠实度；
* 摄影纹理保留程度；
* 重复元素的合并、缩减和省略程度。

例如，原图中的：

* 密集树木；
* 大量窗户；
* 重复楼房；
* 密集人群；
* 道路纹理；
* 背景家具；

都可以被重新分组、简化甚至部分省略。

但必须保护：

* 主体人物；
* 身份关键人脸；
* 核心人群事件；
* 标志性建筑；
* 决定场景身份的主要结构。

### People

人物优先：

> **Simplify people before breaking them.**

也就是优先减少：

* 肌肤细节；
* 衣物细节；
* 小型纹理；
* 局部颜色变化；

而不是破坏：

* 人体轮廓；
* 头部结构；
* 四肢关系；
* 姿态；
* 人物身份。

### Architecture

建筑优先：

> **Remove architectural detail before architectural identity.**

优先减少：

* 窗户；
* 材质；
* 表面纹理；
* 装饰；
* 重复结构。

尽量保留：

* 建筑轮廓；
* 主体体块；
* 透视；
* 标志性结构；
* 建筑身份。

详细规则：

[`references/abstraction-language.md`](references/abstraction-language.md)

---

## ✦ Face Identity Lock

人物身份保护是整个 Skill 的最高优先级。

核心目标不是：

> 必须把原图人脸逐像素贴回去。

而是：

> **最终人物必须保持可识别身份、自然面部结构，以及连贯的头部—颈部—肩部关系。**

生成完成后，首先执行 **Face Restoration Gate**。

如果当前候选人脸已经满足：

* 身份可识别；
* 面部比例正确；
* 眼、鼻、口位置自然；
* 下颌与面颊结构连贯；
* 发际线自然；
* 脸部与颈部连接正常；
* 没有明显生成瑕疵；

则：

```text
KEEP CURRENT FACE
```

不再进行源像素恢复。

只有当人脸出现明显身份或结构错误时，才进入恢复流程。

```text
Candidate A
     ↓
Face Restoration Gate
     │
     ├── Face acceptable
     │       ↓
     │   Keep Candidate A
     │
     └── Face unacceptable
             ↓
       Attempt restoration
             ↓
        Candidate B
             ↓
        Compare A / B
             ↓
Only keep B when visibly better
```

恢复优先级：

1. 不恢复；
2. 不规则语义人脸 Mask；
3. 已验证几何对齐的源人脸恢复；
4. 矩形 Face Box，仅作为最后 fallback。

如果恢复后出现：

* 人脸像贴片；
* 几何错位；
* 发际线错位；
* 肤色断层；
* 头部与身体断裂；
* 下颌和颈部连接异常；
* 比恢复前更不自然；

则必须退回 Candidate A。

核心原则：

> **Preserve identity before pixels.**

> **自然且身份正确的人脸，优先于错误的“原图贴脸”。**

---

## ✦ Human Continuity

人脸身份正确并不意味着人物处理完成。

最终还必须保证：

```text
Face
 ↓
Head contour
 ↓
Jaw
 ↓
Neck
 ↓
Shoulders
 ↓
Body
```

形成连续而自然的结构。

模块边界可以穿过人物附近，但不能制造：

* 错位抠图；
* 头身错位；
* 双重轮廓；
* 肩部断裂；
* 重影；
* 人物局部平移；
* 类似 Photoshop 抠图未对齐的残次效果。

---

## ✦ Architecture Across States

重要建筑不需要被完整锁死在 Reality 区域。

当建筑成为视觉锚点时：

* 身份关键区域保持摄影真实；
* 建筑可以继续跨入邻近抽象状态；
* 抽象区域优先减少窗户、材质与纹理；
* 主要轮廓、体块与标志性结构继续保留。

因此，同一栋建筑可以同时存在于：

```text
Reality
   ↓
30% abstraction
   ↓
65% abstraction
```

甚至跨越更多视觉模块。

这种连续性可以强化：

> **同一主体在现实与抽象之间的反差。**

---

## ✦ Irregular Visible Modules

虽然逻辑层严格维护四等分区域，但最终视觉层不需要表现成规则四切片。

推荐从场景本身寻找边界：

```text
logical zones
       ↓
semantic interpretation
       ↓
irregular visible modules
```

例如：

```text
人物轮廓
建筑屋顶
树木边缘
道路曲线
阴影
天空
大型色块
绘画笔触
```

都可以成为视觉模块的边界。

核心原则：

> **Hidden ownership is mathematical. Visible boundaries are designed.**

---

## ✦ Default Color Identity

如果用户没有指定其他方向，Skill 默认使用一种受 *Robot Dreams* 整体视觉气质启发的色彩系统：

> **温暖、怀旧、阳光感、略带复古、情绪柔和。**

主要颜色家族：

* cream
* warm beige
* dusty peach
* muted coral
* terracotta
* warm brown
* ochre
* muted yellow
* dusty sky blue
* powder blue
* muted teal
* softened blue-green
* sage
* dusty olive

少量强调色可以使用：

* tomato red
* coral
* navy
* warm denim

### One Universe, Four Roles

四个模块需要存在于同一个电影色情绪世界，但不应全部套用相同色调。

例如：

```text
Slice A → terracotta / warm brown / sand
Slice B → cream / dusty peach / warm beige
Slice C → dusty blue / muted teal
Slice D → ochre / muted yellow / soft brick
```

这不是固定分配，只是示例。

核心公式：

```text
ONE SHARED CINEMATIC COLOR UNIVERSE

+

FOUR DISTINCT DOMINANT COLOR ROLES

=

ONE COHERENT BUT CLEARLY MODULAR POSTER
```

模块之间允许利用：

* 冷暖差；
* 主色差；
* 明度差；
* 大型色块差；
* Accent 差异；

产生清晰边界。

不需要依赖人工分割线。

详细规则：

[`references/cinematic-color-system.md`](references/cinematic-color-system.md)

---

## ✦ Decision Priority

当不同规则发生冲突时，按以下优先级处理：

1. **Primary Face Identity & Natural Facial Coherence**
2. **Head / Shoulder / Human Body Continuity**
3. **Reality Anchor Role & Local Source Preservation**
4. **Architectural Identity**
5. **Four-State Readability & Abstraction Assignment**
6. **Robot Dreams-Inspired Color Identity**
7. **Intentional Modular Boundary Design**
8. **Artistic Experimentation**

低优先级规则不得破坏高优先级保护区域。

例如：

```text
漂亮的抽象效果
```

不能优先于：

```text
正确的人脸身份
```

同样：

```text
漂亮的不规则边界
```

不能优先于：

```text
自然的人体连续性
```

---

## ✦ Workflow

```text
Input Photo
    ↓
Analyze
people / faces / architecture / semantic flow
    ↓
Create 4 equal hidden logical zones
    ↓
Choose Reality Anchor
    ↓
Assign 30% / 65% / 90%
    ↓
Choose distinct structural abstraction languages
    ↓
Establish shared cinematic palette
    ↓
Generate four-state composition
    ↓
Convert logical zones
into irregular visible modules
    ↓
Face Restoration Gate
    ↓
Poster-level art direction
    ↓
Subject & structure validation
    ↓
Final Poster
```

---

## ✦ Installation

将仓库放入你的 Codex / Agent Skills 目录。

例如：

```bash
git clone https://github.com/LeoLittleLeo/four-slice-reality-poster.git \
  ~/.codex/skills/four-slice-reality-poster
```

更新：

```bash
cd ~/.codex/skills/four-slice-reality-poster

git pull
```

如果你的 Codex 环境使用其他 Skill 路径，只需要把仓库放到对应 Skills 目录。

---

## ✦ Usage

安装后，可以在支持 Skill 调用的环境中使用：

```text
Use $four-slice-reality-poster to transform my photo into a readable
four-state poster with irregular modules and identity-safe face handling.
```

中文：

```text
使用 $four-slice-reality-poster 处理这张照片。

保留一个摄影级 Reality 状态，并生成 30%、65%、90%
三个结构上明显不同的抽象状态。

保持四个区域清晰可读，允许不规则语义边界，
并优先保护人物身份与自然的人体连续性。
```

也可以追加自定义要求：

```text
使用 $four-slice-reality-poster 处理这张图。

最上方模块使用水墨语言；
最下方模块加入中国古汉字的飘逸结构感；
不要添加文案。
```

或者：

```text
使用 $four-slice-reality-poster 处理。

主体建筑尽量跨越两个视觉模块，
但必须保持建筑身份。
```

用户明确指定的视觉方向可以覆盖默认艺术风格，但仍然必须遵守：

* 人脸身份保护；
* 人体结构连续性；
* 建筑身份保护；
* 四状态可读性。

---

## ✦ Optional Restoration Tool

仓库包含：

```text
scripts/restore_protected_anchor.py
```

这个脚本 **不是默认生成流程**。

它仅用于：

> **Face Restoration Gate 失败后的条件性恢复候选。**

依赖：

```bash
pip install Pillow
```

支持四种模式：

```text
face-mask
```

使用不规则语义 Mask 恢复人脸。

```text
face-core
```

矩形人脸区域恢复，仅作为最后 fallback。

```text
source-mask
```

通过 Mask 恢复不包含主体人脸的源图区域。

```text
full-anchor
```

恢复完整逻辑 Anchor，仅适用于确认没有主体人脸的场景。

查看参数：

```bash
python scripts/restore_protected_anchor.py --help
```

脚本会要求显式确认：

* Face Restoration Gate 是否失败；
* 几何对齐是否已经验证；
* Mask 是否避开主体人脸；
* 当前场景是否不存在主体人脸；

以防止恢复脚本绕过 Skill 本身的人脸保护逻辑。

---

## ✦ Repository Structure

```text
four-slice-reality-poster/
├── SKILL.md
├── README.md
│
├── agents/
│   └── openai.yaml
│
├── references/
│   ├── abstraction-language.md
│   ├── cinematic-color-system.md
│   ├── composition-and-anchor.md
│   ├── intentional-modular-composition.md
│   └── subjects-validation.md
│
└── scripts/
    └── restore_protected_anchor.py
```

| File                                 | Responsibility                 |
| ------------------------------------ | ------------------------------ |
| `SKILL.md`                           | Skill 主入口、视觉目标、完整工作流与决策优先级     |
| `composition-and-anchor.md`          | 四逻辑区、Reality Anchor、状态分配与主体连续性 |
| `abstraction-language.md`            | 抽象方法与 30 / 65 / 90% 等级校准       |
| `cinematic-color-system.md`          | 默认电影配色系统与模块色彩关系                |
| `intentional-modular-composition.md` | 不规则视觉模块、边界与视觉节奏                |
| `subjects-validation.md`             | 人物、建筑、硬约束与最终验收                 |
| `restore_protected_anchor.py`        | 条件性源像素恢复候选生成                   |
| `agents/openai.yaml`                 | Agent 展示信息与默认调用 Prompt         |

---

## ✦ Core Principles

```text
Preserve identity before pixels.
```

```text
Simplify people before breaking them.
```

```text
Remove architectural detail before architectural identity.
```

```text
Reduce repeated components before weakening core semantic identity.
```

```text
Make abstraction structural, not filter-based.
```

```text
Keep hidden logical ownership mathematically equal.
```

```text
Make visible module boundaries irregular, designed, and readable.
```

```text
Use one shared color universe,
but allow four distinct dominant color roles.
```

```text
Deliver one coherent poster,
never four independent images.
```

---

## ✦ In One Sentence

> **在同一张照片中，让现实、轻度抽象、中度抽象与高度抽象同时存在，并通过语义边界、结构重构、人物身份保护与统一电影配色，让四种状态既明显不同，又属于同一个世界。**
