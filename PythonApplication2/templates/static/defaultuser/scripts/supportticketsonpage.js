function supportticket(some_ticket_provided, 
	support_ticket_search = false){
this.supportid = some_ticket_provided.supportid;

this.ticketsubmissiondatetime = some_ticket_provided.ticketsubmissiondatetime;

this.user_name = some_ticket_provided.user_name;

this.user_email = some_ticket_provided.user_email;

this.supporttype = some_ticket_provided.supporttype;

this.supportdescription = some_ticket_provided.supportdescription;

this.supportstatustype = some_ticket_provided.supportstatustype;

this.supportstatusdescription = some_ticket_provided.supportstatusdescription;

this.supportlocation = some_ticket_provided.supportlocation;

this.supportdatetime = some_ticket_provided.supportdatetime;

this.supportstaffemail = some_ticket_provided.supportstaffemail;

this.supportstaffassigned = some_ticket_provided.supportstaffname;

this.user_image = some_ticket_provided.user_image;

this.supportstaffimage = some_ticket_provided.supportstaffimage;

this.elementid = this.supportid + '_' + Math.floor(Math.random() * 100000000);

this.getSupportTicket  = function(){
var ONGOING_SUPPORT_TICKET_KEY = 'Ongoing';

var DELAYED_SUPPORT_TICKET_KEY = 'Delayed';

var COMPLETE_SUPPORT_TICKET_KEY = 'Complete';

function getSupportTime(some_date_time_provided){
	var LESSON_TIMES = 	['7:30 AM', 
						 '7:40 AM', 
						 '8:20 AM', 
						 '9:00 AM', 
						 '9:05 AM', 
						 '9:45 AM', 
						 '10:25 AM', 
						 '11:05 AM',
						 '11:45 AM',
						 '12:25 PM',
						 '12:55 PM',
						 '1:35 PM'];
					
	if(LESSON_TIMES.indexOf(some_date_time_provided) == -1) return some_date_time_provided;

	var lessonNames =  ['Advisory',
						'P1',
						'P2',
						'Locker Break',
						'P3',
						'P4',
						'BREAK-1',
						'P5',
						'P6',
						'BREAK-2',
						'P7',
						'P8'];

	return lessonNames[LESSON_TIMES.indexOf(some_date_time_provided)];
}

var reportedDatetimeProvided = new Date(Date.parse(this.ticketsubmissiondatetime));

var supportDatetimeProvided = new Date(Date.parse(this.supportdatetime));

var dateOptions = {year: 'numeric', month: 'long', day: 'numeric'};

var timeOptions = {hour12: true, hour: 'numeric', minute: 'numeric'};

var supportTimeText = '';

if(supportDatetimeProvided.getTime() == reportedDatetimeProvided.getTime()) supportTimeText = 'As Early as Possible';

else supportTimeText = getSupportTime(supportDatetimeProvided.toLocaleTimeString('en-GB', timeOptions).toUpperCase());

var supportDateText  = supportDatetimeProvided.toLocaleDateString('en-GB', dateOptions).toUpperCase()

return `<div id='${this.elementid}' class="ticketview ${support_ticket_search
											 && `searchticketdetailsview` 
										 || !support_ticket_search 
											 && ``}" onclick="showticketdetails(event, '${this.supportid}')">
<div id='${this.supportid}' class="supportticketactionview">
 <ul>
	 <li onclick="toggleOption(document.getElementById('${this.supportid}')); 
				  supportticketdetails.supportTicketDetails('${this.supportid}')"}">Expand issue</li>
	 <li onclick="copysupportticketdetails('${this.supportid}')">Copy issue</li>
	 <li onclick="cancelsupportticket('${this.supportid}')">Cancel issue</li>
 </ul>
</div>
<div class="issuedisplay">
 <div class="issuedisplaypicture">
	 <i class="fas fa-exclamation-circle fa-lg"></i>
 </div>
 <div class="issuedisplaytext">
	 <p>ISSUE ID: ${this.supportid}</p>
 </div>
 <div id="issueoption_${this.supportid}" class="issueoption">
	 <i class="fas fa-ellipsis-v fa-sm issueoptiondisplay"></i>
 </div>
</div>

<div class="issuename">
 <p>${this.supporttype}</p>
</div>
<div class="issuetext">
 <p>${this.supportdescription}</p>
</div>

${this.supportstatustype === ONGOING_SUPPORT_TICKET_KEY 
&& `<div class="issueeta">
	 <p>${this.supportstatusdescription}</p>
   </div>` 
|| this.supportstatustype === DELAYED_SUPPORT_TICKET_KEY 
&& `<div class="issueaction">
	 <p>Action on this issue delayed</p>
	 <div class="issueactionexpandview">
		 <i class="fas fa-caret-right issueexpandpicture"></i>
		 <p class="issueexpandtext">SEE DETAILS</p>
	 </div>
   </div>`
|| this.supportstatustype == COMPLETE_SUPPORT_TICKET_KEY 
  && ''}

 <div class="issuedetails">
 ${this.supportstatustype != COMPLETE_SUPPORT_TICKET_KEY 
 && `<div class="issuelocation detailitem">
		 <div class="issuedetailpicture">
			 <i class="fas fa-map-marker"></i>
		 </div>
		 <div class="issuedetailtext">
			 <p>${this.supportlocation.toUpperCase()}</p>
		 </div>
	 </div>` 
 || this.supportstatustype == COMPLETE_SUPPORT_TICKET_KEY 
	&& ''}

 
 <div class="issuedate detailitem">
	 <div class="issuedetailpicture">
		 <i class="fas fa-calendar"></i>
	 </div>
	 <div class="issuedetailtext">
		 <p>${supportDateText.toUpperCase()}</p>
	 </div>
 </div>
 
 ${this.supportstatustype != COMPLETE_SUPPORT_TICKET_KEY 
 && `<div class="issuetime detailitem">
		 <div class="issuedetailpicture">
			 <i class="fas fa-clock"></i>
		 </div>
		 <div class="issuedetailtext">
			 <p>${supportTimeText.toUpperCase()}</p>
		 </div>
	 </div>` 
 || this.supportstatustype == COMPLETE_SUPPORT_TICKET_KEY 
	&& ''}
 
 <div class="issuestaff detailitem">
	 <div class="issuedetailpicture">
		 <i class="fas fa-user"></i>
	 </div>
	 <div class="issuedetailtext">
		 <p>${this.supportstaffassigned.toUpperCase()}</p>
	 </div>
 </div>
</div>
</div>`;	
}
};

