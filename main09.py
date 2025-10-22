import socket
import threading
import time
import random
import logging
from queue import Queue

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WorkerNode(threading.Thread):
    def __init__(self, network_id, node_id, task_queue):
        super().__init__()
        self.network_id = network_id
        self.node_id = node_id
        self.available = True
        self.failed = False  # Simulate failure
        self.task_queue = task_queue  # Store reference to the shared task queue
        self.lock = threading.Lock()

    def run(self):
        while True:
            if random.random() < 0.05:  # Simulate a 1% chance of failure
                logging.error(f"{self.network_id} Node-{self.node_id} has failed.")
                self.failed = True
                time.sleep(random.uniform(5, 10))  # Simulate downtime before recovery
                self.failed = False
                logging.info(f"{self.network_id} Node-{self.node_id} has recovered.")
                self.available = True  # Set the worker as available after recovery
                self.check_queue()  # Check for tasks to process after recovery
            time.sleep(1)  # Simulate node being active

    def process_task(self, task):
        with self.lock:
            if self.available and not self.failed:
                self.available = False
                # Create a separate thread to handle task execution
                threading.Thread(target=self._handle_task, args=(task,)).start()

    def _handle_task(self, task):
        try:
            logging.info(f"{task} started by {self.network_id} Node-{self.node_id}")
            time.sleep(random.uniform(5, 10))  # Simulate task processing time
            logging.info(f"{task} completed by {self.network_id} Node-{self.node_id}")
        except Exception as e:
            logging.error(f"Error processing {task}: {e}")
            self.task_queue.put(task)  # Put the task back in the queue if an error occurs
        finally:
            with self.lock:
                self.available = True
            self.check_queue()  # Check the queue for more tasks after completing the current one

    def check_queue(self):
        if not self.failed and self.available:
            # If the node has recovered and is available, check the task queue
            if not self.task_queue.empty():
                next_task = self.task_queue.get()
                logging.info(f"{self.network_id} Node-{self.node_id} picked up {next_task} from the queue.")
                self.process_task(next_task)  # Process the next task from the queue

class MasterNode:
    def __init__(self, networks=3, nodes_per_network=50, tasks=1000):
        self.task_queue = Queue()  # Initialize the task queue first
        self.networks = {
            f"Network-{i}": [WorkerNode(f"Network-{i}", node_id, self.task_queue) for node_id in range(nodes_per_network)] 
            for i in range(networks)
        }
        self.tasks = [f"Task-{i}" for i in range(tasks)]
        self.lock = threading.Lock()
        self.current_network = 0  # Used for round-robin

        # Start all worker nodes
        for network in self.networks.values():
            for worker in network:
                worker.start()

    def start(self):
        # Start distributing tasks
        self.distribute_tasks()

    def distribute_tasks(self):
        for task in self.tasks:
            assigned = False
            while not assigned:
                # Try to assign tasks using round-robin method
                network_name = f"Network-{self.current_network}"
                assigned = self.assign_task_to_network(network_name, task)
                self.current_network = (self.current_network + 1) % len(self.networks)
                if not assigned:
                    logging.warning(f"No available nodes for {task} in {network_name}. Task queued.")
                    self.task_queue.put(task)
                    break

    def assign_task_to_network(self, network, task):
        with self.lock:
            available_workers = [worker for worker in self.networks[network] if worker.available and not worker.failed]
            if available_workers:
                # Assign to the first available worker (round-robin)
                worker = available_workers[0]
                worker.process_task(task)  # Pass the task to the worker
                return True
            return False

if __name__ == "__main__":
    master_node = MasterNode()
    master_node.start()
