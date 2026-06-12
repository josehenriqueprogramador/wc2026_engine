from fastapi import FastAPI
from src.simulate import simulate
from src.data_loader import load_matches
from src.model import MatchModel
from src.report import generate
import src.names as names

app = FastAPI(
    title="WC2026 Prediction Engine",
    version="1.0"
)

@app.get("/")
def root():
    return {
        "service": "World Cup 2026 Prediction Engine",
        "status": "running"
    }

@app.get("/simulate")
def run_simulation():

    df = load_matches()

    model = MatchModel()

    model.fit(df)

    tables = model.build_tables(names.TEAMS)

    result = simulate(tables)

    return {
        "message": "simulation complete",
        "champion_probabilities": result["champion"].tolist()
    }

@app.get("/report")
def build_report():

    df = load_matches()

    model = MatchModel()

    model.fit(df)

    tables = model.build_tables(names.TEAMS)

    result = simulate(tables)

    generate(tables, result)

    return {
        "message": "report generated in outputs/"
    }

@app.get("/health")
def health():
    return {"status": "ok"}
