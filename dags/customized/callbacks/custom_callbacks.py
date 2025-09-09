def dag_level_output_message(context, param1, param2):
    print("-------------- DAG LEVEL CALLBACK WAD TRIGGERED ------------------")
    print("A clustomized callback has been raised!")
    print(f"{param1} ---------- {param2}")
    print("context:", context)
    print("End of callback")
    print("------------------------------------------------------------------")
    with open("result_dag_level_callback.txt", "w") as f:
        f.write(f"DAG level callback was triggered with params: {param1}, {param2}\n")
        f.write(f"and context: {context}\n")
