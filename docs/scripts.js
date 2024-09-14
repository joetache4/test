function toggle_col() {
	show = document.getElementsByClassName("left");
	hide = document.getElementsByClassName("right");
	if (hide[0].classList.contains("secondary")) {
		[show, hide] = [hide, show]
	}	
	// hide cols before showing the others	 
	for (var row = 0; row < hide.length; row++) {
		hide[row].classList.toggle("secondary");
	}		
	for (var row = 0; row < show.length; row++) {
		show[row].classList.toggle("secondary");
	}
}