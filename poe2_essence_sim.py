import random
import pandas as pd
import multiprocessing
# from functools import partial

def simulate_essences_conversion(
    num_simulations=1000,
    price_per_exalted=2.23,
    conversion_prob=0.02249178,
    initial_essence_type="Torment",
    protected_minor_essences=("Haste", "Electricity")
):
    """
    Simulates the conversion of minor essences into major essences in Path of Exile.

    Args:
        num_simulations (int): The number of initial sets of 3 minor essences to simulate.
        price_per_exalted (float): The price of an Exalted Orb in Chaos Orbs.
        conversion_prob (float): The probability of a successful conversion from minor to major essence.
        initial_essence_type (str): The starting type of minor essence.
        protected_minor_essences (tuple, optional): Tuple of minor essence types that are not converted.
                                               Defaults to ("Haste", "Electricity").

    Returns:
        dict: A dictionary containing the results of the simulation, including:
            - initial_exalted_costs: The cost of the initial minor essences in Exalted Orbs.
            - initial_minor_essences: The initial number of minor essences.
            - final_simulations: The total number of conversion attempts.
            - remaining_minor_essences: A dictionary of the remaining minor essences and their counts.
            - major_essences: A dictionary of the obtained major essences and their counts.
            - major_essence_value: Total value of major essences obtained.
            - minor_essence_value: Total value of protected minor essences.
            - total_values: Total value of major and minor essences.
            - profits: The profit from the conversions (total value - initial cost).
    """


    major_essence_prices = {  # Prices for major essences
        "Body": 2.7, "Mind": 26, "Enhancement": 13.5, "Infinite": 86, 
        "Flames": 3.5, "Ice": 5.6, "Electricity": 55, "Torment": 58, 
        "Battle": 8.5, "Sorcery": 60, "Ruin": 6, "Haste": 186
    }

    minor_essence_prices = { # Prices for protected minor essences
        "Electricity": 5, "Haste": 1.5, "Body": 0.5, 
        "Mind": 0.5,  "Enhancement": 13.5, "Infinite": 0.5,  
        "Flames": 0.5,  "Ice": 0.5,  "Torment": 0.5,  
        "Battle": 0.5,  "Sorcery": 0.5,  "Ruin": 0.5, 
    }

    essence_types = list(major_essence_prices.keys())
    minor_essences = {key: 0 for key in major_essence_prices.keys()} # Initialize counts for all minor essence types
    minor_essences[initial_essence_type] = num_simulations * 3 # Start with 3 minor essences per simulation

    major_essences_obtained = []
    total_conversions = 0
    initial_cost = (num_simulations * 3) / price_per_exalted

    greater_essence_weights = [7, 13, 10, 10, 8, 8, 6, 4, 6, 5, 8, 4] # Weights for major essence drop probabilities

    # Weights for failed conversion outcomes, based on observed probabilities.
    failed_weights = [
        3466/3868/10 if et not in ["Electricity", "Haste"] else 
        291/3868 if et == "Electricity" else 
        111/3868 
        for et in essence_types
    ]

    while True:
        convertible_types = [
            etype for etype, count in minor_essences.items() 
            if count >= 3 and etype not in protected_minor_essences
        ]
        
        if not convertible_types:
            break

        essence_type = initial_essence_type if initial_essence_type in convertible_types else random.choice(convertible_types)
        minor_essences[essence_type] -= 3
        total_conversions += 1

        if random.random() < conversion_prob:
            greater_essence = random.choices(essence_types, weights=greater_essence_weights, k=1)[0]
            major_essences_obtained.append(greater_essence)
        else:
            failed_type = random.choices(essence_types, weights=failed_weights, k=1)[0]
            minor_essences[failed_type] += 1

    total_value = sum(major_essence_prices[essence] for essence in major_essences_obtained)
    
    protected_value = sum(
        count * minor_essence_prices[etype] 
        for etype, count in minor_essences.items() 
        if etype in protected_minor_essences
    )

    profit = (total_value + protected_value) - initial_cost

    major_essences = {}

    for essence in major_essences_obtained:
        major_essences[essence] = major_essences.get(essence, 0) + 1

    return {
        "initial_exalted_costs": initial_cost,
        "initial_minor_essences": num_simulations * 3,
        "final_simulations": total_conversions,
        "remaining_minor_essences": minor_essences,
        "major_essences": major_essences,
        "major_essence_value" : total_value,
        "minor_essence_value" : protected_value,
        "total_values": total_value + protected_value,
        "profits": profit
    }


def run_simulations(num_sessions, num_simulations_per_session):
    """Runs multiple simulations in parallel using multiprocessing."""
    with multiprocessing.Pool() as pool:
        args = [num_simulations_per_session] * num_sessions
        results = pool.map(simulate_essences_conversion, args)
    return pd.DataFrame(results)

if __name__ == "__main__":
    NUM_SESSIONS = 100000  # Total number of independent sessions
    SIMULATIONS_PER_SESSION = 1000  # Starting reforges per session
    
    simulation_df = run_simulations(NUM_SESSIONS, SIMULATIONS_PER_SESSION)
    simulation_df.to_csv("poe2_essence_simulation_results.csv", index=False)