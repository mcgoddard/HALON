var character_id = 1;
var character_max = {{ characters|length }};

$( document ).ready(function() {
	for (i = 2; i <= character_max; i++) {
		$('#character-'+i).hide();
	}
	display_character();
});

function hide_character() {
	$('#character-'+character_id).hide();
}

function display_character() {
	$('#character-'+character_id).show();
	$('#character-input').val(character_id);
}

function next() {
	hide_character();
	if (character_id+1 > character_max) {
		character_id = 1;
	}
	else {
		character_id += 1;
	}
	display_character();
}

function previous() {
	hide_character();
	if (character_id-1 < 1) {
		character_id = character_max - 1;
	}
	else {
		character_id -= 1;
	}
	display_character();
}