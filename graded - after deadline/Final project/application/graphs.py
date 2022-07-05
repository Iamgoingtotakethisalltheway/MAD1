import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import datetime
import os
plt.style.use("seaborn")

'''tracker_stats =  [{'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sun, 16 Mar 2022 19:56:25 -0000', 'value': '6', 'note': 'Had a super run today!'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sun, 15 Mar 2022 19:53:00 -0000', 'value': '4', 'note': 'Had a great run today!'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 14 Mar 2022 22:16:49 -0000', 'value': '2', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 13 Mar 2022 22:16:49 -0000', 'value': '2', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 12 Mar 2022 22:16:48 -0000', 'value': '2', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 11 Mar 2022 22:16:48 -0000', 'value': '2', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 10 Mar 2022 22:16:42 -0000', 'value': '5', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 09 Mar 2022 22:16:42 -0000', 'value': '5', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 08 Mar 2022 22:16:42 -0000', 'value': '5', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 07 Mar 2022 22:16:37 -0000', 'value': '4', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 06 Mar 2022 22:16:37 -0000', 'value': '4', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 06 Mar 2022 22:16:36 -0000', 'value': '3', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 05 Mar 2022 22:16:36 -0000', 'value': '4', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 05 Mar 2022 22:16:27 -0000', 'value': '6', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 04 Mar 2022 22:16:27 -0000', 'value': '6', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 03 Mar 2022 22:16:20 -0000', 'value': '6', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 02 Mar 2022 22:13:09 -0000', 'value': '6', 'note': 'ran 6 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 01 Mar 2022 22:12:48 -0000', 'value': '5.5', 'note': 'ran 5.5 kms today'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 28 Feb 2022 22:12:04 -0000', 'value': '5', 'note': 'ran 5 kms'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 27 Feb 2022 22:11:40 -0000', 'value': '3', 'note': 'ran 3 kms'}, {'user_id': 1, 'tracker_id': 1, 'timestamp': 'Sat, 26 Feb 2022 22:11:14 -0000', 'value': '4', 'note': 'ran 4 kms today'}]'''

def line_plot(tracker_stats):
    x, y = [], []
    for log in tracker_stats:
        log_date = log["timestamp"][0:-9]
        log_date = datetime.datetime.strptime(log_date, '%a, %d %b %Y %H:%M')
        log_date = log_date.date()
        x.append(log_date)
        y.append(float(log["value"]))
    
    plt.clf()
    plt.plot_date(x, y, linestyle="solid")
    plt.gcf().autofmt_xdate()
    plt.savefig("./static/graph.png")

# line_plot(tracker_stats)


def pie_chart(tracker_stats):
    value_counts = dict()
    for log in tracker_stats:
        value_counts[log["value"]] = value_counts.get(log["value"], 0) + 1
    labels = value_counts.keys()
    counts = value_counts.values()
    explode = tuple([0.03 for i in range(len(labels))])        # only "explode" the 2nd slice

    plt.clf()
    plt.pie(counts, labels=labels, explode=explode, autopct='%1.1f%%')
    plt.savefig("./static/graph.png")