import time
import random
import numpy as np
from datetime import datetime, timedelta
import secrets
from enum import Enum

# Define AlertLevel enum for different severity levels
class AlertLevel(Enum):
    P0 = "P0 (Critical)"
    P1 = "P1 (Major)"
    P2 = "P2 (Minor)"
    NO_ALERT = "No Alert"

# Alert thresholds
ALERT_THRESHOLDS = {
    AlertLevel.P0: {"latency": 2000, "failure_rate": 10},
    AlertLevel.P1: {"latency": 1000, "failure_rate": 5},
    AlertLevel.P2: {"latency": 500, "failure_rate": 2},
}

# Alert repeat times (in seconds for testing)
ALERT_REPEAT_TIMES = {
    AlertLevel.P0: 2,
    AlertLevel.P1: 12,
    AlertLevel.P2: 48,
}

def get_time():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def generate_commit_hash():
    """Generate a random 40-character hexadecimal commit hash."""
    return secrets.token_hex(20)  # 20 bytes = 40 hex characters

class MetricSimulator:
    def __init__(self):
        self.latency_flaky = False
        self.failure_rate_flaky = False

    def generate_metrics(self):
        """Simulate incoming latency and failure rate data, with flaky or persistent behavior."""

        # Simulate latency (flaky or persistent)
        if not self.latency_flaky:
            if random.random() < 0.2:  # 20% chance to trigger a flaky or persistent issue
                if random.random() < 0.5:  # 50% chance of flaky behavior
                    latency = np.random.poisson(1200)  # Minor issue, more likely (~1200ms)
                    self.latency_flaky = False  # One-time issue (flaky)
                else:
                    latency = np.random.poisson(2000)  # Major issue (~2000ms)
                    self.latency_flaky = True  # Persistent issue, will persist for multiple calls
            else:
                latency = np.random.poisson(300)  # No Alert, normal latency (~300ms)
        else:
            latency = np.random.poisson(3500)  # Critical issue, least likely (~3500ms)
            if random.random() < 0.3:  # 30% chance that persistent issue resolves
                self.latency_flaky = False

        # Simulate failure rate (flaky or persistent)
        if not self.failure_rate_flaky:
            if random.random() < 0.2:  # 20% chance to trigger a flaky or persistent issue
                if random.random() < 0.5:  # 50% chance of flaky behavior
                    failure_rate = np.random.poisson(8) / 100.0  # Minor issue (~8%)
                    self.failure_rate_flaky = False  # One-time issue (flaky)
                else:
                    failure_rate = np.random.poisson(10) / 100.0  # Major issue (~10%)
                    self.failure_rate_flaky = True  # Persistent issue, will persist for multiple calls
            else:
                failure_rate = np.random.poisson(1) / 100.0  # No Alert, normal failure rate (~2%)
        else:
            failure_rate = np.random.poisson(15) / 100.0  # Critical issue, least likely (~15%)
            if random.random() < 0.3:  # 30% chance that persistent issue resolves
                self.failure_rate_flaky = False

        return latency, failure_rate

# Define Alert class
class Alert:
    def __init__(self, alert_level: AlertLevel):
        self.alert_level = alert_level
        self.trigger_time = datetime.now()  # When the alert was first triggered
        self.last_notified = datetime.now()  # When the last notification was sent
    
    def update_last_notified(self):
        """Update the last notified time to the current time."""
        self.last_notified = datetime.now()

    def time_since_trigger(self):
        """Get the time difference since the alert was first triggered."""
        return datetime.now() - self.trigger_time

    def time_since_last_notified(self):
        """Get the time difference since the last notification was sent."""
        return datetime.now() - self.last_notified

    def __str__(self):
        return f"Alert: {self.alert_level.value}, Triggered at: {self.trigger_time}, Last notified at: {self.last_notified}"

