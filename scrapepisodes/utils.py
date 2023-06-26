from supabase import create_client

supabase_url = "your_url"
supabase_key = "your_api_key"

supabase = create_client(supabase_url, supabase_key)

def select(table_name, column_list=None, condition_dict=None):
    # Select specified columns if column_list is provided, otherwise select all columns
    if column_list:
        select_query = supabase.table(table_name).select(column_list)
    else:
        select_query = supabase.table(table_name).select("*")
    
    # Add conditions to the query if condition_dict is provided
    if condition_dict:
        for key, value in condition_dict.items():
            select_query = select_query.eq(key, value)
    
    # Execute the query and return the data
    response = select_query.execute()
    data = response.data
    return data




def insert(table_name, data_dict, upsert=False):
    # Insert data into the table if upsert=False, otherwise upsert the data
    if not upsert:
        supabase.table(table_name).insert(data_dict).execute()
    else:
        supabase.table(table_name).upsert(data_dict, on_conflict='mal_id').execute()
