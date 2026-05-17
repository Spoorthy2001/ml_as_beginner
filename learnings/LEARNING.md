## Model - Torque
### API Failure — Sampling Bias in Production

**Input sent:**
r_m = 10.0m, F_N = 20.0N, theta_deg = 280°

**Expected output:** -196.96 Nm
**Actual output:** 2189.63 Nm

**Root cause:** Sampling bias.
Training data range → r: 0.1 to 1.0m
Input sent → r = 10.0m → 10x outside training range
Model has never seen r = 10m → prediction is garbage

**The lesson:**
A model is only reliable within the range it was trained on.
Outside that range → extrapolation → unpredictable results.

**Real world consequence:**
In aerospace or automotive — this kind of failure
is catastrophic. A model predicting 2189 Nm
when true torque is -196 Nm could cause
a maintenance engineer to make a fatal decision.

**Fix options:**
1. Add input validation in API → reject inputs outside training range
2. Retrain with wider data range
3. Add warning in response when input approaches boundary

**Status:** Known limitation. Documented. Fix in next iteration.

## Model - Energy Efficiency Classification
### Data Failure — Weak Feature - Target relationship

**Input sent:**
Dataset from kaggle

**Expected output:** High accuracy
**Actual output:** in a range of 33 - 38 %

**Root cause:** Flat Features
Equal feature importance = no dominant signal
Models learn noise when signal is absent
More powerful algorithms can't fix absent signal

**The lesson:**
The answer is better data, not better algorithms

**Real world consequence:**
**Real world consequence:**
In aerospace or automotive — deploying a model with 
35% accuracy on a safety-critical system is dangerous.
A predictive maintenance model that's barely better 
than random could miss real failures or flag false alarms
constantly. Engineers lose trust in the system entirely.
Data quality review must happen before model deployment.

**Fix options:**
1. Collect right data

**Status:** Known limitation. Documented.
