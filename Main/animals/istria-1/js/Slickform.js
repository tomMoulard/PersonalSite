$(document).ready(function(){
	
	/*
	 * AJAX Section
	 * This function will handle the contact process through AJAX
	 */
	 $('#slickform').submit(
		function slickcontactparse() {
			
			// EMAIL VALIDATION FUNCTION
			var emailReg = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
			
			// EDIT THIS SECTION IF DIFFERENT FORM ELEMENTS
			// Values
			var successmessage = "Thank you for email, we will be in contact soon!";
			var failedmessage = "There was a problem, please try again!";
			var usersname = $('#name');
			var usersemail = $('#email');
			var usersphone = $('#phone');			
			var userscomment = $('#comment');
			var usershuman = $('#human');
			var isvalid = 1;
			var url = "slickform.php";
			
			//Checking information is correct before sending data
			
			
			//CHECKING EMAIL IS PRESENT AND IS VALID
			if (usersemail.val() == "") {
				$(".slickbutton").animate({marginTop:'50px'},1000).delay(6000).animate({marginTop:'0px'},1000);
				$(".errorcontainer").html('Please Insert Your Email!');
				$(".errorcontainer").delay(1200).fadeIn(1000).delay(4000).fadeOut(1000);
				$('input[type=submit]', $("#slickform")).removeAttr('disabled');
				return false;
			}
			
			var valid = emailReg.test(usersemail.val());
			
			if(!valid) {
				$(".slickbutton").animate({marginTop:'50px'},1000).delay(6000).animate({marginTop:'0px'},1000);
				$(".errorcontainer").html('Please Enter A Valid Email!');
				$(".errorcontainer").delay(1200).fadeIn(1000).delay(4000).fadeOut(1000);
				$('input[type=submit]', $("#slickform")).removeAttr('disabled');
				return false;
			}
			//CHECKING EMAIL IS PRESENT AND IS VALID
			
			
			//CHECKING USERS NAME IS PRESENT
			if (usersname.val() == "") {
				$(".slickbutton").animate({marginTop:'50px'},1000).delay(6000).animate({marginTop:'0px'},1000);
				$(".errorcontainer").html('Please Insert Your Name!');
				$(".errorcontainer").delay(1200).fadeIn(1000).delay(4000).fadeOut(1000);
				$('input[type=submit]', $("#slickform")).removeAttr('disabled');
				return false;
			}
			//CHECKING USERS NAME IS PRESENT
			
			//CHECKING USERS PHONE NUMBER IS PRESENT AND IS ONLY NUMERIC
			if (usersphone.val() == "") {
				$(".slickbutton").animate({marginTop:'50px'},1000).delay(6000).animate({marginTop:'0px'},1000);
				$(".errorcontainer").html('Please Insert Your Phone Number!');
				$(".errorcontainer").delay(1200).fadeIn(1000).delay(4000).fadeOut(1000);
				$('input[type=submit]', $("#slickform")).removeAttr('disabled');
				return false;
			}
			
			var EnteredValue = $.trim(usersphone.val());
			var TestValue = EnteredValue.replace(" ", "");
			 if (isNaN(TestValue)) {
				$(".slickbutton").animate({marginTop:'50px'},1000).delay(6000).animate({marginTop:'0px'},1000);
				$(".errorcontainer").html('Please Enter A Valid Phone Number!');
				$(".errorcontainer").delay(1200).fadeIn(1000).delay(4000).fadeOut(1000);
				$('input[type=submit]', $("#slickform")).removeAttr('disabled');
				return false;
			}
			//CHECKING USERS NAME IS PRESENT
			
			
			//CHECKING THE USER IS HUMAN
			if (usershuman.val() != 14) {
				$(".slickbutton").animate({marginTop:'50px'},1000).delay(6000).animate({marginTop:'0px'},1000);
				$(".errorcontainer").html('Your Are You Human Math Is Incorrect!');
				$(".errorcontainer").delay(1200).fadeIn(1000).delay(4000).fadeOut(1000);
				$('input[type=submit]', $("#slickform")).removeAttr('disabled');
				return false;
			}
			//CHECKING THE USER IS HUMAN
			
			//CHECKING THE USER IS HUMAN
			if (userscomment.val() == "") {
				$(".slickbutton").animate({marginTop:'50px'},1000).delay(6000).animate({marginTop:'0px'},1000);
				$(".errorcontainer").html('You Forgot To Leave A Message!');
				$(".errorcontainer").delay(1200).fadeIn(1000).delay(4000).fadeOut(1000);
				$('input[type=submit]', $("#slickform")).removeAttr('disabled');
				return false;
			}
			//CHECKING THE USER IS HUMAN
			
			/* 
			 *
			 * POSTING DATA USING AJAX AND
			 * THEN RETREIVING DATA FROM PHP SCRIPT
			 *
			*/
			
			$.post(url,{ usersname: usersname.val(), usersemail: usersemail.val(), usersphone: usersphone.val(), userssubject: userssubject.val(), userscomment: userscomment.val(), usershuman: usershuman.val(), isvalid: isvalid } , function(data) {
				
				if(data == 'success'){
					
					$(".slickbutton").animate({marginTop:'50px'},1000).delay(6000).animate({marginTop:'0px'},1000);
					$(".successcontainer").html(successmessage);
					$(".successcontainer").delay(1200).fadeIn(1000).delay(4000).fadeOut(1000);
					$("#name").val('');
					$("#email").val('');
					$("#phone").val('');					
					$("#comment").val('');
					$("#human").val('');
					$('input[type=submit]', $("#slickform")).removeAttr('disabled');
				
				} else {
					
					$(".slickbutton").animate({marginTop:'50px'},1000).delay(6000).animate({marginTop:'0px'},1000);
					$(".errorcontainer").html(failedmessage);
					$(".errorcontainer").delay(1200).fadeIn(1000).delay(4000).fadeOut(1000);
					$('input[type=submit]', $("#slickform")).removeAttr('disabled');
					return false;
					
				}
				
			});
			
			/* 
			 *
			 * POSTING DATA USING AJAX AND
			 * THEN RETREIVING DATA FROM PHP SCRIPT
			 *
			*/
			
		}
		
	);
	
});