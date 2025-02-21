
$(document).ready(function() {
	// Attach click event handler to the logout link
	$("#logout-link").on("click", function(event) {
	  event.preventDefault(); // Prevent default anchor tag behavior

	  // Optionally, prompt a confirmation before logging out
	  if (confirm("Are you sure you want to log out?")) {
		$("#logout-form").submit(); // Submit the hidden logout form
	  }
	});
  });



  $(document).ready(function() {
    // Display messages with a fade-out effect
    $('.notify').fadeIn(500);
    $('.notify').delay(5000).fadeOut(500);
});












