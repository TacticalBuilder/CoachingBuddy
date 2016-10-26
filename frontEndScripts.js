//js codez

"use strict";

var formParser = function() {
	var workout = document.getElementById("workout_form").elements;
	var workout_data = {};
	var stroke = {};
	for(var i = 0; i < workout.length; i++) {
		var item = workout.item(i);
		workout_data[item.name] = item.value;
	}
	
	return workout_data;
}

var workoutReact = function(field, button) {
	if (field == "stroke") {
		var stroke_field = document.getElementById('stroke_rate');
		if (button == "set") {
			stroke_field.style.visibility = 'visible';
		} else {
			stroke_field.style.visibility = 'hidden';
		}
	}
	if (field == "piece") {
		var time_field = document.getElementById('piece_time');
		var dist_field = document.getElementById('piece_distance');
		if (button == "time") {
			dist_field.style.visibility = 'hidden';
			time_field.style.visibility = 'visible';
		}
		if (button == "dist") {
			time_field.style.visibility = 'hidden';
			dist_field.style.visibility = 'visible';
		}
	}
	return;
}

var renderTeamWorkout(roster, piece_data) {
	//temporary roster array until backend roster load function is completed
	roster = ["Brendan Luksik", "Mark Steffl", "Tyler Protivniak", "John Lettman", "Barry Rogers"];
}
