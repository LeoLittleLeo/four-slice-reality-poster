# Four-Slice Reality Poster

> 将一张照片重构为一个由 **Reality + 30% / 65% / 90% 抽象状态**组成的四状态编辑海报，同时尽量保留人物身份、建筑识别度与原始场景语义。

`four-slice-reality-poster` 是一个面向 Codex / Agent 图像工作流的 Skill。

它把**同一张照片**分成四个**自然区域**，每个区域只是抽象方式不同（Reality + 30% / 65% / 90% 抽象状态）——不是四张纸片拼贴。边界以**纸面材质层**来表现：在抽象状态变化处画一条撕纸接缝；没有 z-order、没有整片纸身体、没有把各区变成独立纸片的纸纹。

场景只出现一次；唯一强制保护的是主头部。

可选边界家族：`collage`（分层撕纸纸片）、`torn`（legacy 有序撕纸条带）、`contour`（语义轮廓）、`mask`（自绘区域）、`rect`（等分直条）。

```text
DEFAULT / natural                        LEGACY / torn-strip

  ┌─────────────────────┐                |~~~~|~~~~|~~~~|~~~~|
  │   region 1 (30%)    │                四根波浪条 + 三根米白线
  │ ~~~~纸面接缝~~~~~  │
  │  Reality (photo)    │
  │ ~~~~纸面接缝~~~~~  │       NOT:
  │   region 3 (65%)    │                ┌─────────────────────┐
  │ ~~~~纸面接缝~~~~~  │                │ 纸片1   │ 纸片2  │
  │   region 4 (90%)    │                │  纸片3  │ 纸片4  │
  └─────────────────────┘                └─────────────────────┘
  一幅照片，四个自然区域，               四张纸片拼贴
  边界=纸面材质接缝
```

最终目标：

> **一个摄影级 Reality 状态 + 三个清晰不同、且非线性递进的抽象状态，组成一张完整而统一的海报。**

---

## ✦ Visual Objective

这个 Skill 首先保证四种视觉状态都可以被清晰感知，其次才追求整体融合。

默认使用 **Natural Regions（自然区域）**：

* **同一幅照片**被四个自然区域共同组成，每个区域只是抽象方式不同；
* 区域是照片的一部分，不是独立纸片（无 z-order、无整片纸身体、无纸纹分层）；
* 边界以**纸面材质层**来表现：抽象状态变化处画一条撕纸接缝；
* Reality 保持摄影质感（源图合成），并与各区共享同一微暖 Robot Dreams 调色；
* 三个抽象区域必须使用三种**不同的主抽象方法**（30% ≠ 65% ≠ 90%），共享同一照片视觉系统；
* 场景只出现一次；禁止 blob 分割、孤岛、contact sheet、2×2、四张完整照片、gutters。

核心原则：

> **ONE PHOTO + FOUR NATURAL REGIONS + EACH REGION DIFFERS ONLY BY ABSTRACTION**

> **THE PAPER MATERIAL LAYER IS THE REPRESENTATION OF THE BOUNDARY**

BAD（反例）：

```text
四张独立纸片拼贴（z-order 层叠、单侧纸影、整片纸纹）
同一方法三档强度冒充三种抽象
四根窄竖波浪条
每区用完全不相关的媒介（彩铅 + 低多边形 + 水彩）
```

GOOD（正例）：

```text
同一幅照片的四个自然区域
边界处有一条撕纸纸面接缝
每区一种不同的主抽象方法，但同属这一张照片
```

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

默认（Torn-Strip）下，最终可见边界是三条贯穿画布的撕纸式接缝：

* 多尺度不规则（低频漂移 + 中频撕裂 + 高频纤维毛边）；
* 基本沿切片方向，但局部可蜿蜒；
* 不跟随人物/建筑/道路/天空的轮廓；
* 可以穿过建筑、道路、树、人群和身体；
* 仅避开受保护的主头部。

可选（Semantic Contour）时，边界可以沿着：

* 人体轮廓；
* 人群边缘；
* 建筑结构；
* 天际线；
* 树冠；
* 道路；
* 阴影；
* 大型色块；
* 表现性笔触；

形成语义分割式的模块。语义轮廓不是默认边界家族。

## ✦ Boundary Families

`--boundary` 决定四种可见区域如何切分，默认 `natural`：

| 家族 | 视觉目标 | 说明 |
|---|---|---|
| `natural`（**默认**） | 同一幅照片 + 四个自然区域 | 每区只是抽象方式不同；边界以纸面材质接缝表现；无 z-order/纸片层叠/纸纹；`--layout auto\|horizontal-layered\|side-weighted\|...` |
| `collage`（可选） | 分层撕纸纸片 | 四张构图驱动纸片 + 独立撕纸轮廓 + z-order 单侧纸影 + 纸纹（四张纸片拼贴风格） |
| `torn`（legacy） | 有序撕纸条带 | 四条有序区域 + 三条贯穿画布的波浪撕纸接缝（约 1/4、1/2、3/4） |
| `contour`（可选） | 语义轮廓边界 | 跟随剪影/建筑边缘/屋顶线/天际线/道路/地平线；不是默认 |
| `mask`（自定义） | 完全自由的形状 | 提供 4 张内容感知 mask，脚本归一化为精确平铺 |
| `rect`（回退） | 等分直条 | 纯整数坐标的四条等宽/等高条 |

