import utils.input_gathering as input
import utils.finance_methods as method
global income,expenses,savings_goals,interest
income=0
expenses=0 
savings_goals=["Fixed deposits","Recurring deposit","Self SIP","EPF-style Saving","Emergency Fund Target"]
interest =0.0

input.InputGathering(income,expenses,savings_goals)


print(income,expenses)