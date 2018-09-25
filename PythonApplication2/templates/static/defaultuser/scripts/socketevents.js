var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
    console.log("sent message")
    viewcurrenttickets();
});	


socket.on('connectmessage', function(somedataprovided){
    console.log(somedataprovided);
});

socket.on('addedsupportticket', function(someticketprovided){
    console.log('Added ticket')
    console.log(someticketprovided);
    viewcurrenttickets();
    notificationList.addNotification('Added support ticket');
})


socket.on('cancelledsupportticket', function(){
    viewcurrenttickets();
    notificationList.addNotification('Cancelled support ticket');
});

socket.on('changedsupportticketstatusdescription', function(){
    viewcurrenttickets();
    notificationList.addNotification('Changed support status');
});

socket.on('changedsupportticketstatus', function(){
    viewcurrenttickets();
    notificationList.addNotification('Changed support status');
});

socket.on('claimedsupportticket', function(some_support_staff_assigned){
    viewcurrenttickets();
    console.log(some_support_staff_assigned);
    notificationList.addNotification(`Support ticket claimed by ${JSON.parse(some_support_staff_assigned).supportstaffassigned}`);
});

socket.on('currenttickets', function(someticketlistprovided){
    console.log(someticketlistprovided);
    /**
    var ticketlistprovided = JSON.parse(someticketlistprovided);**/
    
    supportticketsbox.removeAllSupportTickets();
    
    /** 
    if(typeof supportticketlistprovided == Array){
        someticketlistprovided = someticketlistprovided.sort(function(some_element_one, some_element_two){
            var element_one = new Date(Date.parse(some_element_one.ticketsubmissiondatetime)).getTime();

            var element_two = new Date(Date.parse(some_element_two.ticketsubmissiondatetime)).getTime();

            if(element_one < element_two) return 1;

            if(element_one > element_two) return -1;

            return 0;
        });
    }**/

    supportticketsbox.addTicketsProvided(someticketlistprovided);
});

socket.on('supportstaffmembers', function(some_support_staff_members_list){
    if(!supportstaffmemberdetailsview.loadedSupportStaffMembers){
        supportstaffmemberdetailsview.addSupportStaffMembers(JSON.parse(some_support_staff_members_list));
        supportstaffmemberdetailsview.loadedSupportStaffMembers = true;
    }
});
