# TFT Leaderboard Tracker

The TFT Leaderboard Tracker is an innovative analytics platform tailored for enthusiasts of Riot Games' Teamfight Tactics (TFT). It dynamically fetches and displays real-time Leaderboard statistics, including the LP (League Points) cutoffs for Challenger and Grandmaster tiers, leveraging the official Riot Games TFT API. Users can access up-to-date insights on rank distributions, facilitating strategic gameplay and competitive analysis.

This application is a must-have tool for TFT players aiming to understand their standings and the competitive landscape, offering a detailed view of the top-tier gameplay thresholds.

---

### Built with
This application harnesses the power of `Python 3.8` and is built using the Flask web framework, alongside other key technologies:
* [Flask](https://pypi.org/project/Flask/) - Web framework for building the API and serving the application
* [requests](https://pypi.org/project/requests/) - HTTP Requests for API calls to Riot Games' TFT API
* [APScheduler](https://pypi.org/project/APScheduler/) - Job scheduling to periodically update data
* [Chart.js](https://www.chartjs.org/) - Front-end charting library for visualizing data trends
* [HTML/CSS](https://developer.mozilla.org/en-US/docs/Web/HTML) - For structuring and styling the web application interface
* [Git](https://git-scm.com/) - Version control system

---

### Installation and Usage
Ensure you have Python installed on your system. Clone or download this repository to your local machine:

1. **Clone the repository:**

```git clone https://github.com/mtt04/TFT-Leaderboard-Tracker.git```

2. **Navigate to the project directory:**

```cd TFT-Leaderboard-Tracker```

3. **Install the required packages:**

```pip install -r requirements.txt```

4. **Add your Riot Games API key:** Open the `app.py` file (or the relevant file if your main Flask file has a different name) and replace the placeholder for the API key with your own Riot Games API key.

5. **Run the Flask application:**

```python app.py```

6. **Access the web application:** Open your web browser and navigate to `http://127.0.0.1:5000/` to view the TFT Leaderboard Tracker.

---

### How it Works

The TFT Leaderboard Tracker periodically calls the Riot Games TFT API to fetch the latest leaderboard data, including player rankings and LP scores. It then processes and displays this data through a user-friendly web interface:

- **Real-time Updates:** Utilizes APScheduler to automatically refresh the leaderboard data every 10 minutes, ensuring that users have access to the most current information.
- **Historical Analysis:** Tracks changes in the LP cutoffs for Challenger and Grandmaster tiers over time, offering insights into competitive trends and player performance.
- **Data Visualization:** Employs Chart.js to create intuitive and interactive charts, enabling users to visually grasp the competitive dynamics of TFT.

---