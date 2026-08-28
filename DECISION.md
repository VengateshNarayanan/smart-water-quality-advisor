# Decision Log

## Data Cleaning and Feature Engineering

The Johnstone River real-time water-quality dataset was cleaned by converting timestamps into a consistent datetime format, removing duplicate records, converting sensor measurements to numeric values, identifying invalid negative readings, and handling missing telemetry through interpolation where appropriate. Temporal and statistical features were engineered to capture recent water-quality behaviour and time-series trends. Turbidity was selected as the primary forecasting target because it provides a practical indicator of changing water conditions.

## Model Architecture and Validation

A Random Forest regression model was selected because it can capture nonlinear relationships between engineered sensor features while requiring relatively limited preprocessing. Time-series-aware validation was used to avoid training on future observations when evaluating historical predictions.

## LLM Orchestration and Safety

The LLM receives verified model predictions, current measurements, calculated risk levels, and deterministic safety assessments. The prompt explicitly instructs the model not to invent measurements, thresholds, or risk levels and to distinguish observations from predictions. The deterministic ML and safety layers remain authoritative; the LLM is used only to convert verified information into understandable recommendations. If the LLM API is unavailable or exceeds its quota, the core assessment remains operational.
