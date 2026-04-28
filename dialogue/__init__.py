# DE stands for 'Dialogue Type'

DE_SAY = "say"
DE_CLOSE = "close"
DE_BG = "bg"
DE_BGM = "bgm"
DE_SOUND = "sound"

class DialogueEvent:
    def __init__(self, event: str, data: list):
        self.event = event
        self.data = data or []

class DialogueParser:
    def parse(text: str):
        evs = []
        lines = text.splitlines()
        for l in lines:
            if l.startswith('$bgm'):
                path = l.split(' ')[1]
                evs.append(DialogueEvent(DE_BGM, [path]))
            elif l.startswith('$bg'):
                path = l.split(' ')[1]
                evs.append(DialogueEvent(DE_BG, [path]))
            elif l.startswith('$sound'):
                path = l.split(' ')[1]
                evs.append(DialogueEvent(DE_SOUND, [path]))
            elif l.startswith('$close'):
                evs.append(DialogueEvent(DE_CLOSE, []))
            else:
                name = l[0:l.index(':')]
                text = l[l.index(':')+1:]
                evs.append(DialogueEvent(DE_SAY, [name.strip(), text.strip()]))
        return evs