function supportticketlist(some_list_element_in_DOM_provided){
	this.supportTicketList = [];
	
	this.listElementInDOM = some_list_element_in_DOM_provided;
	
	this.getIndex = function(some_support_id_provided){
		try{
			
			for(var i = 0; i < this.supportTicketList.length; ++i){
				if(this.supportTicketList[i].supportid == some_support_id_provided) return i;
			}
			
			throw 'Support ticket not found';
		}
		
		catch(some_error){
			console.error(`Could not get index of support ticket: ${some_support_id_provided} due to: ${some_error}`);
			throw 'Invalid support id provided'; 
		}
	};
	
	this.removeAllElements = function(){
		this.supportTicketList = [];
		this.listElementInDOM.innerHTML = '';
	};
	
	this.ONGOING_SUPPORT_TICKET = 'Ongoing';
	
	this.DELAYED_SUPPORT_TICKET = 'Delayed';
	
	this.COMPLETE_SUPPORT_TICKET = 'Complete';
	
	this.getSupportTicket = function(some_support_id_provided){
		try{
			return this.supportTicketList[this.getIndex(some_support_id_provided)];
		}
		catch(some_error){
			return false;
		}
	};
	
	
	this.updateDOMElement = function(){
		this.listElementInDOM.innerHTML = '';
		
		var currentSupportTicketList = this;
		
		currentSupportTicketList.listElementInDOM.innerHTML = '';
		
		this.supportTicketList.forEach(function(some_ticket_provided){
			currentSupportTicketList.listElementInDOM.innerHTML += some_ticket_provided.getSupportTicket();
		});
	};
	
	this.addSupportTicket = function(some_ticket_provided, 
									 update_DOM_element = true){
		this.supportTicketList.push(new supportticket(some_ticket_provided));
		
		if(update_DOM_element) this.updateDOMElement();
		
	};
	
	this.addSupportTicketsFromList = function(some_ticket_list_provided){
		try{
			var currentSupportTicketList = this;
			some_ticket_list_provided.forEach(function(some_ticket_provided){
												currentSupportTicketList.addSupportTicket(some_ticket_provided, 
																						  false);
											  });

			this.supportTicketList.sort(function(element_one, element_two){
				var element_one_value = new Date(Date.parse(element_one.ticketsubmissiondatetime)).getTime();

				var element_two_value = new Date(Date.parse(element_two.ticketsubmissiondatetime)).getTime();

				if(element_one_value > element_two_value) return -1;

				else if(element_one_value < element_two_value) return 1;

				return 0;
			});

			this.updateDOMElement();
		}
		catch(some_error){
			console.error(`Could not add support tickets from list ${some_ticket_list_provided} due to: ${some_error}`);
		}
	};
	
	this.changeTicketValue = function(some_support_id_provided, 
									  some_property_name, 
									  some_property_value){
		try{
			this.supportTicketList[this.getIndex(some_support_id_provided)][some_property_name] = some_property_value;
		}
		
		catch(some_error){
			console.error(`Could not change property value for support ticket ${some_support_id_provided} : ${some_property_name} to: ${some_property_value} due to: ${some_error}`);
		}
	};
	
	this.removeSupportTicket = function(some_support_id_provided, 
										update_DOM_element = true){	
		try{
			this.supportTicketList.splice(this.getIndex(some_support_id_provided), 
									      1);
										  
			if(update_DOM_element) this.updateDOMElement();
		}
		
		catch(some_error){
			console.error(`Could not remove support ticket ${some_support_id_provided} due to: ${some_error}`);
		}
	};
};