确定性：`natural`/`collage`/`torn` 都使用 `--seed`（默认 42），相同输入必定输出相同的区域/接缝。

```bash
# 默认 natural（一幅照片，四个自然区域，边界=纸面接缝）
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --boundary natural --layout auto \
    --anchor auto --face-boxes "100,60,180,150" \
    --levels 65,90,30 --workdir work/

# 可选：分层撕纸纸片拼贴
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --boundary collage --layout auto \
    --face-boxes "100,60,180,150" --levels 65,90,30 --workdir work/

# legacy 有序撕纸条带
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --boundary torn --direction vertical \
    --face-boxes "100,60,180,150" --levels 65,90,30 --workdir work/
```

---

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

## ✦ Head Continuity

**只有主头部是硬锁定的**：人脸身份、头部轮廓、发际线与脸—颈连接必须连贯。

身体其余部分不是硬要求——身体部位可以横跨模块、同时存在于不同抽象状态（和建筑一样），跨状态的可读碎片往往比完整连续的身体更有冲击力。

```text
Face
 ↓
Head contour
 ↓
Face-to-neck connection   （硬）
──────────────
Shoulders / Body          （软偏好，可跨状态）
```

模块边界可以穿过人物附近（默认 torn 接缝允许穿过身体），但不能制造：

* 错位抠图；
* 双重轮廓；
* 意外重复的肢体/双脸/鬼影；
* 类似 Photoshop 抠图未对齐的残次效果。
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

## ✦ Ordered Torn-Strip Modules

虽然逻辑层严格维护四等分区域，但最终视觉层默认不是规则四切片，而是四条有序区域的撕纸式接缝。

```text
logical zones
       ↓
multi-scale torn-paper seams
       ↓
four ordered sequential regions
```

核心原则：

> **IRREGULAR EDGE ≠ IRREGULAR TERRITORY**

> **Hidden ownership is mathematical. Visible boundaries are designed.**

> **Torn boundaries are layout-defined seams, not semantic segmentation contours.**

默认禁止把四个区域变成任意形状的 blob、孤岛、封闭口袋、U 形环绕或大幅半岛——不规则属于接缝几何，不属于整体模块拓扑。

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
2. **Primary Head Identity & Continuity**（身体与建筑连续性为软偏好，可跨状态共存）
3. **Reality Anchor Role & Local Source Preservation**
4. **Architectural Identity**
5. **Four-State Readability & Abstraction Assignment & Ordered Strip Topology**
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

同样，默认 torn 家族下：

```text
漂亮的不规则边界
```

不能优先于：

```text
有序的四区域拓扑（IRREGULAR EDGE ≠ IRREGULAR TERRITORY）
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
Use $four-slice-reality-poster to transform my photo into ONE continuous
poster: the same photo divided into four natural regions, each region a
different abstraction (Reality / 30% / 65% / 90%), with the boundary
expressed by a torn-paper seam. Never a 2x2 grid or four full-image
versions.
```

中文：

```text
使用 $four-slice-reality-poster 处理这张照片。

把同一张照片分成四个自然区域，每个区域只是抽象方式不同
（Reality + 30%/65%/90%），区域边界用撕纸纸面接缝表现；
不要做成四张独立纸片拼贴。
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
│   ├── deterministic-layout.md
│   ├── intentional-modular-composition.md
│   └── subjects-validation.md
│
└── scripts/
    ├── slice_and_compose.py
    └── restore_protected_anchor.py
```

| File                                 | Responsibility                 |
| ------------------------------------ | ------------------------------ |
| `SKILL.md`                           | Skill 主入口、视觉目标、完整工作流与决策优先级     |
| `composition-and-anchor.md`          | 四逻辑区、Ordered Strip Topology、Reality Anchor、状态分配 |
| `deterministic-layout.md`            | 确定性切分/合成管线（torn/contour/mask/rect）、CLI 与 verify |
| `abstraction-language.md`            | 抽象方法与 30 / 65 / 90% 等级校准       |
| `cinematic-color-system.md`          | 默认电影配色系统与模块色彩关系                |
| `intentional-modular-composition.md` | 边界家族（Torn-Strip 默认 / Semantic Contour 可选）、视觉节奏 |
| `subjects-validation.md`             | 人物、建筑、硬约束与最终验收                 |
| `slice_and_compose.py`               | 确定性切分、torn 接缝生成、合成与 verify   |
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
ONE PHOTO + FOUR NATURAL REGIONS —
each region differs only by abstraction.
```

```text
The paper material layer is the representation of the boundary —
not four separate paper sheets.
```

```text
LEVEL ≠ MEDIUM —
the three abstract states use three different Primary Abstraction Methods,
all inside the same photograph.
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
