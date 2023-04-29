$(document).ready(function() {
  var data = [];
  $.ajax({
    url: 'voice_actors_1-50_2023-04-27_01-26-48.json',
    dataType: 'json',
    async: false,
    success: function(json) {
      data = data.concat(json.data);
    }
  });
  $.ajax({
    url: 'voice_actors_51-100_2023-04-27_23-05-45.json',
    dataType: 'json',
    async: false,
    success: function(json) {
      data = data.concat(json.data);
    }
  });
  $.ajax({
    url: 'voice_actors_200-224_2023-04-27_01-31-59.json',
    dataType: 'json',
    async: false,
    success: function(json) {
      data = data.concat(json.data);
    }
  });
  $('#actor-roles').DataTable({
    data: data,
    columns: [
      { data: 'name' },
      { data: 'role' },
      { data: 'anime' },
      { data: 'info' }    
    ]
  });
});
