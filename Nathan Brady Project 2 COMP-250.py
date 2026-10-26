# -*- coding: utf-8 -*-
"""
@author: nbrady 
"""

from collections import deque

# global variable
alertCounter = 1


# create new alert and add to the queue
def createAlert(queue, sourceIP, description, severity):
    global alertCounter
    
    # create dictionary
    alert = {
        "id": alertCounter,
        "source_ip": sourceIP,
        "description": description,
        "severity": severity
        }
    
    alertCounter += 1
    
    # severity = 5, critical alerts go to the front
    if severity == 5:
        queue.appendleft(alert)
    else: # other alerts go to the back
        queue.append(alert)
    
    return alert

# display an alerts information
def displayAlert(alert):
    print(f"[ID {alert['id']}] Severity {alert['severity']} | {alert['source_ip']} | {alert['description']}")
    
# resolve the next alert in the queue
def resolveAlert(queue, resolved):
    if not queue:
        print("No pending alerts.")
    else: # move into the resolved stack
        alert = queue.popleft()
        resolved.append(alert)
        print("Resolved Alert: ")
        displayAlert(alert)
    
# undo the most recent resolution
def undoAlert(queue, resolved):
    if not resolved:
        print("Nothing to undo.")
    else: # and move it to the front
        alert = resolved.pop()
        queue.appendleft(alert)
        print("Restored Alert: ")
        displayAlert(alert)
        
# search alert via ID
def search_alert(alerts, target_id, index):
    # Base case no more alerts
    if index >= len(alerts):
        return None
    # Base case, matching alert found
    if alerts[index]["id" ] == target_id:
        return alerts[index]
    
    # go through again to check next alert
    return search_alert(alerts, target_id, index + 1)
    
def total_severity(alerts, index):
    # Base case, hit end of list
    if index >= len(alerts):
        return 0
    # add to the current severity and continue through
    return alerts[index]["severity"] + total_severity(alerts, index + 1)

# get info to create a new alert
def addNewAlert(queue):
    sourceIP = input("Enter Source IP: ")
    
    # make sure source IP isn't empty
    while sourceIP.strip() == "":
        print("Input cannot be empty.")
        sourceIP = input("Enter Source IP: ")
    
    description = input("Enter Description: ")
    
    # make sure description isn't empty
    while description.strip() == "":
        print("Input cannot be empty.")
        description = input("Enter Description: ")
    
    severity = get_int("Enter Severity (1 to 5): ", 1, 5)
    alert = createAlert(queue, sourceIP, description, severity)
    print("Added Alert: ")
    displayAlert(alert)
    
# view the next alert without removing it
def viewNewAlert(queue):
    if not queue:
        print("No pending alerts.")
    else:
        displayAlert(queue[0])
    
# view all pending alets
def viewPendingAlerts(queue):
    if not queue:
        print("No pending alerts.")
    else:
        for alert in queue:
            displayAlert(alert)
           
            # calculate severity
    totalSeverity = total_severity(list(queue), 0)
    print("Total Severity ", totalSeverity)
    
# show resolved alerts frm newest to oldest
def viewResolutionHistory(resolved):
    if not resolved:
        print ("No resolution history.")
    else: # start with the last resolved alert
        i = len(resolved) - 1
        
        while i >= 0:
            displayAlert(resolved[i])
            i -= 1
            
 # search alerts for specific ID       
def searchAlertByID(queue):
    if not queue:
        print("No pending alerts.")
    else:
        ID = get_int("Enter Alert ID: ", 1, alertCounter -1)
        alert = search_alert(list(queue), ID, 0)
        
    if alert is None:
        print("Alert not found.")
    else:
        displayAlert(alert)
    
# message to print when exiting goodbye!
def exitMessage():
    print("Goodbye!")
    
    # keep asking until the user enters a value number for our needs
def get_int(prompt, low, high):
    while True:
        value = input(prompt)
        
        if value.isdigit():
            number = int(value)
            
            if low <= number <= high:
                return number
            
        print("Input is not valid. Enter another.")
        
# main, sets up queue and runs menu
def main():
    queue = deque()
    resolved = []
    
    # five starting alerts
    createAlert(queue, "10.0.0.5", "Port scan detected", 2)
    createAlert(queue, "192.168.1.10", "Multiple failed login attempts", 4)
    createAlert(queue, "172.16.0.8", "Ransomware signature detected", 5)
    createAlert(queue, "10.0.0.22", "Unusual outbound traffic", 3)
    createAlert(queue, "192.168.1.45", "Expired SSL certificate", 1)
    
    
    # always show menu unless user exits (8)
    while True:
        print("===== SOC ALERT TRIAGE CONSOLE =====")
        print("1. Add new alert")
        print("2. View next alert")
        print("3. Resolve next alert")
        print("4. Undo last resolution")
        print("5. View all pending alerts")
        print("6. View resolution history")
        print("7. Search alert by ID")
        print("8. Exit")
        
        option = get_int("Choose an option: ", 1 , 8)

        # check which menu option the user selected
        if option == 1:
            addNewAlert(queue)
        elif option == 2:
            viewNewAlert(queue)
        elif option == 3:
            resolveAlert(queue, resolved)
        elif option == 4:
            undoAlert(queue, resolved)
        elif option == 5:
            viewPendingAlerts(queue)
        elif option == 6:
            viewResolutionHistory(resolved)
        elif option == 7:
            searchAlertByID(queue)
        elif option == 8:
            exitMessage()
            break
# Run main      
main()

# Step 7: Time Complexity Analysis
"""
1. O(1) This is O(1) because adding a regular alert takes constant time
2. O(1) Adding a critical alert to the front of a deque takes constant time
3. O(1) Resolving the next alert uses a popleft() which takes constant time
4. O(1) Undoing the last resolution uses a pop() and appendleft() which takes constant time
5. O(n) Searching for an alert is looping through a list, maybe checking all
6. O(n) Removing the first item from a list requires looping throuhg and shifting the other items
7. O(n) A loop would be better in this example to check thousands of alerts because recursion can reach Pythons recursion limit
"""
    