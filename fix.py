import re
with open('core/battle_log.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = re.sub(r'(    def __init__\(self\):\n        self\.events = \[\]\n\n    # запись в лог)', r'\1\n    def phase_start(self, turn, phase):\n        self.add(f"[Turn {turn}] Phase start: {phase}")\n', content)
with open('core/battle_log.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')