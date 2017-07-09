import pandas as pd

url = "http://fcpa.stanford.edu/enforcement-actions.html"
enforcements_df, = pd.read_html(url, header=0)

#print(enforcements_df)
#enforcements_df.to_csv("enforcements.csv", index=False, header=True)
enforcements_df.to_json("enforcement.json")


#import pandas as pd

#calls_df, = pd.read_html("http://apps.sandiego.gov/sdfiredispatch/", header=0, parse_dates=["Call Date"])

#calls_df.to_csv("calls.csv", index=False)