# Define CloudMonitor class that manages alerts
class CloudMonitor:
    def __init__(self):
        self.current_alert = None  # Tracks the current active alert
        self.log_history = []

    # Classify alert based on latency and failure_rate
    def classify_alert(self, latency, failure_rate):
        if latency > ALERT_THRESHOLDS[AlertLevel.P0]["latency"] or failure_rate > ALERT_THRESHOLDS[AlertLevel.P0]["failure_rate"]:
            return AlertLevel.P0
        elif latency > ALERT_THRESHOLDS[AlertLevel.P1]["latency"] or failure_rate > ALERT_THRESHOLDS[AlertLevel.P1]["failure_rate"]:
            return AlertLevel.P1
        elif latency > ALERT_THRESHOLDS[AlertLevel.P2]["latency"] or failure_rate > ALERT_THRESHOLDS[AlertLevel.P2]["failure_rate"]:
            return AlertLevel.P2
        else:
            return AlertLevel.NO_ALERT

    # Simulate alert resolution (mocking)
    def resolve_alert(self):
        if self.current_alert is not None:
            print(f"{get_time()} INFO: Issue resolved for {self.current_alert.alert_level.value}.")
            self.current_alert = None  # Reset to no alert
        else:
            print(f"{get_time()} INFO: No active alert to resolve.")

    # Email notification function (mocking)
    def send_email(self, alert_level, recipient):
        print(f"{get_time()} EMAIL: Sending {alert_level.value} alert to {recipient}")

    # Logging system status
    def log_status(self, latency, failure_rate, alert_level):
        timestamp = get_time()
        log_message = f"{timestamp} Latency: {latency}ms, Failure Rate: {failure_rate:.1%}, Alert: {alert_level.value}"
        print(log_message)
        self.log_history.append(log_message)
        if len(self.log_history) > 90 * 24 * 12:  # Logs for 90 days at 5-minute intervals
            self.log_history.pop(0)

    # Simulate PR merge to resolve persistent issues
    def simulate_pr_merge(self):
        commit_hash = generate_commit_hash()
        print(f"{get_time()} INFO: PR merged to resolve the issue. Commit Hash: {commit_hash}")

    # Handle new alerts, upgrades if needed
    def handle_alerts(self, latency, failure_rate):
        new_alert_level = self.classify_alert(latency, failure_rate)
        
        if new_alert_level == AlertLevel.NO_ALERT:
            # If the situation has normalized, resolve any active alert
            if self.current_alert:
                self.resolve_alert()
            return

        if self.current_alert is None:
            # No active alert, so create a new one
            print(f"{get_time()} {new_alert_level.value} Alert Triggered!")
            self.current_alert = Alert(new_alert_level)
            self.send_email(new_alert_level, "team@company.com")
        
        elif new_alert_level.value < self.current_alert.alert_level.value:
            # If the new alert level is greater in severity, upgrade the alert
            print(f"{get_time()} {new_alert_level.value} Alert Triggered (Upgrading)!")
            self.current_alert = Alert(new_alert_level)  # Upgrade to higher level alert
            self.send_email(new_alert_level, "team@company.com")
        
        elif new_alert_level == self.current_alert.alert_level:
            # If the same alert is triggered, check if it's time to resend
            if self.current_alert.time_since_last_notified() >= timedelta(seconds=ALERT_REPEAT_TIMES[new_alert_level]):
                print(f"{get_time()} ALERT: Resending {new_alert_level.value} alert (Still unresolved)")
                self.current_alert.update_last_notified()  # Update notification time
                self.send_email(new_alert_level, "team@company.com")
        
         # Check if it's time to notify the boss (long-standing alert)
        if self.current_alert and self.current_alert.time_since_trigger() >= timedelta(seconds=ALERT_REPEAT_TIMES[self.current_alert.alert_level] * 5):
            self.send_email(self.current_alert.alert_level, "boss@company.com")

        # Randomly resolve persistent issue by simulating PR merges
        if self.current_alert and random.random() < 0.1:  # 10% chance to mock a PR merge if alert persists
            self.simulate_pr_merge()

def monitor_system():
    # Create instances of MetricSimulator and CloudMonitor
    metric_simulator = MetricSimulator()
    cloud_monitor = CloudMonitor()

    # Monitoring loop (runs every 5 minutes, or adjust the time interval)
    try:
        while True:
            latency, failure_rate = metric_simulator.generate_metrics()

            cloud_monitor.log_status(latency, failure_rate, cloud_monitor.classify_alert(latency, failure_rate))

            cloud_monitor.handle_alerts(latency, failure_rate)

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user.")

# Run the system
if __name__ == "__main__":
    monitor_system()