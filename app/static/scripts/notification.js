$(function () {            

    $.ajax({
        type:"GET",
        url: getNotificationUrl,
        success: function(data) {
            notificationInfos = JSON.parse(data);
            for(notification in notificationInfos){
                prependNotification(notificationInfos[notification]);
            }
        }
    });

    socket.on(HISHOP_UID + 'To' + currentUser, function(data){                
        prependNotification(data);
    });
});