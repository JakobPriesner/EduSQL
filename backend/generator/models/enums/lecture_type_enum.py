from enum import Enum


class LectureType(str, Enum):
    Awpf = "AWPF",
    Fwpm = "FWPM",
    Vl = "VL",
    Su = "SU",
    E = "Exercise"
    P = "P"
