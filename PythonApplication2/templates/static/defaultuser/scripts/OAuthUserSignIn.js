var auth2;

var userLoggedIn = {name: '', 

					email: '',

					image: '',
	
					id: '',

					GoogleAuth: '',

					GoogleUser: '',

					GoogleUserBasicProfile: '',
					
					signOutCurrentUser: function(){
						this.GoogleAuth.signOut().then(function(some_callback_provided){
							//window.location.href = '/logout';
							some_callback_provided();
						});	
					},
					
					nameElementInDOM: '',
					
					emailElementInDOM: '',
					
					imageElementInDOM: '',
					
					
					setCurrentUser: function(){
						if(this.nameElementInDOM.length == undefined) this.nameElementInDOM.innerHTML = this.name;
						
						else
							for(var i = 0; i < this.nameElementInDOM.length; ++i) this.nameElementInDOM[i].innerHTML = this.name;
					
						if(this.emailElementInDOM.length == undefined) this.emailElementInDOM.innerHTML = this.email;
						
						else
							for(var i = 0; i < this.emailElementInDOM.length; ++i) this.emailElementInDOM[i].innerHTML = this.email;
						
						if(this.imageElementInDOM.length == undefined) this.imageElementInDOM.style.backgroundImage = `url('${this.image}')`;
						
						else
							for(var i = 0; i < this.imageElementInDOM.length; ++i) this.imageElementInDOM[i].style.backgroundImage = `url('${this.image}')`;
					},
					
					setUserElementsInDOM: function(some_elements_provided){
						this.nameElementInDOM = some_elements_provided.nameElementProvided;
						this.emailElementInDOM = some_elements_provided.emailElementProvided;
						this.imageElementInDOM = some_elements_provided.imageElementProvided;
					}
					
				   };
				   
var initClient = function() {
    gapi.load('auth2', function(){
        auth2 = gapi.auth2.init({
				client_id: '781246595138-3dkh6d0uv6icr8nt2ndu6eg19bo3ke6b.apps.googleusercontent.com'
		}).then(function(){
			userLoggedIn.GoogleAuth = gapi.auth2.getAuthInstance();
			
			userLoggedIn.GoogleUser = userLoggedIn.GoogleAuth.currentUser.get();
			
			userLoggedIn.GoogleUserBasicProfile = userLoggedIn.GoogleUser.getBasicProfile();
			
			userLoggedIn.name = userLoggedIn.GoogleUserBasicProfile.getName();
			
			userLoggedIn.email = userLoggedIn.GoogleUserBasicProfile.getEmail();
			
			userLoggedIn.image = userLoggedIn.GoogleUserBasicProfile.getImageUrl();
			
			userLoggedIn.id = userLoggedIn.GoogleUserBasicProfile.getId();
			
			userLoggedIn.setUserElementsInDOM({nameElementProvided: document.getElementById('currentusernameelement'), 
											   emailElementProvided: document.getElementById('currentuseremailelement'), 
											   imageElementProvided: document.getElementsByClassName('currentuserimage')});
			
			userLoggedIn.setCurrentUser();
						
			console.log(userLoggedIn);
		});
    });
};

initClient()