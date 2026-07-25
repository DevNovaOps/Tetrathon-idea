import datetime

class HistoryService:
    @staticmethod
    def get_available_months(user=None):
        # Generate the last 12 months up to the current month deterministically
        months = []
        today = datetime.date.today()
        
        # Determine how far back to go. If user has a join date, we could use that,
        # but to ensure a good UX we'll always show at least the last 12 months.
        
        for i in range(12):
            m = today.month - i
            y = today.year
            while m <= 0:
                m += 12
                y -= 1
            
            val_str = f"{y}-{m:02d}"
            label_str = datetime.date(y, m, 1).strftime("%B %Y")
            
            months.append({
                "value": val_str,
                "label": label_str
            })
            
        return months


