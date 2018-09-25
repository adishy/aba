function viewcurrenttickets(){
    socket.emit('viewcurrenttickets')
}

function getticketdetailsprovided(){
    addsupportticketprovided(document.getElementById('supporttypeentry')
                                        .options[document.getElementById('supporttypeentry').selectedIndex].value, 
                                document.getElementById('supportdescriptionentry').value,
                                document.getElementById('supportlocationentry').value,
                                document.getElementById('supportdateentry').value + ' ' + document.getElementById('supporttimeentry').value)						
                                console.log(document.getElementById('supportdateentry').value + ' ' + document.getElementById('supporttimeentry').value)

    toggleHidden(SUPPORT_TICKET_ENTRY);
}

function copysupportticketdetails(some_support_id_provided){
    getSupportTicketText(supportticketsbox.getSupportTicket(some_support_id_provided));
    notificationList.addNotification('Copied ticket to clipboard');
}

function showticketdetails(event, some_support_id_provided){
    if(event.target
            .className == 'issueoption' 
        || document.getElementById(`issueoption_${some_support_id_provided}`)
                    .contains(event.target)){
        toggleOption(document.getElementById(some_support_id_provided));
        return;
    }
    
    supportticketdetails.supportTicketDetails(supportticketsbox.getSupportTicket(some_support_id_provided));
}

function cancelsupportticket(some_ticket_id_provided){
    supportticketdetails.removeSupportTicketDetails();
    socket.emit('cancelsupportticket', 
                {supportid: some_ticket_id_provided});
}

function logoutCurrentUser(){
    window.location.href = 'logout';
}

    
function toggleOption(some_given_element, some_given_callback){
    console.log('nfsdjnfjksdn');

    toggleHidden(some_given_element);
    
    if(ACTIVE_OPTION == some_given_element) ACTIVE_OPTION = '';
    
    else ACTIVE_OPTION = some_given_element;
    
    toggleHidden(OPTION_BACKGROUND);

    if(typeof some_given_callback == 'function') some_given_callback();

    console.log(some_given_element.style);
    console.log(some_given_element.classList);
}

function showSidebar(){
    toggleClass(document.querySelector('.sidebar'), 'sidebarview');
}

function toggleClass(some_element_provided, some_class_provided){
    if(some_element_provided.classList.contains(some_class_provided)) some_element_provided.classList.remove(some_class_provided);

    else some_element_provided.classList.add(some_class_provided);
}

function toggleHidden(some_given_element){
    if(some_given_element.style.display == '') some_given_element.style.display = 'none';
    
    if(some_given_element.style.display == 'block') some_given_element.style.display = 'none';
        
    else if(some_given_element.style.display == 'none') some_given_element.style.display = 'block';
}

function showuserdetails(event){
    if(event.target.id == 'notificationbuttonpictureview' || event.target.tagName == 'svg'){
        toggleOption(document.querySelector('.usernotificationview'));
        notificationBoxView.addSeenNotifications();
        return;
    }

    toggleOption(CURRENT_USER);
}