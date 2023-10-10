
import matplotlib.pyplot as plt

# Generate data
udp_response_times = [1.29, 1.29,1.29,1.29,1.29,1.29,1.29,1.29,1.29,1.08]
tcp_response_times = [.0571, 0.0578, 0.05, 0.057, 0.0404,.0506,.0537,.0503,.0568,.0472]
concurrent_requests = [1, 10, 50, 100, 500, 1000, 2500, 5000, 7500, 10000]

# Create the plot
plt.plot(concurrent_requests, udp_response_times, label="UDP")
plt.plot(concurrent_requests, tcp_response_times, label="TCP")

# Set the labels and title
plt.xlabel("Concurrent Requests")
plt.ylabel("Average Request Response Time (ms)")
plt.title("Average Request Response Time vs. Concurrent Requests")

# Add a legend
plt.legend()

# Show the plot
plt.show()