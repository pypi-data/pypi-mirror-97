from subsparser.subtitle import Subtitle
from subsparser.constants import Extensions
from subconverter.utils import fr_to_ms

class WebVTT:
    HEADER = "WEBVTT\n\n"
    EXT = Extensions.WEBVTT
    TIMELINE_FORMAT = "{start} --> {end}"
    TIMESTAMP_FORMAT = "{:02d}:{:02d}:{:02d}.{:03d}"

    def __init__(self, data, encoding="utf-8", frame_rate=24.00):
        self.data = data
        self.frame_rate = frame_rate
        self.encoding = encoding


    def to_webvtt_timestamp(self, timestamp, frame_rate):
        h, m, s, ms, fr = timestamp.values()
        ms = fr_to_ms(fr, frame_rate) if fr else ms
        return WebVTT.TIMESTAMP_FORMAT.format(h, m, s, ms)

    def to_webvtt(self):
        content = "{}".format(WebVTT.HEADER)
        index = 1
        for ins in self.data:
            start, end, text = ins.start, ins.end, "".join(ins.text).strip()
            if not text:
                continue
            content += "{index}\n{timeline}\n{text}\n\n".format(
                index=index,
                timeline=WebVTT.TIMELINE_FORMAT.format(
                    start=self.to_webvtt_timestamp(start, self.frame_rate),
                    end=self.to_webvtt_timestamp(end, self.frame_rate)
                ),
                text=text
            )
            index += 1
        return content

    def write(self, path):
        ext = Extensions.get(path)
        fpath = path.replace(ext, self.EXT.value)
        with open(file=fpath, mode="w+", encoding=self.encoding) as f:
            f.write(self.to_webvtt())
        return fpath

    @staticmethod
    def from_file(path, encoding='utf-8', language_code=None, frame_rate=24.00):
        subtitle = Subtitle(path=path, encoding=encoding, language_code=language_code)
        subtitle.detect_encoding().read().parse()
        webvtt = WebVTT(
            data=subtitle.data, encoding=encoding, frame_rate=frame_rate
        )
        return webvtt.write(path)

