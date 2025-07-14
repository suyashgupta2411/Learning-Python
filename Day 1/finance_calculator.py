import utils.input_gathering as input
import utils.finance_methods as method
import globals
globals.income,globals.expenses,globals.savings_goals_selected_option=input.InputGathering(globals.income,globals.expenses,globals.savings_goals,globals.savings_goals_selected_option)
globals.interest=method.compute(globals.income-globals.expenses,globals.savings_goals_selected_option,globals.interest)
print('The interest you will in an year would be ',globals.interest)
print('Total savings at the end of an year would be ',globals.interest+(globals.income-globals.expenses)*12)