from .compound_engine import CompoundEngine

class ChartDataEngine:
    """
    Generates datasets for the frontend Chart.js line chart.
    """
    @staticmethod
    def generate_datasets(monthly_sip: int, years: int, scenarios: list) -> dict:
        labels = [f"Year {y}" for y in range(0, years + 1)]
        datasets = []
        
        # Determine max value for Y-axis scaling if needed (handled by Chart.js though)
        for scen in scenarios:
            data_points = []
            for y in range(0, years + 1):
                fv = CompoundEngine.calculate_future_value(monthly_sip, y, scen["cagr"])
                data_points.append(fv)
            
            datasets.append({
                "label": f"{scen['name'].split(' ')[0]} ({scen['cagr']}%)",
                "data": data_points,
                "id": scen["id"]
            })
            
        return {
            "labels": labels,
            "datasets": datasets
        }
