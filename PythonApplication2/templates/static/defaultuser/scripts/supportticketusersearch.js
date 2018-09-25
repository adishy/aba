var searchsupporttickets = {
            elementInDOM: '',
            
            supportTicketListElementInDOM: function(){
                return document.querySelector('.searchresultview');
            },

            searchBoxElementInDOM: function(){
                return document.querySelector('.searchboxvalue');
            },

            addSearchSupportTicketsBox: function(){
                var currentSupportTicketSearchBox = this;

                this.elementInDOM = document.querySelector('.searchresultbox');

                var currentSupportTicketSearchBoxRemoveElement = document.querySelector('.searchresultclosebox');
                
                currentSupportTicketSearchBoxRemoveElement.onclick = function(){
                    console.log('Remove support ticket search box');
                    toggleHidden(this);
                    toggleHidden(currentSupportTicketSearchBox.elementInDOM);
                    toggleHidden(document.querySelector('.user_image_display'));
                };

                toggleHidden(document.querySelector('.user_image_display'));

                this.searchBoxElementInDOM().onclick = function(){
                    toggleHidden(currentSupportTicketSearchBox.elementInDOM);
                    toggleHidden(document.querySelector('.user_image_display'));
                    toggleHidden(currentSupportTicketSearchBoxRemoveElement);
                };

                this.searchBoxElementInDOM().onkeyup = function(){
                    if(this.value.length) currentSupportTicketSearchBox.getSupportTickets(this.value);		 

                    else currentSupportTicketSearchBox.supportTicketListElementInDOM().innerHTML = '';
                };
            },

            showTickets: function(some_support_ticket_list){
                this.supportTicketListElementInDOM().innerHTML = '';

                for(var i = 0; i < some_support_ticket_list.length; ++i){
                    this.supportTicketListElementInDOM().innerHTML += (new supportticket(some_support_ticket_list[i], true)).getSupportTicket();
                }
            },

            getSupportTickets: function(some_support_ticket_text){
                var currentSupportTicketSearchBox = this;

                var supportticketssearch = new XMLHttpRequest();

                supportticketssearch.open('POST', 
                                            '/searchusersupporttickets', 
                                            true);

                supportticketssearch.setRequestHeader('content-type', 
                                                        'application/x-www-form-urlencoded');

                supportticketssearch.onloadend = function(){
                                                    currentSupportTicketSearchBox.showTickets(JSON.parse(this.responseText));
                                                    }

                supportticketssearch.send(`search_details=${some_support_ticket_text}`);
            }
        }

        searchsupporttickets.addSearchSupportTicketsBox();