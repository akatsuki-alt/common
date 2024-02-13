from akatsuki_pp_py import Beatmap as Beatmap_akat, Calculator as Calculator_akat

from common.repos.beatmaps import get_beatmap_file
from common.database.objects import DBScore
from common.api.server_api import Score
from common.logging import get_logger

from dataclasses import dataclass

logger = get_logger("performance")

@dataclass
class SimulatedScore:
    beatmap_id: int
    mode: int
    mods = 0
    n300 = 0
    n100 = 0
    n50 = 0
    nMiss = 0
    nGeki = 0
    nKatu = 0
    max_combo = 0
    acc = 0

class PerformanceSystem:
    
    def __init__(self, name: str):
        self.name = name

    def calculate_db_score(self, score: DBScore, as_fc=False) -> float:
        return 0.0
    
    def calculate_score(self, score: Score, as_fc=False) -> float:
        return 0.0
    
    def simulate(self, score: SimulatedScore) -> float:
        return 0.0
    
class AkatsukiPerformanceSystem(PerformanceSystem):
    
    def __init__(self):
        super().__init__("akatsuki-pp-rs_0.9.6")
    
    def calculate_db_score(self, score: DBScore, as_fc=False) -> float:
        try:
            beatmap = get_beatmap_file(score.beatmap_id)
            if beatmap is None:
                return 0.0
            map = Beatmap_akat(bytes=beatmap)
            calc = Calculator_akat(
                mode = score.mode,
                mods = score.mods,
                n300 = score.count_300,
                n100 = score.count_100,
                n50 = score.count_50,
                n_misses = score.count_miss,
                n_geki = score.count_geki,
                n_katu = score.count_katu,
                acc = score.accuracy,
            )
            if as_fc:
                calc.set_n_misses(0)
                calc.set_n300(score.count_300 + score.count_miss)
            else:
                calc.set_combo(score.max_combo)
            return calc.performance(map).pp
        except:
            logger.error(f"Failed to calculate performance for score {score.id} (BeatmapID: {score.beatmap_id})", exc_info=True)
    
    def calculate_score(self, score: Score, as_fc=False) -> float:
        return self.calculate_db_score(score.to_db(), as_fc=as_fc)

    def simulate(self, score: SimulatedScore) -> float:
        try:
            beatmap = get_beatmap_file(score.beatmap_id)
            if beatmap is None:
                return 0.0
            map = Beatmap_akat(bytes=beatmap)
            calc = Calculator_akat(mode = score.mode)
            for key in score.__dict__.keys():
                match key:
                    case "mods":
                        calc.set_mods(score.mods)
                    case "n300":
                        calc.set_n300(score.n300)
                    case "n100":
                        calc.set_n100(score.n100)
                    case "n50":
                        calc.set_n50(score.n50)
                    case "nMiss":
                        calc.set_n_misses(score.nMiss)
                    case "nGeki":
                        calc.set_n_geki(score.nGeki)
                    case "nKatu":
                        calc.set_n_katu(score.nKatu)
                    case "acc":
                        calc.set_acc(score.acc)
                    case "max_combo":
                        calc.set_combo(score.max_combo)
            return calc.performance(map).pp
        except:
            logger.error(f"Failed to calculate performance for score {score.id} (BeatmapID: {score.beatmap_id})", exc_info=True)
