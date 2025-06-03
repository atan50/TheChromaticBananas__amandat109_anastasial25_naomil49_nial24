// hue
var hue_slider = document.getElementById("hue_slider");
var selected_hue = document.getElementById("selected_hue");
selected_hue.innerHTML = hue_slider.value;


hue_slider.oninput = function(){
  selected_hue.innerHTML = this.value;
}

// saturation
var sat_slider = document.getElementById("sat_slider");
var selected_sat = document.getElementById("selected_sat");
selected_sat.innerHTML = sat_slider.value;


sat_slider.oninput = function(){
  selected_sat.innerHTML = this.value;
}

// brightness
var br_slider = document.getElementById("br_slider");
var selected_br = document.getElementById("selected_br");
selected_br.innerHTML = br_slider.value;


br_slider.oninput = function(){
  selected_br.innerHTML = this.value;
}
