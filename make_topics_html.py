# -*- coding: utf-8 -*-
"""Build 史記_topics.html from 史記_topics.txt."""
import html
import re

LABELS = {
    0: ("Direct Speech & Dialogue", "Dominated by quotation marks plus dialogue particles like 何, 吾, 矣, and honorifics 君/臣. This topic captures passages of quoted speech — advisers, ministers and rulers debating in the 史記's signature dramatic dialogues."),
    1: ("Statecraft & Service", "Generic action and social-order characters (行, 得, 臣, 主, 家, 世) describing conduct, duty and the service of ministers to rulers. It clusters around reflective chapters on officials, loyalty and the fate of families in the state."),
    2: ("Military Campaigns", "军, 将, 兵, 骑, 击, 破, 斩, 攻 — the vocabulary of warfare. This topic concentrates on battle narratives, especially the campaigns of generals like Li Guang (广) and the awarding of fiefs after victory."),
    3: ("Imperial Court & Succession", "王, 太, 帝, 后, 丞相, 孝, 皇 — titles of the imperial household. It marks passages on emperors, empresses, heir apparents (太子) and chancellors, i.e. court politics of the Qin and early Han."),
    4: ("Chu–Han Contention", "汉, 项(羽), 楚, 沛, 陈(涉), 信(韩信) — the proper names of the civil war between Liu Bang and Xiang Yu. This topic maps the rise of the Han founder from 沛 and the struggle with Chu."),
    5: ("Chronology & Numbers", "十, 年, 二, 三, 馀, 百 — almost purely numerals with 年 (year) and 元/始 (era beginnings). It corresponds to annalistic dating formulas, especially the 「十二年」-style regnal counts of the chronological tables and basic annals."),
    6: ("Rhetoric & Biographical Style", "兮 (the Chu-ci particle), 传, 列, 孟, 贾, 原 (屈原), 睢 — characters from the biographies of poets and rhetoricians. This topic gathers the literary chapters, including Qu Yuan's verse and the collected biographies (列传)."),
    7: ("Ritual, Music & Moral Order", "礼, 乐, 德, 道, 民, 天, 周公 — the language of Confucian political philosophy. It captures the treatises and chapters on rites, music and benevolent governance, from the Zhou ideal down to Han ceremony."),
    8: ("Xiongnu & Western Regions", "匈奴, 单(于), 汉, 万, 千, 西, 南, 东 — diplomacy and war on the frontiers. This topic covers the Xiongnu account, embassies (使) and the geography of the steppe and Western Regions."),
    9: ("Sacrifices & the Sacred", "祠, 神, 封(禅), 泰(山), 帝, 山, 海 — worship, sacrifices and sacred geography. It represents the chapters on the Feng and Shan sacrifices at Mount Tai, immmortals (方士) and the state cult."),
    10: ("Medicine & Physicians", "病, 脉, 气, 阴, 阳, 治, 方 — the technical vocabulary of diagnosis and therapy. This is the biography of the physicians Canggong and Bian Que, with pulse-reading cases (診籍) in dialogue form."),
    11: ("Confucius & His Disciples", "孔(子), 仲(尼), 子, 公, 齐, 鲁, 卫 — the master, his disciples (氏, 孙, 叔, 季) and his home states. This topic is the Confucius biography and the 仲尼弟子列传, tracing his travels among Qi, Lu and Wei."),
    12: ("Spring & Autumn States", "晋, 周, 吴, 郑, 楚, 伯, 立, 卒, 伐 — the hereditary houses of the Eastern Zhou. It maps the 世家 chapters: successions (立), deaths (卒) and wars (伐) of the feudal lords of the Spring and Autumn period."),
    13: ("Warring States Diplomacy", "秦, 赵, 魏, 齐, 韩, 燕, 攻, 地 — the seven powers contending for land. This topic captures the stratagems, alliances (与) and territorial bargains of the Warring States narrated in the biographies of the strategists."),
    14: ("Celestial Omens & Calendrics", "星, 月, 日, 太(白), 行, 居 — the motion of planets and heavenly bodies. This is the 天官书 (Treatise on Celestial Offices): planetary positions, omens and their correlation with affairs of state."),
}

