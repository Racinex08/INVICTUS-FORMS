with open('c:\\Users\\Isaac Racines\\Downloads\\Invictus Form\\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<button id="historyBtn" class="history-btn">📋</button>\\n        ', '')
text = text.replace('<button id="historyBtn" class="history-btn">📋</button>\\n    ', '')
text = text.replace('<button id="historyBtn" class="history-btn">📋</button>\\n', '')
text = text.replace('<button id="historyBtn" class="history-btn">📋</button>', '')

with open('c:\\Users\\Isaac Racines\\Downloads\\Invictus Form\\index.html', 'w', encoding='utf-8') as f:
    f.write(text)
