import streamlit as st
from leader_board import leader_board
from matchup import matchup
from player_comp import player_comp
from player_search import player_search
from venue_stats import venue_search
import pandas as pd

# file_path = r"C:\Users\adith\Documents\Projects\python-projects\cric_metric_clone\json_csv\csv_files\t20_matches_new_format.csv"  # replace with your file path
# if st.button('Rerun'): st.experimental_rerun()
file_path='https://csvfiles-cricmetric-clone.s3.ap-south-1.amazonaws.com/t20_matches_with_types.csv?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRzBFAiAaVNPJO9i5Tvql0uZHK%2Fd4qyGO4L2UJHP7EWjlgJxlKAIhAPUXcdhdtjWX0Gx5GNAibynlZCPvKecGjkSlsusMYd10Ku0CCO%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMODk3NzI2MDkxOTY1Igwfh3HPtlFNtVH6YZAqwQIyRKGWjACLiWKHgwOENPFj0iyns0FLDym6c0EexiweKpuSfS26MZBJEeyAsgw5cGCJ0YeB0rR4NuBMM6ydy4SElCw4Tg7bm%2Bsk82GGPLWaLy61C3lPir8k%2B1v6zKVFfu66BeAYMkKO4xvq8KLZ89g8%2F1M8oM0%2Fj7MwGgZfU0g%2F%2B%2F0ld1L8rwf2XUlZ2%2FVdGSZMHcZZh7Wh88hAucuamqTOuF5bKLpVaFTfzRc3SNHpr0UdN7VEUbJwlZjdKcpDQP2WOa8u4XJjcCF4GAQh6ajA2Z9XNkYI686o%2BNtcm9pOSDE4ICpGT7haxZli%2BH7yws5MfkriXHws4%2FIx7rlEKeau76YA%2F%2BmdDrjVklU1E3%2FiwJQZtNpXsbMb2KkAU3gKdRMfyuiLa50QlxWjG0BWOPVjlTdHMIiFPNkl%2BEwQAMSPBUcw0cexrwY6swKtLqTmsBzPLeRSkNMh9Pq7Ldlm5UCDUOI9LiHFoFgRWuArNqeUf1%2F3e8eA7%2Bc1RVFIp0x%2FXlMMIE%2BqlnqshQusqr8%2FRd9x9dNGCycZzIGNnEmi2AHzV8Lax5gKiuGnjoRWrT9qdGKM4EJPGmXheTQNgI0l4I%2BkdR4N8bEKXCdwx40sAlZmynDswdnVRXdgPYTB4anYvqy7ur1rISSq1QSE8b9WBB0zUtThMQ77DcLyPQSuy76dUyTsVLWeF3BXYWMh2QCgYtK5cTKAp3nbfDI2iEePVRUaNpPQ8ZNeE7prg0E3Tff9R9jvHDI8bmBstFJfxVer6ty0uuKrZyzvapw6EP7DXAxuhGWQ8JTCudAl%2FlcvhI%2F2iJtnMD%2FcMabBczcELqe0XGe64jzgcVnoS8DBctLN&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240309T134650Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA5CBFFCK6QT2EHMX7%2F20240309%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=559e7457c87ef6d7fc42656201649640de2a875347975da4b04052b372e87928'
# Load the dataframe
df = pd.read_csv(file_path) 


# Create a sidebar for navigation
option = st.selectbox(
    'Select an option',
    ['Leader Board', 'Matchup', 'Player Comparison', 'Player Search','Venue Search']
)

# Call the appropriate function based on the user's selection
if option == 'Leader Board':
    leader_board(df)
elif option == 'Matchup':
    matchup(df)
elif option == 'Player Comparison':
    player_comp(df)
elif option == 'Player Search':
    player_search(df)
elif option == 'Venue Search':
    venue_search(df)
