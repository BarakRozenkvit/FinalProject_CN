import time

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
            stream["data"] += data

    # def hagit_check(self):
    #     for stream in self.streams:
    #         with open(f"Files/{stream}.txt", "wb") as f:
    #             data_to_write = self.streams[stream]["data"]
    #             if isinstance(data_to_write, str):
    #                 data_to_write = data_to_write.encode()
    #             f.write(data_to_write)

    def calculate_statistics(self):
        stats = {}
        total_bytes = 0
        total_packets = 0
        total_time = time.time() - self.start_time  # Calculate total time

        for stream_id, stream in self.streams.items():
            stream_time = stream["end_time"] - stream["start_time"]
            avg_data_rate = stream["total_bytes"] / stream_time
            avg_packet_rate = stream["total_packets"] / stream_time

            stats[stream_id] = {
                "total_time (ms)": stream_time * 1000,
                "total_bytes (bytes)": stream["total_bytes"],
                "total_packets (number)": stream["total_packets"],
                "avg_data_rate (bytes/sec)": avg_data_rate,
                "avg_packet_rate (packet/sec)": avg_packet_rate
            }

            total_bytes += stream["total_bytes"]
            total_packets += stream["total_packets"]

        overall_data_rate = total_bytes / total_time if total_time > 0 else 0
        overall_packet_rate = total_packets / total_time if total_time > 0 else 0

        stats["overall"] = {
            "total_bytes": total_bytes,
            "total_packets": total_packets,
            "avg_data_rate": overall_data_rate,
            "avg_packet_rate": overall_packet_rate
        }

        print("Overall statistics:\n-----------------------------------")
        for stream in stats:
            print("Stream ID: ", stream)
            for i in stats[stream]:
                if(i == "data"):
                    continue
                print(i, ": ", stats[stream][i])