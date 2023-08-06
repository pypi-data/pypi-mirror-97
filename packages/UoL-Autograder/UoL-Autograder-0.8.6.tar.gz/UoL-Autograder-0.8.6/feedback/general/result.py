class CheckResult:
    precision = 4

    def __init__(self, config, name, score, output, sub_number=None, sub_weight=1):
        config = config if type(config) == dict else config._asdict()
        self.name = name
        self.output = output
        self.tags = config.get("tags", [])
        self.max_score = round(config.get("max_score", 0) * float(sub_weight), self.precision)
        self.score = round(config.get("max_score", 0) * float(sub_weight) * float(score), self.precision)
        base_number = config.get("number", None)
        self.number = f"{base_number}.{sub_number}" if base_number and sub_number else (str(base_number) if base_number else None)
        self.visibility = config.get("visibility", None)

    def to_dict(self):
        return {
            **{
                "score": self.score,
                "max_score": self.max_score,
                "name": self.name,
                "tags": self.tags,
                "output": self.output
            },
            **({"number": self.number} if self.number else {}),
            **({"visibility": self.visibility} if self.visibility else {})
        }