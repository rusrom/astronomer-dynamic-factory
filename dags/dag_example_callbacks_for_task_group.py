def callback_for_tg_say_hello(context):
    print("+++++++++++++ tg +++++++++++++++ hello from callback for task_group")
    print(context)
    print("+++++++++++++ tg +++++++++++++++ end of callback for task_group")


def defaut_callback_for_all_tasks(context):
    print("************* task ************** hello from default callback for all tasks")
    print(context)
    print("************* task ************** end of default callback for all tasks")
