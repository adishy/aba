var supportticketcomment = {
	elementInDOM: '',

	elementData: function(){
				return `<div class="commenttextbox">
						</div>
						<div class="commentaddbox">
								<textarea id="commentaddvaluebox" class="commentaddvalue" rows="1" placeholder="Add a comment"></textarea>
								<p id="commentaddbuttonview" class="commentaddbutton">ADD</p>
						</div>`
				 },

	
	commentBoxElementInDOM: '',

	supportid: '',

	userImageUrl: '',

	supportStaffImageUrl: '',

	userCommentText: function(some_text_provided){
		return `<div class="usercommentbox">
					<div class="userimage" style="background: url('${this.userImageUrl}'); background-position: center; background-size: cover;">
					</div>
					<div class="username">
						YOU:
					</div>
					<div class="usercommenttext">
						${some_text_provided}
					</div>
				</div>`;		
	},

	supportStaffCommentText: function(some_text_provided){
		return `<div class="supportstaffcommentbox">
					<div class="userimage" style="background: url('${this.supportStaffImageUrl}'); background-position: center; background-size: cover;">
					</div>
					<div class="username">
						SUPPORT STAFF:
					</div>
					<div class="supportstaffcommenttext">
						${some_text_provided}
					</div>
				</div>`;
	},

	getCommentText: function(){
		var supportTicketCommentBox = this;

		socket.emit('viewsupportticketcomments', 
				    {supportid: supportTicketCommentBox.supportid});
	},

	showCommentText: function(some_support_ticket_comments){
		this.commentBoxElementInDOM.innerHTML = '';

		console.log(some_support_ticket_comments);

		for(var i = 0; i < some_support_ticket_comments.length; ++i){
			if(some_support_ticket_comments[i].commentauthor == 1){
				this.commentBoxElementInDOM.innerHTML += this.userCommentText(some_support_ticket_comments[i].commenttext);
				continue;
			}

			else{
				this.commentBoxElementInDOM.innerHTML += this.supportStaffCommentText(some_support_ticket_comments[i].commenttext);
			}
		}
	},

	addComment: function(some_support_ticket_comment_text){
		socket.emit('addsupportticketcomments', 
					{supportid: this.supportid, 
					 commenttext: some_support_ticket_comment_text});
	},

	addSupportTicketCommentBox: function(some_element_in_DOM, 
										 some_supportid, 
										 some_user_image_url, 
										 some_support_staff_image_url){
		
		console.log('Support ticket comments');

		this.elementInDOM = some_element_in_DOM;

		this.elementInDOM.innerHTML = this.elementData();

		this.commentBoxElementInDOM = document.querySelector('.commenttextbox');

		this.supportid = some_supportid;

		this.userImageUrl = some_user_image_url;

		this.supportStaffImageUrl = some_support_staff_image_url;

		var supportTicketCommentAddValue = document.getElementById('commentaddvaluebox');

		var supportTicketCommentAddButton = document.getElementById('commentaddbuttonview');

		var supportTicketCommentBox = this;

		socket.on('supportticketcomments', function(some_support_ticket_comments){
			supportTicketCommentBox.showCommentText(some_support_ticket_comments);
		});		

		this.getCommentText();

		supportTicketCommentAddButton.onclick = function(){
			supportTicketCommentBox.addComment(supportTicketCommentAddValue.value);
		};

		socket.on('addedsupportticketcomment', function(){
			supportTicketCommentBox.getCommentText();
			supportTicketCommentAddValue.value = '';
		});
	}
};
var supportticketdetails = {
	elementInDOM: '',
	
	elementid: '',
	
	elementData: function(some_ticket_provided){
		console.log(some_ticket_provided);
		
		this.elementid = Math.floor(Math.random() * 100000000);
				
		function getSupportTime(some_date_time_provided){
			var LESSON_TIMES = 	['7:30 am', 
								 '7:40 am', 
								 '8:20 am', 
								 '9:00 am', 
								 '9:05 am', 
								 '9:45 am', 
								 '10:25 am', 
								 '11:05 am',
								 '11:45 am',
								 '12:25 pm',
								 '12:55 pm',
								 '1:35 pm'];
							
			if(LESSON_TIMES.indexOf(some_date_time_provided) == -1) return some_date_time_provided;
		
			var lessonNames =  [ 'Advisory (7:30-7:40)',
								 'Period 1 (7:40-8:20)',
								 'Period 2 (8:20-9:00)',
								 'Locker Break (9:00-9:05)',
								 'Period 3 (9:05-9:45)',
								 'Period 4 (9:45-10:25)',
								 'BREAK-1 (10:25-11:05)',
								 'Period 5 (11:05-11:45)',
								 'Period 6 (11:45-12:25)',
								 'BREAK-2 (12:25-12:55)',
								 'Period 7 (12:55-13:35)',
								 'Period 8 (13:35-14:15)'];
		
			return lessonNames[LESSON_TIMES.indexOf(some_date_time_provided)];
		}

		var supportDatetimeProvided = new Date(Date.parse(some_ticket_provided.supportdatetime));

		var ticketSubmissionDatetimeProvided = new Date(Date.parse(some_ticket_provided.ticketsubmissiondatetime));

		var supportDateTimeText = '';
		
		var dateOptions = {year: 'numeric', month: 'long', day: 'numeric'};

		var timeOptions = {hour12: true, hour: 'numeric', minute: 'numeric'};

		if(supportDatetimeProvided.getTime() == ticketSubmissionDatetimeProvided.getTime()) supportDateTimeText = 'As Early as Possible';

		else supportDateTimeText = `${supportDatetimeProvided.toLocaleDateString('en-GB', dateOptions)} ${getSupportTime(supportDatetimeProvided.toLocaleTimeString('en-GB', timeOptions))}`;
		
	
		return `<div id="${this.elementid}" class="supportticketdetails">
						<div class="issueexpanddisplay">
							<div class="issuedisplaypicture">
								<i class="fas fa-exclamation-circle fa-lg"></i>
							</div>
							<div class="issueexpanddisplaytext">
								<p>ISSUE ID: ${some_ticket_provided.supportid}</p>
							</div>
							<div class="issueoption" onclick="supportticketdetails.removeSupportTicketDetails()">
								<i class="fas fa-times"></i>
							</div>
						</div>
						
						<div class="issueexpandtitle">
							<p>SUPPORT AREA</p>
						</div>
						
						<div class="issueexpandname">
							<p>${some_ticket_provided.supporttype}</p>
						</div>
						
						<div class="issueexpandtitle expandtitledown">
							<p>SUPPORT DESCRIPTION</p>
						</div>
						
						<div class="issueexpandtextsupportdescrirption">
							<p>${some_ticket_provided.supportdescription}</p>
						</div>
						
						<div class="issueexpanddetails">
							<div class="issueexpandtime issueexpanddetailbox">
								<div class="issueexpanddetailtitle">
									<p><i class="fas fa-calendar"></i> REPORTED ON</p>
								</div>
								<div class="issueexpanddetailtext">
									<p>${ticketSubmissionDatetimeProvided.toLocaleDateString('en-GB', dateOptions)} ${ticketSubmissionDatetimeProvided.toLocaleTimeString('en-GB', timeOptions)}</p>
								</div>
							</div>	
						<div class="issueexpandtime issueexpanddetailbox">
								<div class="issueexpanddetailtitle">
									<p><i class="fas fa-calendar"></i> SUPPORT DATE &amp; TIME</p>
								</div>
								<div class="issueexpanddetailtext">
									<p>${supportDateTimeText}</p>
								</div>
							</div>	
							<div class="issueexpandlocation issueexpanddetailbox issueexpanddetailboxdown">
								<div class="issueexpanddetailtitle">
									<p><i class="fas fa-map-marker"></i> SUPPORT LOCATION</p>
								</div>
								<div class="issueexpanddetailtext">
									<p>${some_ticket_provided.supportlocation}</p>
								</div>
							</div>
							<div class="issueexandstaff issueexpanddetailbox issueexpanddetailboxdown">
								<div class="issueexpanddetailtitle">
									<p><i class="fas fa-user"></i> ATTENDED BY</p>
								</div>
								<div class="issueexpanddetailtext">
									<p>${some_ticket_provided.supportstaffassigned}</p>
								</div>
							</div>
						</div>
						
						${some_ticket_provided.supportstatustype === 'Ongoing' 
						&& `<div class="issueexpandetaview">
									<div class="issueexpandetabox">
										<p class="issueexpandeta">${some_ticket_provided.supportstatusdescription}</p>
									</div>
							</div>` 
						|| some_ticket_provided.supportstatustype === 'Delayed' 
						&& `<div class="issueexpandetaview">
									<div class="issueexpanddelayedetabox">
										<p class="issueexpandeta">Action on this issue delayed</p>
									</div>
							</div>` 
						|| some_ticket_provided.supportstatustype === 'Complete' 
							&& ''}
						
						${some_ticket_provided.supportstatustype === 'Delayed' 
							&& `<div class="issueexpandtitle">
									<p>REASON</p>
								</div>
						
								<div class="issueexpandtextsupportdescrirption">
									<p>${some_ticket_provided.supportstatusdescription}</p>
								</div>` 
						|| some_ticket_provided.supportstatustype != 'Delayed' 
							&& ''}
								
						<div class="issueexpandtitle">
							<p>COMMENTS</p>
						</div>

						<div class="commentbox">
						</div>

						<div class="issueexpandbuttonview" onclick="copysupportticketdetails('${some_ticket_provided.supportid}')">
							<div class="issueexpandbutton">
								<p><i class="fas fa-clone"></i> COPY ISSUE</p>
							</div>
							
							<div class="issueexpandbutton" onclick="cancelsupportticket('${some_ticket_provided.supportid}')">
								<p><i class="fas fa-trash"></i> CANCEL ISSUE</p>
							</div>
						</div>
					</div>`
	},
	
	supportTicketDetails: function(some_ticket_provided){
		if(!this.elementid.length){
			this.elementInDOM.style.display = 'block';
			this.elementInDOM.innerHTML = this.elementData(some_ticket_provided);
			console.log(some_ticket_provided);
			supportticketcomment.addSupportTicketCommentBox(document.querySelector('.commentbox'), 
															some_ticket_provided.supportid, 
															some_ticket_provided.user_image, 
															some_ticket_provided.supportstaffimage);
		}
		
		else{
			this.removeSupportTicketDetails();
			this.supportTicketDetails(some_ticket_provided);
			console.log(some_ticket_provided);
			supportticketcomment.addSupportTicketCommentBox(document.querySelector('.commentbox'), 
															some_ticket_provided.supportid, 
															some_ticket_provided.user_image, 
															some_ticket_provided.supportstaffimage);
		}
	},
	
	removeSupportTicketDetails: function(){
		if(this.elementid){
			this.elementInDOM.removeChild(document.getElementById(this.elementid));
			this.elementid = '';
			this.elementInDOM.style.display = 'none';
		}
	}
};