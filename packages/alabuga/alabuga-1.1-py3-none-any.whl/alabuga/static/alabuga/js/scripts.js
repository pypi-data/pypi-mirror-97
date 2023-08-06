function render(json, id){
	var element = document.getElementById(id);
	for (i = element.length - 1; i > 0; i--) {
		element.remove(i);
	}
	for (var obj in json.data){
		var option = document.createElement("option");
		option.value = json.data[obj].id;
		option.text = json.data[obj].title;
		element.add(option, element[element.length]);		
	}
}

function country_handle(){
	var sel_country = document.getElementById('id_country');
	var sel_sub_region = document.getElementById('id_sub_region');
	var sel_brand = document.getElementById('id_brand');

	for (i = sel_sub_region.length - 1; i > 0; i--) {
		sel_sub_region.remove(i);
	}

	for (i = sel_brand.length - 1; i > 0; i--) {
		sel_brand.remove(i);
	}


	var ind = sel_country.options[sel_country.selectedIndex].value;
	fetch(`/alabuga/regions/${ind}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		}
	}).then(response => response.json()).then(json => render(json, 'id_region')).catch(error => console.error(error))
}

function region_handle(){
	var sel_region = document.getElementById('id_region');
	var sel_brand = document.getElementById('id_brand');
	for (i = sel_brand.length - 1; i > 0; i--) {
		sel_brand.remove(i);
	}

	var ind = sel_region.options[sel_region.selectedIndex].value;
	fetch(`/alabuga/sub-regions/${ind}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		}
	}).then(response => response.json()).then(json => render(json, 'id_sub_region')).catch(error => console.error(error));

}

function sub_region_handle(){
	var sel_region = document.getElementById('id_region');
	var sel_sub_region = document.getElementById('id_sub_region');
	var ind = sel_region.options[sel_region.selectedIndex].value;
	var ind_sub = sel_sub_region.options[sel_sub_region.selectedIndex].value;
	fetch(`/alabuga/brands/?reg=${ind}&sub-reg=${ind_sub}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		}
	}).then(response => response.json()).then(json => render(json, 'id_brand')).catch(error => console.error(error))
}
