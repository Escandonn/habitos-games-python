class XPService:
    PRIORITY_XP = {
        "Baja": 5,
        "Media": 10,
        "Alta": 20
    }

    INTENSITY_MULT = {
        "Baja": 1,
        "Media": 2,
        "Alta": 3
    }

    @staticmethod
    def calculate_xp(priority, intensity):
        base_xp = XPService.PRIORITY_XP.get(priority, 5)
        mult = XPService.INTENSITY_MULT.get(intensity, 1)
        return base_xp * mult

    @staticmethod
    def calculate_gold(xp_gained, streak=0):
        # 1 Gold per 2 XP roughly
        base_gold = max(1, xp_gained // 2)
        # Bonus por racha activa
        if streak >= 30: bonus = 50
        elif streak >= 7: bonus = 20
        elif streak >= 3: bonus = 5
        else: bonus = 0
        return base_gold + bonus

    @staticmethod
    def get_level_threshold(level):
        # Global user level thresholds
        thresholds = {1: 0, 2: 100, 3: 250, 4: 500, 5: 800, 6: 1200, 7: 1700, 8: 2300, 9: 3000, 10: 4000}
        return thresholds.get(level, 4000 + (level - 10) * 1500)

    @staticmethod
    def get_habit_level_threshold(level):
        # Individual habit level thresholds (smaller steps)
        thresholds = {1: 0, 2: 50, 3: 150, 4: 300, 5: 500}
        return thresholds.get(level, 500 + (level - 5) * 300)

    @staticmethod
    def check_level_up(current_xp, current_level, is_habit=False):
        next_level = current_level + 1
        threshold = XPService.get_habit_level_threshold(next_level) if is_habit else XPService.get_level_threshold(next_level)
        if current_xp >= threshold:
            return True, next_level
        return False, current_level
