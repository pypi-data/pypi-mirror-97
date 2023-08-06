# playscript

[> English version](https://github.com/satamame/playscript/blob/master/README_en.md)

## 概要

台本を構造化データとして扱うためのパッケージです。

## クラス

### PSc

台本データのクラスです。

### PScLine

PSc オブジェクトに含まれる各行を表すクラスです。  
"type" 属性により、セリフやト書きといった「行の種類」が決まります。

### PScLineType

PScLine の "type" を定義する enum 型です。

## 例

### 3行からなる台本を作る

```python
from playscript import PScLineType, PScLine, PSc

title = PScLine.from_text(PScLineType.TITLE, 'ろくでなしの冒険')
dialogue1 = PScLine.from_text(PScLineType.DIALOGUE, '六郎「どうする？」')
dialogue2 = PScLine.from_text(PScLineType.DIALOGUE, '七郎「帰って寝る」')

script = PSc(lines=[title, dialogue1, dialogue2])
```
