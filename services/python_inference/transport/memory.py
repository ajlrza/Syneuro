import json, random, asyncio
from watchfiles import watch, Change


memory_holder = []
neurons = None

int_to_string_map_single = {
    1: "one", 
    2: "two", 
    3: "three", 
    4: "four", 
    5: "five", 
    6: "six", 
    7: "seven", 
    8: "eight", 
    9: "nine"
}

int_to_string_map_single_edge = {
    11: "eleven", 
    12: "twelve", 
    13: "thirteen"
}

int_to_string_map_double = {
    10: "ten", 
    20: "twenty", 
    30: "thirty", 
    40: "forty", 
    50: "fifty", 
    60: "sixty", 
    70: "seventy", 
    80: "eighty", 
    90: "ninety", 
    100: "one hundred"
}

int_to_string_map_scale = {
    1: "ones", 
    2: "tens", 
    3: "hundred", 
    4: "thousand", 
    5: "ten thousands", 
    6: "hundred thousand", 
    7: "million", 
    8: "ten million", 
    9: "hundred million", 
    10: "billion"
}

async def continue_memory_transport(memory_iter) -> bool:

    neuron_activated = False

    while (neuron_activated != True):
                
        if (neuron_status[random_available_neuron] == "Active"):
            continue

        else:
            neuron_int_to_string = None # add function here
            
            neurons["neuron_status"]["random_available_neuron"] = "Active"
            neurons["neuron_status"]["neuron_int_to_string"] = memory # Assuming thisalso has the same format in json so they just be overwritten smoothly

            neuron_activated = True

    return True
    

async def memory_filter(change: Change, path: str) -> bool:

    if (change.modified):
        print("Neuron modified.")

    if (change.modified > 5):
        print("Neuron potentially freed up or used.")

    return True

if (len(memory_holder) == 100):

    print(f"Loaded {len(neurons['neuron_status'])} neurons. Starting allocation...\n")
    
    try:
        with open('synaptic_neurons.json', 'r', encoding='utf-8') as file:
            
            neurons = json.load(file)
            print("Neurons activated:", neurons)

    except FileNotFoundError:
        print("Error: The file 'synaptic_neurons.json' could not be found.")

    except json.JSONDecodeError:
        print("Error: The file contains invalid JSON syntax.")


    for memory in memory_holder:

        memory_operation_iterate = 0 
        parse_memory = json.loads(memory) 
        
        neuron_status = neurons["neuron_status"]

        neuron_activated = False
        neuron_int_to_string = None

        while (neuron_activated != True):

            random_available_neuron = random.randint(1, 5000)

            memory_operation_iterate += 1

            if memory_operation_iterate == 20:
                
                print(f"Failsafe triggered for memory item {memory_holder.index(memory)}.")
                memory_operation_iterate = 0
                break

            if (neuron_status[random_available_neuron] == "Active"):

                random_available_neuron = random.random(1, 5001)
                continue

            else:

                if (len(str(random_available_neuron)) in int_to_string_map_scale.keys()):

                    int_length = int_to_string_map_scale[len(str(random_available_neuron))]

                    if (int_length == 3):

                        int_string = str(random_available_neuron)
                        int_tmp_list = []

                        for number in int_string:

                            int_tmp_list.append(int_to_string_map_single[number])

                            if len(int_tmp_list) == 1:
                                int_tmp_list.append(int_to_string_map_scale[3])

                        int_tmp_list[2] = int_to_string_map_double[int(int_tmp_list[2] + "0")]
                        neuron_int_to_string = int_tmp_list.join()

                    if (int_length == 4):

                        int_string = str(random_available_neuron)
                        int_tmp_list = []

                        for number in int_string:

                            int_tmp_list.append(int_to_string_map_single[number])

                            if len(int_tmp_list) == 1:
                                int_tmp_list.append(int_to_string_map_scale[4])

                            if len(int_tmp_list) == 3:
                                int_tmp_list.append(int_to_string_map_scale[3])

                            if len(int_tmp_list) == 4:
                                int_tmp_list.append(int_to_string_map_double[int(int_tmp_list[2] + "0")])

                        neuron_int_to_string = int(int_tmp_list)

                    if (int_length > 4):
                        print("Brain cannot keep up with the neurons at the moment, allocating to a temporary cortex..")
                        break

                    int_string = str(random_available_neuron)
                    int_tmp_list = []

                    for number in int_string:

                        if number != 0:

                            get_double_digit = int_to_string_map_double[int(int_tmp_list[0] + "0")]
                            int_tmp_list.clear()
                            neuron_int_to_string = int(get_double_digit)

                    double_digit = int_to_string_map_double[int(int_tmp_list[1] + "0")]
                    int_tmp_list[0] = double_digit

                    neuron_int_to_string = int(int_tmp_list)


                neurons["neuron_status"][random_available_neuron] = "Active"
                neurons["neuron_status"][neuron_int_to_string] = parse_memory # Assuming thisalso has the same format in json so they just be overwritten smoothly

                neuron_activated = True
                print(f"[{memory_holder.index(memory)+1}/100] Memory allocated to Neuron {random_available_neuron} (Attempts: {memory_operation_iterate})")

        asyncio.create_task(continue_memory_transport(memory))
        memory_operation_iterate = 0

synapse_watcher = watch("synaptic_neurons.json", watch_filter=memory_filter)