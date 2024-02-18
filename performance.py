from titanic_pp_py import Beatmap as Beatmap_titanic, Calculator as Calculator_titanic
from akatsuki_pp_py import Beatmap as Beatmap_akat, Calculator as Calculator_akat
from rosu_pp_py import Beatmap as Beatmap_rosu, Calculator as Calculator_rosu

from common.repos.beatmaps import get_beatmap_file
from common.database.objects import DBScore
from common.api.server_api import Score
from common.logging import get_logger

from dataclasses import dataclass
from typing import Dict, Type

logger = get_logger("performance")

@dataclass
class SimulatedScore:
    beatmap_id: int
    mode: int
    mods: int = 0
    n300: int = 0
    n100: int = 0
    n50: int = 0
    nMiss: int = 0
    nGeki: int = 0
    nKatu: int = 0
    max_combo: int = 0
    acc: float = 0
    passed_objects: int = 0

class PerformanceSystem:
    
    def __init__(self, name: str):
        self.name = name

    def calculate_db_score(self, score: DBScore, as_fc=False) -> float:
        return 0.0
    
    def calculate_score(self, score: Score, as_fc=False) -> float:
        return 0.0
    
    def simulate(self, score: SimulatedScore) -> float:
        return 0.0


class RosuForkPerformanceSystem(PerformanceSystem):
    
    def __init__(self, name: str, beatmap_class: Type, calculator_class: Type):
        self.beatmap_class = beatmap_class
        self.calculator_class = calculator_class
        super().__init__(name)
    
    def calculate_db_score(self, score: DBScore, as_fc=False) -> float:
        try:
            beatmap = get_beatmap_file(score.beatmap_id)
            if beatmap is None:
                logger.warn(f"Can't recalculate {score.id}! (BeatmapID: {score.beatmap_id} not found)")
                return 0.0
            if score.beatmap_md5 != beatmap[1]:
                logger.warn(f"Can't recalculate {score.id}! (BeatmapMD5: {score.beatmap_md5} != {beatmap[1]})")
                return 0.0
            map = self.beatmap_class(bytes=beatmap[0])
            calc = self.calculator_class(
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
                logger.warn(f"Can't recalculate {score.id}! (BeatmapID: {score.beatmap_id} not found)")
                return 0.0
            map = self.beatmap_class(bytes=beatmap[0])
            calc = self.calculator_class(mode = score.mode)
            for key in score.__dict__.keys():
                match key:
                    case "mods":
                        if score.mods:
                            calc.set_mods(score.mods)
                    case "n300":
                        if score.n300:
                            calc.set_n300(score.n300)
                    case "n100":
                        if score.n100:
                            calc.set_n100(score.n100)
                    case "n50":
                        if score.n50:
                            calc.set_n50(score.n50)
                    case "nMiss":
                        if score.nMiss:
                            calc.set_n_misses(score.nMiss)
                    case "nGeki":
                        if score.nGeki:
                            calc.set_n_geki(score.nGeki)
                    case "nKatu":
                        if score.nKatu:
                            calc.set_n_katu(score.nKatu)
                    case "acc":
                        if score.acc:
                            calc.set_acc(score.acc)
                    case "max_combo":
                        if score.max_combo:
                            calc.set_combo(score.max_combo)
                    case "passed_objects":
                        if score.passed_objects:
                            calc.set_passed_objects(score.passed_objects)
            return calc.performance(map).pp
        except:
            logger.error(f"Failed to calculate performance for score {score.id} (BeatmapID: {score.beatmap_id})", exc_info=True)


performance_systems: Dict[str, PerformanceSystem] = {
    'akatsuki': RosuForkPerformanceSystem('akatsuki-pp-rs_0.9.6', Beatmap_akat, Calculator_akat),
    'bancho':   RosuForkPerformanceSystem('rosu-pp-rs_0.10.0', Beatmap_rosu, Calculator_rosu),
    'titanic':  RosuForkPerformanceSystem('titanic-pp-rs_0.0.5', Beatmap_titanic, Calculator_titanic),
}

def by_version(version: str) -> PerformanceSystem | None:
    for system in performance_systems.values():
        if system.name == version:
            return system
    return None