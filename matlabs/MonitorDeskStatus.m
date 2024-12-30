function monitorDeskStatus()
    % This function monitors the desk status using ThingSpeak data. It checks
    % whether the desk is occupied or unoccupied and sends email alerts if
    % thresholds for occupancy or inactivity are exceeded.

    % ThingSpeak configuration
    channelID = 2792998; 
    readAPIKey = 'XICTHWA0KKU6P5MI'; 
    fieldNumber = 1; 

    % Persistent variable to track the time the last alert was sent
    persistent lastAlertTime;
    if isempty(lastAlertTime)
        % we initialize the last alert time to ensure alerts can be sent immediately
        lastAlertTime = datetime('now') - minutes(31); 
    end

    % Alert configuration
    alertThresholdMinutes = 30; % Threshold: desk must be occupied for 30+ minutes to send an alert
    unoccupiedAlertThreshold = 5; % Threshold: desk must be unoccupied for 5+ minutes to send an alert
    emailRateLimitMinutes = 1; % Minimum time between consecutive email alerts

    % Here we get the latest status of the desk from thingspeek
    try
        % Reads the latest value from the specified field in thingspeak
        
        deskStatus = thingSpeakRead(channelID, 'Fields', fieldNumber, ...
            'NumPoints', 1, 'ReadKey', readAPIKey);
        disp(['Latest desk status: ', num2str(deskStatus)]);
    catch ME
        % Error handling if ThingSpeak read operation fails
        disp('Error reading from ThingSpeak:');
        disp(ME.message);
        return; 
    end

    % Get the current time
    currentTime = datetime('now');

    % We make sure alerts are sent not too frequently 
    if minutes(currentTime - lastAlertTime) < emailRateLimitMinutes
        disp('Skipping email alert due to rate limit.');
        return; % Exit if the rate limit condition is met
    end

    % Here we have some if statments to check which email to send in this case we send 
    % Prolonged activity email which triggers after 30min pass
    
    if deskStatus == 1
        % Desk is occupied; check if occupancy exceeds threshold
        if minutes(currentTime - lastAlertTime) > alertThresholdMinutes
            disp('Desk has been occupied for over 30 minutes.');
            
            % Prepare and send an email alert for prolonged occupancy
            alertBody = 'The desk has been occupied for more than 30 minutes.';
            alertSubject = 'Prolonged Desk Occupancy Alert';
            sendEmailAlert(alertSubject, alertBody);

            % Update the last alert time to the current time
            lastAlertTime = currentTime;
        end
    elseif deskStatus == 0
        % Desk is unoccupied, for 5 min and email threshhold is not exceeded we send an email telling us that.
        if minutes(currentTime - lastAlertTime) > unoccupiedAlertThreshold
            disp('Desk is unoccupied for 5 minutes.');
            
            % Prepare and send an email alert for prolonged inactivity
            alertBody = 'The desk is now unoccupied.';
            alertSubject = 'Desk Unoccupied Alert';
            sendEmailAlert(alertSubject, alertBody);

            % Update the last alert time to the current time
            lastAlertTime = currentTime;
        end
    end

    % Function to send an email alert using ThingSpeak Alerts API
    function sendEmailAlert(subject, body)
        % Configurations for ThingSpeak Alerts API
        alertsAPIKey = 'TAKegks/Ip1vYrF1wBa'; 
        alertsURL = 'https://api.thingspeak.com/alerts/send'; 

        % Construct JSON message with subject and body
        jsonMessage = jsonencode(struct('subject', subject, 'body', body));

        % Configure web options for the HTTP request
        options = weboptions('HeaderFields', ...
            {'ThingSpeak-Alerts-API-Key', alertsAPIKey; ...
             'Content-Type', 'application/json'});

        % Send the email alert using a POST request
        try
            response = webwrite(alertsURL, jsonMessage, options);
            if response.StatusCode == 200
                disp(['Email alert sent: ', subject]); % Confirm successful alert
            end
        catch ME
            % Handle errors during the email alert process
            disp('Error sending email alert:');
            disp(ME.message);
        end
    end
end
