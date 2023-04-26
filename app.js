$(document).ready(function() {
  $('#actor-roles').DataTable({
    ajax: {
      url: 'voice_actors_1-50_2023-04-27_01-26-48.json',
      dataSrc: 'data'
    },
    columns: [
      { data: 'name' },
      { data: 'role' },
      { data: 'anime' },
      { data: 'info' }    
    ]
  });
});