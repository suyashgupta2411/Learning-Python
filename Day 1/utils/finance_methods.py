def compute(amount: float, option: int, interest_rate: float) -> float:
    # Standard interest rates can be stored in a dictionary
    rates = {
        1: 0.065,  # Fixed Deposit
        2: 0.06,   # Recurring Deposit
        3: 0.10,   # SIP (self-assumed)
        4: 0.08,   # EPF-style Saving
        5: 0.04    # Emergency Fund (assumed in savings account)
    }

    rate = rates.get(option, 0.0)
    interest = amount * ((1 + rate) ** years - 1)  # Compound interest formula
    return interest