function supportticketlistview(some_ongoing_list_element_provided, 
							   some_delayed_list_element_provided, 
							   some_complete_list_element_provided){
	this.ongoingTicketsList = new supportticketlist(some_ongoing_list_element_provided);
	
	this.delayedTicketsList = new supportticketlist(some_delayed_list_element_provided);
	
	this.completeTicketsList = new supportticketlist(some_complete_list_element_provided);
	
	var currentSupportTicketList = this;
	
	this.getSupportTicket = function(some_support_id_provided){
		var supportTicketLists = [this.ongoingTicketsList, 
								  this.delayedTicketsList, 
								  this.completeTicketsList];
	
		for(var i = 0; i < supportTicketLists.length; ++i){
			var supportTicketProvided = supportTicketLists[i].getSupportTicket(some_support_id_provided);
			if(supportTicketProvided) return supportTicketProvided;
		}
		
		return false;
	};
	
	this.addTicketsProvided = function(some_ticket_list_provided){
		
		this.ONGOING_SUPPORT_TICKET = 'Ongoing';
	
		this.DELAYED_SUPPORT_TICKET = 'Delayed';
		
		this.COMPLETE_SUPPORT_TICKET = 'Complete';
	
		var supportTicketLists = [[], [], []];
	
		for(var i = 0; i < some_ticket_list_provided.length; ++i){
			var supportStatusProvided = some_ticket_list_provided[i].supportstatustype;
				
			console.log(supportStatusProvided);
			
			console.log(this.ONGOING_SUPPORT_TICKET);
			
			if(supportStatusProvided === this.ONGOING_SUPPORT_TICKET){
					supportTicketLists[0].push(some_ticket_list_provided[i]);
			}
				
			else if(supportStatusProvided === this.DELAYED_SUPPORT_TICKET){
					supportTicketLists[1].push(some_ticket_list_provided[i]);
			}
				
			else if(supportStatusProvided === this.COMPLETE_SUPPORT_TICKET){
					supportTicketLists[2].push(some_ticket_list_provided[i]);
			}
		}
	
	console.log(supportTicketLists);
	
		for(var i = 0; i < supportTicketLists.length; ++i){
			switch(i){
				case 0:
					this.ongoingTicketsList.addSupportTicketsFromList(supportTicketLists[i]);
				break;
				
				case 1:
					this.delayedTicketsList.addSupportTicketsFromList(supportTicketLists[i]);
				break;
				
				case 2:
					this.completeTicketsList.addSupportTicketsFromList(supportTicketLists[i]);
				break;
			}
		}
	};
	
	this.changeTicketSupportStatusType = function(some_support_ticket_details){
		var changeSupportStatus = function(some_support_ticket_list_provided){
			var currentsupportticket = some_support_ticket_list_provided.getSupportTicket(some_support_ticket_details.supportid);
			some_support_ticket_list_provided.removeSupportTicket(some_support_ticket_details.supportid);
			currentsupportticket.supportstatustype = some_support_ticket_details.newsupportstatustype;
			
			switch(currentsupportticket.supportstatustype){
				case this.ONGOING_SUPPORT_TICKET:
					this.ongoingTicketsList.addSupportTicket(currentsupportticket);
				break;
				
				case this.DELAYED_SUPPORT_TICKET:
					this.delayedTicketsList.addSupportTicket(currentsupportticket);
				break;
				
				case this.COMPLETE_SUPPORT_TICKET:
					this.compeleteTicketsList.addSupportTicket(currentsupportticket);
				break;
			}
		};
		
		switch(some_support_ticket_details.previoussupportstatustype){
			case this.ONGOING_SUPPORT_TICKET:
				changeSupportStatus(this.ongoingTicketsList);
			break;
			
			case this.DELAYED_SUPPORT_TICKET:
				changeSupportStatus(this.delayedTicketsList);
			break;
			
			case this.COMPLETE_SUPPORT_TICKET:
				changeSupportStatus(this.completeTicketsList);
			break;
		};
		
	}
	
	this.removeAllSupportTickets = function(){
		this.ongoingTicketsList.removeAllElements();
		this.delayedTicketsList.removeAllElements();
		this.completeTicketsList.removeAllElements();
	};
};