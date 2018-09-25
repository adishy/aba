
var OPTION_BACKGROUND = '';

var ACTIVE_OPTION = '';

var CURRENT_USER = '';

var someSupportTicketBox = '';

window.onload = function(){
    OPTION_BACKGROUND = document.getElementById('optionbackground');
    CURRENT_USER = document.getElementById('currentuserbox')
    SUPPORT_TICKET_ENTRY = document.getElementById('newsupportticket');
    SIDEBARVIEW= document.querySelector('.sidebar');
    notificationList.notificationElementInDOM = document.getElementById('someelementprovided');
    supportticketdetails.elementInDOM = document.getElementById('supportticketdetailsbox');
    newsupportticketbox.elementInDOM = document.getElementById('newsupportticket');
    newsupportticketbox.addSupportTicketView();
    
    someSupportTicketBox = new Siema({selector: document.getElementById('supportticketsview'),
                                            perPage: {768: 3}, 
                                            onChange: currentSupportTicketTitle});

    var supportticketbox = document.querySelectorAll('.ticketviewbox');
                
    for(var i = 0; i < supportticketbox.length; ++i){
        supportticketbox[i].style.cssText = `height: ${window.innerHeight - 128}px`;
    }

    
    var content_views = document.querySelectorAll('.supporttickets');

    var sidebar_menu_options = document.querySelectorAll('.sidebar_menu_item');

    for(var i = 0; i < sidebar_menu_options.length; ++i){
        sidebar_menu_options[i].onclick = function(){
            for(var i = 0; i < content_views.length; ++i) content_views[i].style.display = 'none';
            
            for(var i = 0; i < sidebar_menu_options.length; ++i) sidebar_menu_options[i].classList.remove('active_menu_item');

            this.classList.add('active_menu_item');
            
            content_views[Array.prototype.indexOf.call(sidebar_menu_options, this)].style.display = 'grid';
        }
    }

    sidebar_menu_options[2].previousOnClick = sidebar_menu_options[2].onclick;

    sidebar_menu_options[2].onclick = function(){
        sidebar_menu_options[2].previousOnClick();

        if(!supportstaffmemberdetailsview.loadedSupportStaffMembers){
            socket.emit('viewsupportstaffmembers');
        }
    }

    for(var i = 0; i < content_views.length; ++i){
        content_views[i].style.display = 'none';
    }

    content_views[0].style.display = 'grid';
    
    notificationBoxView.addNotificationListBox(document.querySelector('.usernotificationview'));
};

window.onresize = function(){
    var supportticketbox = document.querySelectorAll('.ticketviewbox');
    
    if(window.innerWidth > 768){			
        for(var i = 0; i < supportticketbox.length; ++i){
            supportticketbox[i].style.cssText = `height: ${window.innerHeight - 128}px`;
        }
        
        showSupportTickets('ongoing');

        return;
    }
    
    for(var i = 0; i < supportticketbox.length; ++i){
        supportticketbox[i].style.height = '100%';
    }	
};

var changeSupportTicketsCategoryTitle = function(some_support_ticket_category_element_provided){
    window.scrollTo(0, 0);

    var supportTicketTitles = document.querySelectorAll('.column_title');

    for(var i = 0; i < supportTicketTitles.length; ++i){
        supportTicketTitles[i].classList.remove('column_selected');
        supportTicketTitles[i].classList.add('column_not_active');
    }

    var supportTicketsTitleProvided = document.querySelector(some_support_ticket_category_element_provided);
    supportTicketsTitleProvided.classList.remove('column_not_active');
    supportTicketsTitleProvided.classList.add('column_selected');
};

var currentSupportTicketTitle = function(){
    switch(someSupportTicketBox.currentSlide){
        case 0:
            changeSupportTicketsCategoryTitle('.ongoing_support_tickets_title');
        break;

        case 1:
            changeSupportTicketsCategoryTitle('.delayed_support_tickets_title');
        break;

        case 2:
            changeSupportTicketsCategoryTitle('.complete_support_tickets_title');
        break;
    }
};


function showSupportTickets(some_support_ticket_category_provided){
    switch(some_support_ticket_category_provided){
        case 'ongoing':
            someSupportTicketBox.goTo(0);
        break;

        case 'delayed':
            someSupportTicketBox.goTo(1);
        break;

        case 'complete':
            someSupportTicketBox.goTo(2);
        break;
    }

}

var newsupportticketbox = new newsupportticketview();


var supportticketsbox = new supportticketlistview(document.getElementById('ongoingticketviewbox'), 
                                                    document.getElementById('delayedticketviewbox'), 
                                                    document.getElementById('completeticketviewbox'));