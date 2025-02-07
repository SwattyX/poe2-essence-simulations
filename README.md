# PoE2 Essence Conversion Simulation

This repository contains a Python script that simulates the conversion of minor essences into major essences in Path of Exile 2. The simulation takes into account the an estimate of the probabilities of successful conversions, the prices of both minor and major essences, and allows for the specification of protected minor essences that are not converted.

## Description

The script simulates the process of converting sets of three minor essences into major essences.  It models the probabilistic nature of the conversion process and calculates the potential profit or loss based on the market prices of the essences. The simulation considers that some minor essences can be protected and not used for conversion.

## How to Use

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/SwattyX/poe2-essence-simulations.git
    ```

2.  **Navigate to the directory:**

    ```bash
    cd poe2-essence-simulations
    ```

3.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv .venv  # Create the virtual environment
    source .venv/bin/activate  # Activate it (Linux/macOS)
    .venv\Scripts\activate  # Activate it (Windows)
    ```

4.  **Install the requirements:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the script:**

    ```bash
    python poe_essence_simulator.py
    ```

    This will execute the simulation and save the results to a CSV file named `poe2_essence_simulation_results.csv`.

## Configuration

The following parameters can be adjusted within the `poe_essence_simulator.py` script:

*   **`NUM_SESSIONS`**:  The total number of independent simulation runs. This controls how many times the entire conversion process is repeated.  **Update this value to control the scale of the simulation.**  A higher number will provide more statistically robust results but will take longer to run.
*   **`SIMULATIONS_PER_SESSION`**: The number of initial sets of three minor essences each session starts with. This controls the number of conversion attempts within each session. **Update this to control the depth of each individual simulation.**
*   **`price_per_exalted`**: The price of an Exalted Orb in Chaos Orbs. This is used to calculate the initial cost of the minor essences.  **Update this value to reflect current market prices.**
*   **`major_essence_prices`**: A dictionary containing the prices of each major essence type.  **Update these values to reflect current market prices.**
*   **`minor_essence_prices`**: A dictionary containing the prices of each minor essence type. **Update these values to reflect current market prices.**
*   **`initial_essence_type`**: The type of minor essence that the simulation starts with.
*   **`protected_minor_essences`**: A tuple containing the names of the minor essence types that are *not* converted.  This allows you to simulate scenarios where you're accumulating certain minor essences.

**Example Configuration Update:**

```python
NUM_SESSIONS = 500000       # Increased number of sessions
SIMULATIONS_PER_SESSION = 2000    # Increased simulations per session
price_per_exalted = 2.50      # Updated Exalted Orb price
major_essence_prices = {  # Updated major essence prices
    "Body": 2.8, "Mind": 28, "Enhancement": 14, "Infinite": 90, 
    "Flames": 3.6, "Ice": 5.8, "Electricity": 60, "Torment": 62, 
    "Battle": 9, "Sorcery": 65, "Ruin": 6.5, "Haste": 200
}
# ... other configurations
