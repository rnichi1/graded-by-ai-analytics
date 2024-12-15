def get_average_accuracy(tracker):
    cleaned_tracker = []
    accuracy_sum = 0
    for x in tracker:
        # check nan
        if x['accuracy'] == x['accuracy'] and x['accuracy'] >= 0:
            cleaned_tracker.append(x)
            accuracy_sum += x['accuracy']
        else:
            # Add 0 for wrong data to still count it in the average
            cleaned_tracker.append(0)
    average = accuracy_sum / len(cleaned_tracker)
    return average, cleaned_tracker