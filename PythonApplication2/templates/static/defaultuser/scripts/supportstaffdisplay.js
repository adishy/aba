var supportstaffmemberdetailsview = {
    loadedSupportStaffMembers: false,

    elementData: function(some_support_staff_member){

        return `<div  class="supportstaffmemberdetails">
                    <div class="supportstaffmemberbox">
                        <div class="supportstaffimage" style="background: url('${some_support_staff_member.image}'); background-position: center; background-size: cover;">
                        </div>
                        <p class="supportstaffmembertitle">${parseInt(some_support_staff_member.adminuser)
                                                                && `IT ADMINISTRATOR` 
                                                                || !parseInt(some_support_staff_member)
                                                                    && `SUPPORT STAFF MEMBER`}</p>
                        <p class="supportstaffmembername">${some_support_staff_member.name}</p>
                        <div class="supportstaffdetailsbox">
                            <div class="supportstaffdetails">
                                <i class="fas fa-envelope supportstaffmemberdetail"></i>
                                <p class="supportstaffmemberdetail">${some_support_staff_member.email}</p>
                            </div>	
                            <div class="supportstaffdetails">
                                <i class="fas fa-map-marker supportstaffmemberdetail supportstafflocationpicture"></i>
                                <p class="supportstaffmemberdetail supportstafflocationtext">${some_support_staff_member.location}</p>
                            </div>
                            <div class="supportstaffdetails">
                                <i class="fas fa-phone supportstaffmemberdetail supportstafflocationpicture"></i>
                                <p class="supportstaffmemberdetail supportstafflocationtext">${some_support_staff_member.phone}</p>
                            </div>
                        </div>
                    </div>
                </div>`
    },

    elementInDOM: document.getElementById('supportstaffmemberdetails'),

    addSupportStaffMembers: function(some_support_staff_member_list){
        if(this.loadedSupportStaffMembers) return true;
        
        for(var i = 0; i < some_support_staff_member_list.length; ++i)
            if(some_support_staff_member_list[i].firstlogin == 1) 
                this.elementInDOM.innerHTML += this.elementData(some_support_staff_member_list[i]);
    }
};	