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
    def get_level_threshold(level):
        # Level thresholds from the context
        thresholds = {
            1: 0,
            2: 100,
            3: 250,
            4: 500,
            5: 800,
            6: 1200,
            7: 1700,
            8: 2300,
            9: 3000,
            10: 4000
        }
        if level in thresholds:
            return thresholds[level]
        # For levels > 10, use a simple formula (example)
        return 4000 + (level - 10) * 1500

    @staticmethod
    def check_level_up(current_xp, current_level):
        next_level = current_level + 1
        threshold = XPService.get_level_threshold(next_level)
        if current_xp >= threshold:
            return True, next_level
        return False, current_level