def parse(path):
    topics, cur = [], None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        m = re.match(r"^Topic (\d+):$", line)
        if m:
            cur = {"id": int(m.group(1)), "words": [], "docs": []}
            topics.append(cur)
            continue
        if cur is None:
            continue
        s = line.strip()
        m = re.match(r"segment (\d+)\t([\d.]+)$", s)
        if m:
            cur["docs"].append((int(m.group(1)), float(m.group(2))))
        elif "\t" in s:
            w, p = s.split("\t")
            cur["words"].append((w, float(p)))
    return topics

topics = parse("史記_topics.txt")

CSS = """
:root{--ink:#2b2620;--paper:#f7f3ea;--accent:#8c2f2f;--gold:#b8860b;--muted:#7a7265;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Source Han Serif SC","Noto Serif CJK SC","Songti SC",serif;
     background:var(--paper);color:var(--ink);line-height:1.6;padding:2rem 1rem}
.wrap{max-width:860px;margin:0 auto}
header{text-align:center;margin-bottom:2.5rem;border-bottom:3px double var(--accent);padding-bottom:1.5rem}
header h1{font-size:2rem;letter-spacing:.3em;color:var(--accent)}
header .sub{color:var(--muted);margin-top:.5rem;font-size:.95rem}
.meta{display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;justify-content:center;margin-top:1rem;
      font-size:.85rem;color:var(--muted)}
.topic{background:#fffdf8;border:1px solid #e4dcc9;border-left:5px solid var(--accent);
       border-radius:6px;padding:1.25rem 1.5rem;margin-bottom:1.5rem;
       box-shadow:0 1px 4px rgba(0,0,0,.06)}
.topic h2{font-size:1.15rem;display:flex;align-items:baseline;gap:.75rem;flex-wrap:wrap}
.tnum{color:var(--accent);font-size:.9rem;letter-spacing:.1em}
.label{font-weight:700}
.explain{color:#5c554a;margin:.6rem 0 1rem;font-size:.93rem}
.words{display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:1rem}
.word{background:#f1ead9;border:1px solid #ddd2b8;border-radius:4px;padding:.15rem .5rem;
      font-size:1.05rem}
.word b{color:var(--accent)}
.word .p{color:var(--muted);font-size:.75rem;margin-left:.3rem}
.docs{font-size:.88rem;color:var(--muted);border-top:1px dashed #d8cfba;padding-top:.7rem}
.docs span{margin-right:1.2rem;white-space:nowrap}
.docs b{color:var(--gold)}
footer{text-align:center;color:var(--muted);font-size:.8rem;margin-top:2rem}
"""

parts = ["""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8">
<title>史記 · LDA Topics</title>
<style>%s</style></head>
<body><div class="wrap">
<header>
  <h1>史記 · 主題模型</h1>
  <div class="sub">Character-level LDA topic model of the Records of the Grand Historian</div>
  <div class="meta">
    <span>Corpus: 史記.txt</span><span>433 segments × 1000 chars</span>
    <span>15 topics</span><span>100 Gibbs iterations</span><span>random_state = 42</span>
    <span>stopwords: qhchina zh_cl_tr</span>
  </div>
</header>""" % CSS]

for t in topics:
    tid = t["id"]
    label, explain = LABELS[tid]
    words = "".join(
        f'<span class="word"><b>{html.escape(w)}</b>'
        f'<span class="p">{p:.4f}</span></span>'
        for w, p in t["words"])
    docs = "".join(
        f'<span>segment <b>{d}</b> ({p:.3f})</span>'
        for d, p in t["docs"])
    parts.append(f"""
<section class="topic">
  <h2><span class="tnum">TOPIC {tid:02d}</span><span class="label">{html.escape(label)}</span></h2>
  <p class="explain">{html.escape(explain)}</p>
  <div class="words">{words}</div>
  <div class="docs"><b>Strongest segments:</b> {docs}</div>
</section>""")

parts.append("""
<footer>Generated from 史記_topics.txt — LDAGibbsSampler (qhchina)</footer>
</div></body></html>""")

with open("史記_topics.html", "w", encoding="utf-8") as f:
    f.write("".join(parts))
print("wrote 史記_topics.html")
