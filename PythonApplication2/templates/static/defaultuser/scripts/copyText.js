//Function used from https://hackernoon.com/copying-text-to-clipboard-with-javascript-df4d4988697f
//Function on Github: https://gist.github.com/Chalarangelo/4ff1e8c0ec03d9294628efbae49216db#file-copytoclipboard-js 
function copyTextProvided(some_text_provided){
	  var el = document.createElement('textarea');  
	  el.value = some_text_provided;                                 
	  el.setAttribute('readonly', '');                
	  el.style.position = 'absolute';                 
	  el.style.left = '-9999px';                      
	  document.body.appendChild(el);                  
	  var selected =            
		document.getSelection().rangeCount > 0        
		  ? document.getSelection().getRangeAt(0)     
		  : false;                                    
	  el.select();                                    
	  document.execCommand('copy');                   
	  document.body.removeChild(el);                  
	  if (selected) {                                 
		document.getSelection().removeAllRanges();    
		document.getSelection().addRange(selected);   
	  }
};

function getSupportTicketText(some_support_ticket_provided){
	var ticketSubmissionDateTime = new Date(Date.parse(some_support_ticket_provided.ticketsubmissiondatetime)); 
	
	var supportDatetimeProvided = new Date(Date.parse(some_support_ticket_provided.supportdatetime));

	var dateOptions = {year: 'numeric', month: 'long', day: 'numeric'};

	var timeOptions = {hour12: true, hour: 'numeric', minute: 'numeric'};
	
	var some_text_from_support_ticket = 

` Support ticket: ${some_support_ticket_provided.supportid}
 User: ${some_support_ticket_provided.user_name}
 Email: ${some_support_ticket_provided.user_email}
 Reported on ${ticketSubmissionDateTime.toLocaleDateString('en-GB', dateOptions)} ${ticketSubmissionDateTime.toLocaleTimeString('en-GB', timeOptions)}
 Support ticket type: ${some_support_ticket_provided.supportstatustype} 
 Support type: ${some_support_ticket_provided.supporttype}
 Support description: ${some_support_ticket_provided.supportdescription}
 Support status: ${some_support_ticket_provided.supportstatusdescription}
 Attended by: ${some_support_ticket_provided.supportstaffassigned}
 Support staff email: ${some_support_ticket_provided.supportstaffemail}
 Support date and time: ${supportDatetimeProvided.toLocaleDateString('en-GB', dateOptions)} ${supportDatetimeProvided.toLocaleTimeString('en-GB', timeOptions)}`;

	copyTextProvided(some_text_from_support_ticket);									
}