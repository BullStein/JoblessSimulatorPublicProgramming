from libs import *


new_data = get_data()
new_data["account"]["is_logged"] = True
save_data(new_data)