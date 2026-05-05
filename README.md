# ml_as_beginner

ML Engineering portfolio by Spoorthy J.  
Software Engineer → ML Engineer.  
Machines. Motors. Aerospace.

---

## Hence Proved Series
Physics laws proven through Machine Learning — one model at a time.

| # | Law | Model | R² | Status |
|---|---|---|---|---|
| 01 | Newton's 2nd Law — F = ma | Linear Regression | 0.9999 | Live |
| 02 | Friction — Will it move? | Logistic Regression | TBD | Building |
| 03 | Bernoulli's Principle | TBD | TBD | Planned |

---

## Projects

### Predictive Maintenance — AI4I Dataset
Classification model to predict machine failure from sensor data.  
Status — In Progress

### NASA CMAPSS — RUL Prediction
Remaining Useful Life prediction for jet engines.  
Status — Planned

---

## Stack
Python · Scikit-learn · FastAPI · Docker · Pandas · NumPy

---

## API — Hence Proved
Run the F=ma model locally with one command:

```bash
docker pull spoorthy091/fma-api
docker run -p 8000:8000 spoorthy091/fma-api
```

Endpoints:
- `GET /` — health check
- `GET /model` — model info
- `POST /predict` — send mass, acceleration, get force

---

## Author
**Spoorthy J** · [GitHub](https://github.com/Spoorthy2001) · [LinkedIn](https://www.linkedin.com/in/spoorthy-jayanna/)