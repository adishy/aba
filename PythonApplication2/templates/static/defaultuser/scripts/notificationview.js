function notificationview(some_text_provided, 
						  some_notification_category, 	
						  some_element_in_dom_provided){
		var elementid = Math.floor(Math.random() * 100000000);
		
		some_element_in_dom_provided.innerHTML = `<div id=${elementid} class="notificationbox hidden">
														<div class="notificationtext">
															
															${some_notification_category == null 
															  && `<i class="fas fa-info-circle fa-lg"></i>` 
														   || some_notification_category == 'success' 
															  && `<i class="fas fa-check-circle fa-lg"></i>` 
														   || some_notification_category == 'error' 
															  && `<i class="fas fa-times-circle fa-lg"></i>` 
														   || some_notification_category 
															  && ''}
														   <span>
																${some_text_provided}
														   </span>
														   
														</div>
												  </div>`;	
		
		document.getElementById(elementid).style.display = 'block';
		
		document.getElementById(elementid).classList.add('animation-target_3');

		return elementid;
	}

var notificationList = {
	notificationTime: 3000,
	
	notificationElementInDOM: '',
	
	addNotification: function(some_text_provided, 
							  some_notification_category_provided){
		var currentNotification = notificationview(some_text_provided, 
												   some_notification_category_provided, 
												   this.notificationElementInDOM);
		
		setTimeout(function(){
			var currentNotificationElementInDOM = document.getElementById(currentNotification);
			currentNotificationElementInDOM.parentNode.removeChild(currentNotificationElementInDOM);
		}, this.notificationTime);
	}
};

var notificationBoxView = {
	elementInDOM: '',

	elementData: function(){
					return `<div class="usernotificationtitle">
									<i class="far fa-bell fa-lg usernotificationtitledetail"></i>
									<p class="usernotificationtitledetail">NOTIFICATIONS</p>
								</div>
								<p class="usernotificationclearbutton">CLEAR</p>

								<div class="usernotificationtextlist">
								</div>` 
				  },

	notificationList: [],

	newNotificationElementInDOM: '',

	notificationTextElementData: function(some_notification){
									var notificationtextprovided = JSON.parse(some_notification.notificationtext);

									return 	`<div id="${some_notification.notificationid}" class="usernotificationtext">
												<div class="usernotificationpicture">
													<i class="fas fa-exclamation-circle fa-lg"></i>
												</div>
												<div>
													<p class="usernotificationtexttitle">${notificationtextprovided.title}</p>
													<p class="usernotificationtexview">${notificationtextprovided.notificationbody}</p>
												</div>
											</div>`;
								},

	notificationListElementInDOM: function(){
										return document.querySelector('.usernotificationtextlist');
								  },


	clearNotifications: function(){
							socket.emit('clearnotifications');
						},

	
	addSeenNotifications: function(){
							console.log('Add seennotifications');
							var currentNotificationListBox = this;
							socket.emit('addseennotifications', currentNotificationListBox.getSeenNotifications());
						 },

	getSeenNotifications: function(){
		var unseen_notifications = [];

		for(var i = 0; i < this.notificationList.length; ++i){
			if(parseInt(this.notificationList[i].notificationseen) == 0){
				unseen_notifications.push(this.notificationList[i].notificationid);
			}
		}

		console.log(unseen_notifications);

		return unseen_notifications;
	},

	getNotifications: function(){
							console.log('View notification text');
							socket.emit('viewnotificationtext');
					  },

	unseenNotificationElement: function(){
									return document.querySelector('.unseennotificationview');
							  },

	showNotifications: function(some_notifications){
		this.notificationListElementInDOM().innerHTML = '';
		
		var currentNotificationListBox = this;

		console.log(some_notifications);

		var unseenNotifications = true;

		for(var i = 0; i < some_notifications.length; ++i){
			this.notificationListElementInDOM().innerHTML += this.notificationTextElementData(some_notifications[i]);

			if(unseenNotifications && parseInt(some_notifications[i].notificationseen) == 0){
				console.log('Unseen notifications')
				currentNotificationListBox.unseenNotificationElement().style.display = 'block';
				currentNotificationListBox.unseenNotificationElement().classList.add('animation-target_2');
				unseenNotifications = false;
			}
		}
	},

	addNotificationListBox: function(some_element_in_DOM_provided){
		this.elementInDOM = some_element_in_DOM_provided;

		this.elementInDOM.innerHTML += this.elementData();

		var currentNotificationListBox = this;

		document.querySelector('.usernotificationclearbutton').onclick = function(){
			console.log('Clear notifications');
			currentNotificationListBox.clearNotifications();			
		};

		socket.on('notificationchanged', function(){
			currentNotificationListBox.getNotifications();
		});

		socket.on('notificationtext', function(some_notifications_provided){
			console.log(some_notifications_provided);
			currentNotificationListBox.notificationList = JSON.parse(some_notifications_provided);
			currentNotificationListBox.showNotifications(currentNotificationListBox.notificationList);
		})

		socket.on('addedseennotifications', function(){
			currentNotificationListBox.unseenNotificationElement().style.display = 'none';
		})

		this.getNotifications();
	}
};