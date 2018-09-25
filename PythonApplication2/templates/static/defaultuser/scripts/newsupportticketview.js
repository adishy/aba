function newsupportticketview(){
	/*******************************************************************/
	/**New Support Ticket Details**/
	/*******************************************************************/
	this.supporttype = '';
	
	this.supportdescription = '';
	
	this.supportlocation = '';
	
	this.supportdate = '';

	this.supporttime = '';
	
	/*******************************************************************/
	/**Support Ticket View Element ID**/
	/*******************************************************************/
	this.elementid = Math.floor(Math.random() * 100000000);
	
	this.csrfidvalue = '';
	
	/*******************************************************************/
	/**DOM Elements**/
	/*******************************************************************/
	this.elementInDOM = '';
 
	this.supporttypeElementInDOM = '';
	
	this.supportdescriptionElementInDOM = '';
	
	this.supportlocationElementInDOM = '';
	
	this.supportdatetimeElementInDOM = '';
	
	this.supportdescriptionstextElementInDOM = '';
	
	this.supportlocationstextElementInDOM = '';
	
	this.character_check_length = 120;

	this.elementData = function(){
			return 	`<div class="ongoingticketview">
							<div class="newsupporttickettitle">
								<p>New Support Ticket</p>	
							</div>
							
							<div class="issueinputexpandtitle">
								<p>SUPPORT AREA</p>
							</div>
							
							<div class="issuetype">
								<select id="${this.elementid}_supporttype">
								</select>
							</div>

							<div class="issueinputexpandtitle">
								<p>DESCRIPTION</p>
							</div>
							
							<div class="issuesupportdescription">
								<input type="text" id="${this.elementid}_supportdescription" list="${this.elementid}_supportdescriptionstext" maxlength="120" placeholder="Enter a detailed description of your issue">
								<datalist id="${this.elementid}_supportdescriptionstext">
								</datalist>
								<p class="issuedescriptionlength">${this.character_check_length} characters</p>
							</div>

							<div class="issueinputexpandtitle">
								<p>LOCATION</p>
							</div>
							
							<div class="issuelocationtext">
								<input id="${this.elementid}_supportlocation" list="${this.elementid}_supportlocationstext" type="text" placeholder="Tell us where you need support on campus">
								<datalist id="${this.elementid}_supportlocationstext">
								</datalist>
							</div>
							
							<div class="issueinputexpandtitle">
								<p>REQUIRED DATE AND TIME</p>
							</div>
							
							<div class="issuetype">
								<select class="supportdatetimeentry">
									<option>
										Today, as early as possible
									</option>
									<option>
										Choose a lesson
									</option>
									<option>
										Custom date and time
									</option>
								</select>
							</div>
						
							<div class="supporttime supportdatetime_lessons">
								<i class="fas fa-calendar"></i>
								<input class="supportdateview lessonsdateentry" type="date">
								
								<span class="supportdetailtimebox">
									<i class="fas fa-clock"></i>	
									<select class="supportdatetimelessonsentry">
									</select>
								</span>
							</div>

							<div class="supporttime supportdatetime_customdatetime">
								<i class="fas fa-calendar"></i>
								<input id="${this.elementid}_supportdateentry" class="supportdateview customdateentry" type="date">
								
								<span class="supportdetailtimebox">
									<i class="fas fa-clock"></i>
									<input id="${this.elementid}_supporttimeentry" type="time">
								</span>
							</div>
							
							<div class="supportcreatebox">
								<div id="${this.elementid}_createsupportticket" class="createticket">
									<p>CREATE TICKET</p>
								</div>
								<div class="supportticketcancel" onclick="toggleHidden(SUPPORT_TICKET_ENTRY)">
									<p>CANCEL</p>
								</div>
							</div>
						</div>`;
	};
	

	this.supportdatetimeEntryElement = '';

	this.supportdatetimeLessonEntryElement = '';

	this.supportdatetimeLessons = 	['07:30', 
									 '07:40', 
									 '08:20', 
									 '09:00', 
									 '09:05', 
									 '09:45', 
									 '10:25', 
									 '11:05',
									 '11:45',
									 '12:25',
									 '12:55',
									 '13:35'];

	this.getLessonsTime = function(){
		return this.supportdatetimeLessons[this.supportdatetimeLessonEntryElement.selectedIndex];
	};

	this.addSupportTicket = function(){
		var some_supportdatetime = '';

		switch(this.supportdatetimeEntryElement.selectedIndex){
			case 0:
			break;

			case 1:
				if(document.querySelector('.lessonsdateentry').value.length == 0){
					throw new Error('Support date not provided');
				}
				
				some_supportdatetime = `${document.querySelector('.lessonsdateentry').value} ${this.getLessonsTime()}`;
				
				if(Date.now() > Date.parse(some_supportdatetime)) throw new Error('Invalid support date or time');
				
			break;

			case 2:
				if(document.querySelector('.customdateentry').value.length == 0 || document.getElementById(`${this.elementid}_supporttimeentry`).value.length == 0){
					throw new Error('Support date and time not provided');
				}

				some_supportdatetime = `${document.querySelector('.customdateentry').value} ${document.getElementById(`${this.elementid}_supporttimeentry`).value}`;

				if(Date.now() > Date.parse(some_supportdatetime)) throw new Error('Invalid support date or time');

			break;
		}

		var currentNewSupportTicketView = this;

		if(currentNewSupportTicketView.supportdescription.length ==  0){
			throw new Error('Support description not provided');
		}

		if(currentNewSupportTicketView.supportlocation.length == 0){
			throw new Error('Support location not provided');
		}

		if(currentNewSupportTicketView.supporttype.length == 0){
			throw new Error('Support type not provided');
		}

		socket.emit('addsupportticket', 
					{supporttype: currentNewSupportTicketView.supporttype, 
					supportdescription: currentNewSupportTicketView.supportdescription,
					supportlocation: currentNewSupportTicketView.supportlocation,
					supportdatetime: some_supportdatetime,
					csrfidvalue: currentNewSupportTicketView.csrfidvalue});
	};
	
	this.getSupportTypesText = function(){
		console.log(this.supportTypeOptionsText);
		
		for(var i = 0; i < this.supportTypeOptionsText.length; ++i){
			this.supporttypeElementInDOM.innerHTML += `<option>${this.supportTypeOptionsText[i]}</option>`;
		}
	};
	
	this.getCSRFID = function(){
		socket.emit('csrfidtext');
	};

	this.getNewSupportTicketViewDetails = function(){
		console.log('new support ticket view details');
		socket.emit('supporttypeoptiontext');
		this.getCSRFID();
	};

	this.addSupportTicketView = function(){
		this.elementInDOM.innerHTML = this.elementData();

		this.supporttypeElementInDOM = document.getElementById(`${this.elementid}_supporttype`);
		this.supportdescriptionElementInDOM = document.getElementById(`${this.elementid}_supportdescription`);
		this.supportlocationElementInDOM = document.getElementById(`${this.elementid}_supportlocation`);
		this.supportdatetimeElementInDOM = document.getElementById(`${this.elementid}_supportdatetime`);
		this.supportdescriptionstextElementInDOM = document.getElementById(`${this.elementid}_supportdescriptionstext`);
		this.supportlocationstextElementInDOM = document.getElementById(`${this.elementid}_supportlocationstext`);
		this.supportticketbuttonElementInDOM = document.getElementById(`${this.elementid}_createsupportticket`)
		
		var supportdatetimeLessonElementInDOM = document.querySelector('.supportdatetime_lessons');

		var supportdatetimeCustomDatetimeElementInDOM = document.querySelector('.supportdatetime_customdatetime');
		
		this.supportdatetimeEntryElement = document.querySelector('.supportdatetimeentry');

		this.supportdatetimeLessonEntryElement = document.querySelector('.supportdatetimelessonsentry');

		this.supportdatetimeEntryElement.onchange = function(){
			switch(this.selectedIndex){
				case 0:
					supportdatetimeLessonElementInDOM.style.display = 'none';
					supportdatetimeCustomDatetimeElementInDOM.style.display = 'none';
				break;

				case 1:
					supportdatetimeLessonElementInDOM.style.display = 'block';
					supportdatetimeCustomDatetimeElementInDOM.style.display = 'none';
				break;

				case 2:
					supportdatetimeLessonElementInDOM.style.display = 'none';
					supportdatetimeCustomDatetimeElementInDOM.style.display = 'block';
				break;
			}
		}

		var lessonNames = [ 'Advisory (7:30-7:40)',
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

		for(var i = 0; i < this.supportdatetimeLessons.length; ++i){
			this.supportdatetimeLessonEntryElement.innerHTML += `<option>${lessonNames[i]}</option>`;
		}

		this.getNewSupportTicketViewDetails();
		
		var today = new Date().toISOString().split('T')[0];

		console.log(new Date().toISOString().split('T')[1]);

		var dateentryElements = document.querySelectorAll('.supportdateview');
		
		for(var i = 0; i < dateentryElements.length; ++i){
			dateentryElements[i].setAttribute('min', today);
			dateentryElements[i].setAttribute('value', today);
		}

		var currentNewSupportTicketView = this;
		
		this.supporttypeElementInDOM.onchange = function(){
			currentNewSupportTicketView.supporttype = currentNewSupportTicketView.supporttypeElementInDOM
								   .options[currentNewSupportTicketView.supporttypeElementInDOM
																	   .selectedIndex]
								   .value;
		};
		
		this.supportdescriptionElementInDOM.onchange = function(){
			currentNewSupportTicketView.supportdescription = this.value;
		};
		
		this.supportlocationElementInDOM.onkeyup = function(){
			currentNewSupportTicketView.supportlocation = this.value;
			socket.emit('supportlocation',
						{supportlocationprovided: currentNewSupportTicketView.supportlocation});
		};
							   
		this.supporttypeElementInDOM.onchange = function(){
				currentNewSupportTicketView.supporttype = currentNewSupportTicketView.supporttypeElementInDOM
							   .options[currentNewSupportTicketView.supporttypeElementInDOM.selectedIndex]
							   .value;
				
				socket.emit('supportdescription', 
							{supporttype: currentNewSupportTicketView.supporttype})

				console.log(currentNewSupportTicketView.supporttype);
		};

		socket.on('addedsupportticket', function(){
			socket.emit('csrfidtext');
		});

		socket.on('supportdescriptiontext', function(some_descriptions_provided){
			currentNewSupportTicketView.getSupportDescriptionsText(JSON.parse(some_descriptions_provided));
		});
		
		socket.on('supportlocationtext', function(some_locations_provided){
			currentNewSupportTicketView.getSupportLocationsText(some_locations_provided.supportlocations);
		});
		
		socket.on('supporttypeoptions', function(some_options_provided){
			console.log(some_options_provided);
			
			for(var i = 0; i < some_options_provided.length; ++i){
				currentNewSupportTicketView.supportTypeOptionsText
										   .push(some_options_provided[i].supporttypedetails);
			}
			currentNewSupportTicketView.getSupportTypesText();
			
			currentNewSupportTicketView.supporttype = currentNewSupportTicketView.supporttypeElementInDOM
								   .options[0]
								   .value;
								   
			socket.emit('supportdescription', 
						{supporttype: currentNewSupportTicketView.supporttype})
						
			console.log(currentNewSupportTicketView.supporttype);
			console.log(currentNewSupportTicketView.supporttypeElementInDOM.options);
		});
		
		socket.on('csrfid', function(some_csrfidvalue_provided){
			console.log(some_csrfidvalue_provided)
			currentNewSupportTicketView.csrfidvalue = some_csrfidvalue_provided.csrfid;
		});
		
		document.getElementById(`${this.elementid}_supportdescription`).onkeyup = function(){
			var text_description_length_element = document.querySelector('.issuedescriptionlength');
			var text_description_length = 120 - this.value.length;
			text_description_length_element.innerHTML = `${text_description_length} characters`;

			if(text_description_length <= 0) text_description_length_element.style.color = '#e93e2c';

			else text_description_length_element.style.color = '#606060';
		};

		this.supportticketbuttonElementInDOM.onclick = function(){
			try{
				currentNewSupportTicketView.addSupportTicket();
				currentNewSupportTicketView.elementInDOM.style.display = 'none';
			}
			catch(some_error){
				notificationList.addNotification(some_error.toString());
			};
		};
	};
	
	this.getSupportDescriptionsText = function(some_descriptions_provided){
		this.supportdescriptionstextElementInDOM.innerHTML = '';
		
		for(var i = 0; i < some_descriptions_provided.length; ++i){
			this.supportdescriptionstextElementInDOM.innerHTML += `<option value="${some_descriptions_provided[i]}">`;
		}
	};

	this.getSupportLocationsText = function(some_locations_provided){
		this.supportlocationstextElementInDOM.innerHTML = '';
		
		for(var i = 0; i < some_locations_provided.length; ++i){
			this.supportlocationstextElementInDOM.innerHTML += `<option value="${some_locations_provided[i]}">`;
		}
	};

	this.supportTypeOptionsText = [];
};