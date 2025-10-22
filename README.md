# Distributed-computing-framework
This is a network design of how distributed computing is working in a network.

🌐 Network-Based Distributed Computing Framework
📘 Overview

This project implements a Network-Based Distributed Computing Framework using Python.
It simulates the distribution of computing tasks across multiple networks of worker nodes, featuring:

✅ Task Scheduling

⚖️ Load Balancing

🧩 Fault Tolerance and Recovery

Each worker node processes tasks, can randomly fail, recover after downtime, and automatically reassign tasks from a queue — providing a simplified model of real-world distributed systems.

🚀 Features

Multi-Network System:
Tasks are distributed among several independent networks, each containing multiple worker nodes.

Task Scheduling:
Implements a round-robin scheduling algorithm to distribute tasks evenly among networks.

Load Balancing:
Ensures that tasks are dynamically assigned to available worker nodes.

Fault Tolerance:
Simulates random node failures (with automatic recovery) and reassigns incomplete tasks.

Task Queue Management:
Unprocessed or failed tasks are added to a queue and picked up by recovered nodes.

🧠 How It Works

Master Node

Creates multiple networks, each containing several worker nodes.

Generates and distributes tasks to workers using round-robin scheduling.

Monitors load and manages the global task queue.

Worker Nodes

Continuously run as threads simulating distributed computing.

Randomly fail and recover (to test fault tolerance).

Pick tasks from the queue upon recovery.

Log task start, completion, failure, and recovery events.

⚙️ Technologies Used
Component	Description
Language	Python 3.x
Modules	threading, queue, time, random, logging
Concepts	Distributed Systems, Load Balancing, Fault Tolerance, Multithreading
🧩 Code Structure
main09.py
├── WorkerNode (class)
│   ├── run()                # Simulates node activity, failure, and recovery
│   ├── process_task()       # Handles task assignment
│   ├── _handle_task()       # Simulates task execution
│   └── check_queue()        # Picks tasks from the queue after recovery
│
└── MasterNode (class)
    ├── distribute_tasks()   # Distributes tasks in round-robin fashion
    ├── assign_task_to_network() # Assigns tasks to available workers
    └── start()              # Starts the framework

🧪 How to Run

Clone the Repository

git clone https://github.com/yourusername/distributed-computing-framework.git
cd distributed-computing-framework


Run the Program

python main09.py


Observe Logs

Logs will appear in your console showing:

Task assignment and completion.

Node failures and recoveries.

Tasks being picked up from the queue.

📊 Example Log Output
2025-10-22 18:30:05 - INFO - Task-5 started by Network-1 Node-12
2025-10-22 18:30:12 - ERROR - Network-0 Node-7 has failed.
2025-10-22 18:30:18 - INFO - Network-0 Node-7 has recovered.
2025-10-22 18:30:19 - INFO - Network-0 Node-7 picked up Task-22 from the queue.
2025-10-22 18:30:27 - INFO - Task-22 completed by Network-0 Node-7

🛠️ Configuration

You can easily customize the simulation in the MasterNode constructor:

master_node = MasterNode(networks=3, nodes_per_network=50, tasks=1000)

Parameter	Description	Default
networks	Number of independent networks	3
nodes_per_network	Number of worker nodes per network	50
tasks	Total number of tasks to simulate	1000
📈 #Future Enhancements

Implement real network communication using socket or gRPC.

Add task prioritization and dynamic scaling of nodes.

Visualize task distribution and completion with a web dashboard.

Include persistent state tracking using databases or message queues (e.g., RabbitMQ).
