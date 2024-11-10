import time
#import matplotlib.pyplot as plt

class Statistics:

    def __init__(self):
        self.streams = {}
        self.start_time = time.time()  # Track the start time

    def add_stream(self, stream_id):
        if stream_id not in self.streams:
            self.streams[stream_id] = {
                "total_bytes": 0,
                "total_packets": 0,
                "start_time": time.time(),
                "end_time": None,
                "data" : ""
            }

    def update_stream(self, stream_id, data_length,data):
        if stream_id in self.streams:
            stream = self.streams[stream_id]
            stream["total_bytes"] += data_length
            stream["total_packets"] += 1  # Assuming each data chunk is one packet
            stream["end_time"] = time.time()

    def calculate_statistics(self):
        stats = {}
        total_data_rate = 0
        total_packet_rate = 0
        total_time = time.time() - self.start_time  # Calculate total time

        for stream_id, stream in self.streams.items():
            stream_time = stream["end_time"] - stream["start_time"]
            data_rate = stream["total_bytes"]/ stream_time
            packet_rate = stream["total_packets"] / stream_time

            stats[stream_id] = {
                "total_bytes (bytes)": stream["total_bytes"],
                "total_packets (number)": stream["total_packets"],
                "data_rate (bytes/sec)": data_rate,
                "packet_rate (packet/sec)": packet_rate
            }

            total_data_rate += data_rate
            total_packet_rate += packet_rate

        overall_data_rate = total_data_rate/len(stats.keys())
        overall_packet_rate = total_packet_rate /len(stats.keys())

        stats["overall"] = {
            "avg_data_rate (bytes/sec)": overall_data_rate,
            "avg_packet_rate (packet/ms)": overall_packet_rate
        }

        print("Overall statistics:\n-----------------------------------")
        for stream in stats:
            print("Stream ID: ", stream)
            for i in stats[stream]:
                if(i == "data"):
                    continue
                print(i, ": ", stats[stream][i])
            print("------------------------------------")
        

        # # x axis values
        # x = [1,2,3]
        # # corresponding y axis values
        # y = [2,4,1]

        # # plotting the points 
        # plt.plot(x, y)

        # # naming the x axis
        # plt.xlabel('x - axis')
        # # naming the y axis
        # plt.ylabel('y - axis')

        # # giving a title to my graph
        # plt.title('My first graph!')

        # # function to show the plot
        # plt.show()